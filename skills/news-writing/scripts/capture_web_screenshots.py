#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class Entry:
    label: str
    source_id: str
    source_name: str
    page_url: str
    capture_opts: Dict[str, str] = field(default_factory=dict)
    keywords: List[str] = field(default_factory=list)
    exclude_keywords: List[str] = field(default_factory=list)
    layout_opts: Dict[str, str] = field(default_factory=dict)


def parse_csv_keywords(raw: str) -> List[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def parse_kv_opts(raw: str) -> Dict[str, str]:
    raw = raw.strip()
    if not raw:
        return {}
    if raw.lower() == "fullpage":
        return {"fullPage": "true"}

    options: Dict[str, str] = {}
    for piece in raw.split(";"):
        piece = piece.strip()
        if not piece or "=" not in piece:
            continue
        key, value = piece.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key and value:
            options[key] = value
    return options


def parse_entry(raw: str) -> Entry:
    parts = [part.strip() for part in raw.split("|")]
    if len(parts) < 4 or len(parts) > 8:
        raise ValueError(
            "Each --entry must use format: "
            "label|source_id|source_name|page_url"
            "[|capture_opts][|keywords][|exclude_keywords][|layout_opts]"
        )
    label, source_id, source_name, page_url = parts[:4]
    if not page_url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid page_url in --entry: {page_url}")

    capture_opts = parse_kv_opts(parts[4]) if len(parts) >= 5 else {}
    keywords = parse_csv_keywords(parts[5]) if len(parts) >= 6 else []
    exclude_keywords = parse_csv_keywords(parts[6]) if len(parts) >= 7 else []
    layout_opts = parse_kv_opts(parts[7]) if len(parts) >= 8 else {}
    return Entry(
        label=label,
        source_id=source_id,
        source_name=source_name,
        page_url=page_url,
        capture_opts=capture_opts,
        keywords=keywords,
        exclude_keywords=exclude_keywords,
        layout_opts=layout_opts,
    )


def sanitize_filename(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in value.strip().lower())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "image"


def build_screenshot_url(page_url: str, provider: str, width: int, capture_opts: Dict[str, str]) -> str:
    if provider == "microlink":
        query: Dict[str, str] = {
            "url": page_url,
            "screenshot": "true",
            "meta": "false",
            "embed": "screenshot.url",
        }
        query.update(capture_opts)
        return "https://api.microlink.io/?" + urllib.parse.urlencode(query, safe=":/#.%")
    if provider == "mshots":
        encoded = urllib.parse.quote(page_url, safe="")
        return f"https://s.wordpress.com/mshots/v1/{encoded}?w={width}"
    if provider == "thumio":
        encoded = urllib.parse.quote(page_url, safe=":/?&=%#")
        return f"https://image.thum.io/get/width/{width}/{encoded}"
    raise ValueError(f"Unsupported provider: {provider}")


def fetch_page_text(url: str) -> str:
    result = subprocess.run(
        ["curl", "-L", "-sS", "--max-time", "60", url],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.stdout.strip():
        return result.stdout
    return ""


def validate_record(
    entry: Entry,
    match_mode: str,
    min_keyword_hit: int,
    global_deny_keywords: List[str],
) -> tuple[bool, str]:
    merged_exclude = list(dict.fromkeys([*entry.exclude_keywords, *global_deny_keywords]))
    if not entry.keywords and not merged_exclude:
        return True, "no validation rules"

    page_text = fetch_page_text(entry.page_url)
    if not page_text:
        return False, "cannot fetch page text for content validation"

    lowered = page_text.lower()
    blocked = [keyword for keyword in merged_exclude if keyword.lower() in lowered]
    if blocked:
        return False, f"exclude keywords found: {', '.join(blocked)}"

    if not entry.keywords:
        return True, "exclude-keyword validation passed"

    hits = [keyword for keyword in entry.keywords if keyword.lower() in lowered]
    hit_count = len(hits)
    total = len(entry.keywords)

    if match_mode == "all":
        if hit_count == total:
            return True, f"keyword validation passed (mode=all, hit={hit_count}/{total})"
        missing = [keyword for keyword in entry.keywords if keyword not in hits]
        return False, f"missing keywords: {', '.join(missing)} (mode=all, hit={hit_count}/{total})"

    if match_mode == "any":
        if hit_count >= 1:
            return True, f"keyword validation passed (mode=any, hit={hit_count}/{total})"
        return False, f"no keyword matched (mode=any, hit=0/{total})"

    threshold = max(1, min(min_keyword_hit, total))
    if hit_count >= threshold:
        return True, (
            f"keyword validation passed (mode=threshold, "
            f"hit={hit_count}/{total}, required>={threshold})"
        )
    return False, (
        f"insufficient keyword matches (mode=threshold, "
        f"hit={hit_count}/{total}, required>={threshold})"
    )


def download_image(url: str, path: pathlib.Path) -> None:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=40) as response:
            data = response.read()
        path.write_bytes(data)
        return
    except Exception:  # noqa: BLE001
        pass

    result = subprocess.run(
        ["curl", "-L", "-sS", url, "-o", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "curl download failed")


def parse_size(raw: str) -> Tuple[int, int]:
    value = raw.strip().lower()
    if "x" not in value:
        raise ValueError(f"Invalid size format: {raw}. Use WIDTHxHEIGHT, e.g. 1200x720.")
    width_str, height_str = value.split("x", 1)
    width = int(width_str.strip())
    height = int(height_str.strip())
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid size values: {raw}")
    return width, height


def anchor_to_xy(anchor: str) -> Tuple[float, float]:
    normalized = anchor.strip().lower().replace("_", "-")
    mapping = {
        "center": (0.5, 0.5),
        "top": (0.5, 0.0),
        "bottom": (0.5, 1.0),
        "left": (0.0, 0.5),
        "right": (1.0, 0.5),
        "top-left": (0.0, 0.0),
        "top-right": (1.0, 0.0),
        "bottom-left": (0.0, 1.0),
        "bottom-right": (1.0, 1.0),
    }
    if normalized in mapping:
        return mapping[normalized]
    return 0.5, 0.5


def apply_layout_crop(
    image_path: pathlib.Path,
    size: Tuple[int, int],
    mode: str,
    anchor: str,
) -> None:
    from PIL import Image

    target_w, target_h = size
    if mode not in {"cover", "contain"}:
        raise ValueError(f"Unsupported layout mode: {mode}")

    with Image.open(image_path) as source_image:
        image = source_image.convert("RGB")
        src_w, src_h = image.size
        if src_w <= 0 or src_h <= 0:
            raise ValueError(f"Invalid source image size: {image_path}")

        anchor_x, anchor_y = anchor_to_xy(anchor)

        if mode == "cover":
            scale = max(target_w / src_w, target_h / src_h)
            resized_w = max(1, int(round(src_w * scale)))
            resized_h = max(1, int(round(src_h * scale)))
            resized = image.resize((resized_w, resized_h), Image.Resampling.LANCZOS)

            max_left = max(0, resized_w - target_w)
            max_top = max(0, resized_h - target_h)
            left = int(round(max_left * anchor_x))
            top = int(round(max_top * anchor_y))
            right = min(resized_w, left + target_w)
            bottom = min(resized_h, top + target_h)
            cropped = resized.crop((left, top, right, bottom))
            if cropped.size != (target_w, target_h):
                cropped = cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
            cropped.save(image_path)
            return

        scale = min(target_w / src_w, target_h / src_h)
        resized_w = max(1, int(round(src_w * scale)))
        resized_h = max(1, int(round(src_h * scale)))
        resized = image.resize((resized_w, resized_h), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (target_w, target_h), color=(255, 255, 255))
        max_left = max(0, target_w - resized_w)
        max_top = max(0, target_h - resized_h)
        left = int(round(max_left * anchor_x))
        top = int(round(max_top * anchor_y))
        canvas.paste(resized, (left, top))
        canvas.save(image_path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate webpage screenshots with content audit and optional post-crop "
            "to news layout size."
        )
    )
    parser.add_argument(
        "--entry",
        action="append",
        required=True,
        help=(
            "label|source_id|source_name|page_url"
            "[|capture_opts][|keywords][|exclude_keywords][|layout_opts]"
        ),
    )
    parser.add_argument(
        "--provider",
        default="microlink",
        choices=["microlink", "mshots", "thumio"],
        help="Screenshot provider (default: microlink)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1400,
        help="Screenshot width request for provider (default: 1400)",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download screenshots to --out-dir. If omitted, emit external links only.",
    )
    parser.add_argument(
        "--out-dir",
        default="outputs/screenshots",
        help="Output directory for downloaded files.",
    )
    parser.add_argument(
        "--markdown-out",
        default="",
        help="Optional file path to save generated Markdown block.",
    )
    parser.add_argument(
        "--audit-report",
        default="",
        help="Optional JSON path for audit and processing report.",
    )
    parser.add_argument(
        "--strict-validation",
        action="store_true",
        help="Skip screenshot generation when content validation fails.",
    )
    parser.add_argument(
        "--match-mode",
        default="all",
        choices=["all", "any", "threshold"],
        help="Keyword match mode for content validation (default: all).",
    )
    parser.add_argument(
        "--min-keyword-hit",
        type=int,
        default=2,
        help="Minimum keyword hits when --match-mode=threshold (default: 2).",
    )
    parser.add_argument(
        "--audit-deny-keywords",
        default="blocked,access denied,verify you are human,captcha,unusual traffic",
        help="Global deny keywords for audit; comma-separated.",
    )
    parser.add_argument(
        "--layout-size",
        default="1200x720",
        help="Final image layout size WIDTHxHEIGHT for downloaded images (default: 1200x720).",
    )
    parser.add_argument(
        "--layout-mode",
        default="cover",
        choices=["cover", "contain"],
        help="Layout processing mode for downloaded images (default: cover).",
    )
    parser.add_argument(
        "--layout-anchor",
        default="center",
        help="Crop/placement anchor: center/top/bottom/left/right/top-left/... (default: center).",
    )
    args = parser.parse_args()

    records = [parse_entry(raw) for raw in args.entry]
    global_deny_keywords = parse_csv_keywords(args.audit_deny_keywords)
    out_dir = pathlib.Path(args.out_dir).resolve()
    if args.download:
        out_dir.mkdir(parents=True, exist_ok=True)

    lines: List[str] = []
    report: List[Dict[str, str]] = []
    for index, record in enumerate(records, start=1):
        entry_report: Dict[str, str] = {
            "index": str(index),
            "label": record.label,
            "page_url": record.page_url,
            "status": "pending",
        }
        is_valid, validation_msg = validate_record(
            entry=record,
            match_mode=args.match_mode,
            min_keyword_hit=args.min_keyword_hit,
            global_deny_keywords=global_deny_keywords,
        )
        entry_report["validation"] = validation_msg

        if not is_valid:
            print(
                f"[warn] validation mismatch for {record.page_url}: {validation_msg}",
                file=sys.stderr,
            )
            if args.strict_validation:
                entry_report["status"] = "skipped_validation"
                lines.append(
                    f"<!-- skipped: {record.label} (validation mismatch: {validation_msg}) -->"
                )
                lines.append("")
                report.append(entry_report)
                continue

        screenshot_url = build_screenshot_url(
            record.page_url,
            args.provider,
            args.width,
            record.capture_opts,
        )
        image_ref = screenshot_url
        layout_msg = ""

        if args.download:
            file_name = f"{index:02d}-{sanitize_filename(record.label)}.png"
            file_path = out_dir / file_name
            try:
                download_image(screenshot_url, file_path)

                size_raw = record.layout_opts.get("size", args.layout_size).strip()
                mode = record.layout_opts.get("mode", args.layout_mode).strip().lower()
                anchor = record.layout_opts.get("anchor", args.layout_anchor).strip().lower()
                if size_raw:
                    size = parse_size(size_raw)
                    apply_layout_crop(file_path, size=size, mode=mode, anchor=anchor)
                    layout_msg = f"排版裁剪：{size[0]}x{size[1]} ({mode}, anchor={anchor})"

                image_ref = str(file_path)
                entry_report["status"] = "ok_downloaded"
                entry_report["image_ref"] = image_ref
            except Exception as exc:  # noqa: BLE001
                print(
                    f"[warn] failed to download/process screenshot for {record.page_url}: {exc}",
                    file=sys.stderr,
                )
                entry_report["status"] = "download_or_layout_failed"
                entry_report["error"] = str(exc)
        else:
            entry_report["status"] = "ok_external"
            entry_report["image_ref"] = image_ref

        detail_text = validation_msg if not layout_msg else f"{validation_msg}；{layout_msg}"
        lines.append(f"![{record.label}]({image_ref})")
        lines.append(
            f"*图{index}：{record.label}（来源：{record.source_name}，"
            f"source_id：{record.source_id}，页面：[{record.page_url}]({record.page_url})，"
            f"内容校验：{detail_text}）*"
        )
        lines.append("")
        report.append(entry_report)

    output = "\n".join(lines).strip() + "\n"
    print(output)

    if args.markdown_out:
        markdown_path = pathlib.Path(args.markdown_out).resolve()
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        markdown_path.write_text(output, encoding="utf-8")
        print(f"[ok] markdown saved: {markdown_path}", file=sys.stderr)

    if args.audit_report:
        report_path = pathlib.Path(args.audit_report).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "strict_validation": args.strict_validation,
            "match_mode": args.match_mode,
            "min_keyword_hit": args.min_keyword_hit,
            "audit_deny_keywords": global_deny_keywords,
            "results": report,
        }
        report_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"[ok] audit report saved: {report_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
