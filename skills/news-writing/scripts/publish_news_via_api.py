#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Tuple


IMAGE_PATTERN = re.compile(r"!\[[^\]]*]\(([^)]+)\)")


def default_sites_file() -> pathlib.Path:
    skill_root = pathlib.Path(__file__).resolve().parents[1]
    return skill_root / "outputs" / "publishing" / "sites.json"


def join_url(base_url: str, route: str) -> str:
    return f"{base_url.rstrip('/')}/{route.lstrip('/')}"


def load_registry(path: pathlib.Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Sites file not found: {path}. "
            "Run manage_publish_sites.py init first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def find_site(data: Dict[str, Any], site_id: str) -> Dict[str, Any] | None:
    for site in data.get("sites", []):
        if site.get("site_id") == site_id:
            return site
    return None


def get_auth_headers(site: Dict[str, Any]) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    auth = site.get("auth", {}) or {}
    auth_type = auth.get("type", "none")

    if auth_type == "none":
        pass
    elif auth_type == "bearer":
        token_env = auth.get("token_env", "").strip()
        if not token_env:
            raise ValueError(f"Site {site.get('site_id')} uses bearer auth but token_env is empty.")
        token = os.getenv(token_env, "").strip()
        if not token:
            raise ValueError(f"Missing auth token env var: {token_env}")
        headers["Authorization"] = f"Bearer {token}"
    elif auth_type == "header":
        token_env = auth.get("token_env", "").strip()
        header_name = auth.get("header_name", "").strip()
        if not token_env or not header_name:
            raise ValueError(
                f"Site {site.get('site_id')} uses header auth but token_env/header_name is not configured."
            )
        token = os.getenv(token_env, "").strip()
        if not token:
            raise ValueError(f"Missing auth token env var: {token_env}")
        headers[header_name] = token
    else:
        raise ValueError(f"Unsupported auth type: {auth_type}")

    extra_headers = site.get("extra_headers", {}) or {}
    for key, value in extra_headers.items():
        headers[str(key)] = str(value)
    return headers


def request_json(url: str, method: str, headers: Dict[str, str], payload: Dict[str, Any] | None, timeout: int) -> Dict[str, Any]:
    request_headers = dict(headers)
    body_bytes: bytes | None = None
    if payload is not None:
        request_headers["Content-Type"] = "application/json"
        body_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url=url, method=method, headers=request_headers, data=body_bytes)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            if not raw:
                return {}
            return json.loads(raw)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} {exc.reason} for {method} {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        return request_json_via_curl(
            url=url,
            method=method,
            headers=headers,
            payload=payload,
            timeout=timeout,
            original_error=exc,
        )
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Non-JSON response for {method} {url}") from exc


def request_json_via_curl(
    url: str,
    method: str,
    headers: Dict[str, str],
    payload: Dict[str, Any] | None,
    timeout: int,
    original_error: Exception,
) -> Dict[str, Any]:
    marker = "__HTTP_STATUS__:"
    command: List[str] = [
        "curl",
        "-L",
        "-sS",
        "--max-time",
        str(timeout),
        "-X",
        method,
        url,
        "-w",
        f"\\n{marker}%{{http_code}}",
    ]
    for key, value in headers.items():
        command.extend(["-H", f"{key}: {value}"])
    if payload is not None:
        command.extend(["-H", "Content-Type: application/json"])
        command.extend(["--data", json.dumps(payload, ensure_ascii=False)])

    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            f"Network error for {method} {url}: {original_error}; "
            f"curl fallback failed: {result.stderr.strip()}"
        )

    output = result.stdout
    status_index = output.rfind(marker)
    if status_index == -1:
        raise RuntimeError(f"curl fallback missing status marker for {method} {url}")
    body = output[:status_index].strip()
    status_text = output[status_index + len(marker) :].strip()
    try:
        status_code = int(status_text)
    except ValueError as exc:
        raise RuntimeError(f"Invalid status code from curl fallback: {status_text}") from exc

    if status_code >= 400:
        raise RuntimeError(f"HTTP {status_code} for {method} {url}: {body}")
    if not body:
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Non-JSON response for {method} {url}: {body[:200]}") from exc


def parse_images(cli_images: List[str], content: str, extract_from_markdown: bool) -> List[str]:
    images: List[str] = []
    for chunk in cli_images:
        for item in chunk.split(","):
            value = item.strip()
            if value:
                images.append(value)
    if extract_from_markdown:
        images.extend(match.strip() for match in IMAGE_PATTERN.findall(content) if match.strip())
    deduped: List[str] = []
    seen = set()
    for image in images:
        if image not in seen:
            seen.add(image)
            deduped.append(image)
    return deduped


def resolve_community_id(
    site: Dict[str, Any],
    headers: Dict[str, str],
    timeout: int,
    community_id: str,
    community_name: str,
) -> Tuple[str, str]:
    if community_id:
        return community_id.strip(), ""

    if site.get("default_community_id"):
        if not community_name:
            return str(site["default_community_id"]).strip(), ""

    if not community_name:
        raise ValueError(
            "Missing community info. Provide --community-id or --community-name, "
            "or configure default_community_id in sites.json."
        )

    route = site.get("routes", {}).get("list_communities", "/communities")
    url = join_url(site["api_base_url"], route)
    response = request_json(url=url, method="GET", headers=headers, payload=None, timeout=timeout)
    communities = response.get("data", []) if isinstance(response, dict) else []
    if not isinstance(communities, list):
        raise ValueError("Invalid communities response format.")

    normalized_query = community_name.strip().lower()
    exact = [item for item in communities if str(item.get("name", "")).strip().lower() == normalized_query]
    if exact:
        match = exact[0]
        return str(match["id"]), str(match.get("name", ""))

    contains = [item for item in communities if normalized_query in str(item.get("name", "")).lower()]
    if len(contains) == 1:
        match = contains[0]
        return str(match["id"]), str(match.get("name", ""))
    if len(contains) > 1:
        names = ", ".join(str(item.get("name", "")) for item in contains)
        raise ValueError(f"Community name is ambiguous: {community_name}. Candidates: {names}")

    names = ", ".join(str(item.get("name", "")) for item in communities)
    raise ValueError(f"Community not found: {community_name}. Available: {names}")


def build_payload(
    title: str,
    author_name: str,
    community_id: str,
    content: str,
    images: List[str],
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "title": title.strip(),
        "community_id": community_id.strip(),
        "author_name": author_name.strip(),
    }
    if content.strip():
        payload["content"] = content
    if images:
        payload["images"] = images
    return payload


def parse_content(args: argparse.Namespace) -> str:
    if args.content_file:
        path = pathlib.Path(args.content_file).resolve()
        return path.read_text(encoding="utf-8")
    return args.content or ""


def print_publish_receipt(
    site: Dict[str, Any],
    response: Dict[str, Any],
    payload: Dict[str, Any],
    matched_community_name: str,
) -> None:
    post_id = ""
    if isinstance(response, dict):
        data = response.get("data", {})
        if isinstance(data, dict):
            post_id = str(data.get("id", "")).strip()

    web_base_url = str(site.get("web_base_url", "")).rstrip("/")
    post_url = f"{web_base_url}/post/{post_id}" if web_base_url and post_id else ""

    receipt = {
        "site_id": site.get("site_id"),
        "post_id": post_id,
        "post_url": post_url,
        "community_id": payload.get("community_id"),
        "community_name": matched_community_name,
        "title": payload.get("title"),
        "author_name": payload.get("author_name"),
        "images_count": len(payload.get("images", [])) if isinstance(payload.get("images", []), list) else 0,
        "api_response": response,
    }
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Publish news content to configured website by API.")
    parser.add_argument(
        "--sites-file",
        default=str(default_sites_file()),
        help="Path to site registry JSON file.",
    )
    parser.add_argument("--site-id", default="", help="Target site_id. Defaults to registry default_site_id.")
    parser.add_argument("--title", required=True, help="Post title.")
    parser.add_argument("--author-name", default="", help="Author display name.")
    parser.add_argument("--community-id", default="", help="Community UUID.")
    parser.add_argument("--community-name", default="", help="Community name (auto resolve to ID).")

    content_group = parser.add_mutually_exclusive_group(required=True)
    content_group.add_argument("--content", help="Post content text.")
    content_group.add_argument("--content-file", help="Path to markdown/text file for post content.")

    parser.add_argument(
        "--images",
        action="append",
        default=[],
        help="Image URLs, can repeat or pass comma-separated values.",
    )
    parser.add_argument(
        "--extract-images-from-markdown",
        action="store_true",
        help="Extract image links from markdown content and append into payload.images.",
    )
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout seconds.")
    parser.add_argument("--dry-run", action="store_true", help="Resolve and print payload without posting.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        registry = load_registry(pathlib.Path(args.sites_file).resolve())
        site_id = args.site_id or registry.get("default_site_id", "")
        if not site_id:
            raise ValueError("No site_id provided and default_site_id is empty.")
        site = find_site(registry, site_id)
        if not site:
            raise ValueError(f"Site not found: {site_id}")
        if not site.get("enabled", True):
            raise ValueError(f"Site is disabled: {site_id}")

        author_name = args.author_name.strip() or str(site.get("default_author", "")).strip()
        if not author_name:
            author_name = "News Bot"

        content = parse_content(args)
        images = parse_images(args.images, content, args.extract_images_from_markdown)
        headers = get_auth_headers(site)
        community_id, matched_community_name = resolve_community_id(
            site=site,
            headers=headers,
            timeout=args.timeout,
            community_id=args.community_id,
            community_name=args.community_name,
        )
        payload = build_payload(
            title=args.title,
            author_name=author_name,
            community_id=community_id,
            content=content,
            images=images,
        )

        create_post_route = site.get("routes", {}).get("create_post", "/posts")
        create_post_url = join_url(site["api_base_url"], create_post_route)

        if args.dry_run:
            preview = {
                "site_id": site.get("site_id"),
                "create_post_url": create_post_url,
                "community_match_name": matched_community_name,
                "payload": payload,
            }
            print(json.dumps(preview, ensure_ascii=False, indent=2))
            return 0

        response = request_json(
            url=create_post_url,
            method="POST",
            headers=headers,
            payload=payload,
            timeout=args.timeout,
        )
        print_publish_receipt(
            site=site,
            response=response,
            payload=payload,
            matched_community_name=matched_community_name,
        )
        return 0
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
