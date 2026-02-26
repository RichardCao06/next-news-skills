#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any, Dict, List


def default_sites_file() -> pathlib.Path:
    skill_root = pathlib.Path(__file__).resolve().parents[1]
    return skill_root / "outputs" / "publishing" / "sites.json"


def default_registry() -> Dict[str, Any]:
    return {
        "schema_version": 1,
        "default_site_id": "lca-echo",
        "sites": [
            {
                "site_id": "lca-echo",
                "display_name": "LCA Echo",
                "web_base_url": "https://lca-echo.lovable.app",
                "docs_url": "https://lca-echo.lovable.app/api-docs",
                "api_base_url": "https://meezfvpwfzzpibkecrvj.supabase.co/functions/v1/api",
                "routes": {
                    "create_post": "/posts",
                    "list_communities": "/communities",
                },
                "auth": {
                    "type": "none",
                    "token_env": "",
                    "header_name": "Authorization",
                },
                "extra_headers": {},
                "default_author": "LCAEcho Bot",
                "default_community_id": "a1000000-0000-0000-0000-000000000005",
                "enabled": True,
                "notes": "默认站点，来自公开 API 文档。",
            }
        ],
    }


def normalize_base_url(value: str) -> str:
    return value.strip().rstrip("/")


def normalize_path(value: str) -> str:
    value = value.strip()
    if not value:
        return "/"
    if not value.startswith("/"):
        value = "/" + value
    return value


def parse_headers(header_items: List[str]) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    for item in header_items:
        if "=" not in item:
            raise ValueError(f"Invalid --extra-header: {item}. Use KEY=VALUE.")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise ValueError(f"Invalid --extra-header: {item}. Empty key.")
        headers[key] = value
    return headers


def load_registry(path: pathlib.Path, auto_init: bool = False) -> Dict[str, Any]:
    if not path.exists():
        if auto_init:
            data = default_registry()
            save_registry(path, data)
            return data
        raise FileNotFoundError(f"Sites file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_registry(path: pathlib.Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_site(data: Dict[str, Any], site_id: str) -> Dict[str, Any] | None:
    for site in data.get("sites", []):
        if site.get("site_id") == site_id:
            return site
    return None


def command_init(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.sites_file).resolve()
    if path.exists() and not args.force:
        print(f"[skip] already exists: {path}")
        return 0
    save_registry(path, default_registry())
    print(f"[ok] initialized: {path}")
    return 0


def command_list(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.sites_file).resolve()
    data = load_registry(path, auto_init=args.auto_init)
    default_site_id = data.get("default_site_id", "")
    sites = data.get("sites", [])
    if not sites:
        print("[info] no sites configured")
        return 0
    print("site_id\tdefault\tenabled\tdisplay_name\tapi_base_url")
    for site in sites:
        marker = "*" if site.get("site_id") == default_site_id else ""
        enabled = "yes" if site.get("enabled", True) else "no"
        print(
            f"{site.get('site_id','')}\t{marker}\t{enabled}\t"
            f"{site.get('display_name','')}\t{site.get('api_base_url','')}"
        )
    return 0


def command_show(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.sites_file).resolve()
    data = load_registry(path, auto_init=args.auto_init)
    site = find_site(data, args.site_id)
    if not site:
        print(f"[error] site not found: {args.site_id}", file=sys.stderr)
        return 1
    print(json.dumps(site, ensure_ascii=False, indent=2))
    return 0


def command_set_default(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.sites_file).resolve()
    data = load_registry(path, auto_init=args.auto_init)
    site = find_site(data, args.site_id)
    if not site:
        print(f"[error] site not found: {args.site_id}", file=sys.stderr)
        return 1
    data["default_site_id"] = args.site_id
    save_registry(path, data)
    print(f"[ok] default site set to: {args.site_id}")
    return 0


def command_remove(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.sites_file).resolve()
    data = load_registry(path, auto_init=args.auto_init)
    sites = data.get("sites", [])
    kept = [site for site in sites if site.get("site_id") != args.site_id]
    if len(kept) == len(sites):
        print(f"[error] site not found: {args.site_id}", file=sys.stderr)
        return 1
    data["sites"] = kept
    if data.get("default_site_id") == args.site_id:
        data["default_site_id"] = kept[0]["site_id"] if kept else ""
    save_registry(path, data)
    print(f"[ok] removed site: {args.site_id}")
    return 0


def build_site_from_args(args: argparse.Namespace, current: Dict[str, Any] | None = None) -> Dict[str, Any]:
    site: Dict[str, Any] = dict(current or {})
    if not current:
        site["site_id"] = args.site_id

    if args.display_name is not None:
        site["display_name"] = args.display_name.strip()
    if args.web_base_url is not None:
        site["web_base_url"] = normalize_base_url(args.web_base_url)
    if args.docs_url is not None:
        site["docs_url"] = args.docs_url.strip()
    if args.api_base_url is not None:
        site["api_base_url"] = normalize_base_url(args.api_base_url)
    if args.default_author is not None:
        site["default_author"] = args.default_author.strip()
    if args.default_community_id is not None:
        site["default_community_id"] = args.default_community_id.strip()
    if args.notes is not None:
        site["notes"] = args.notes
    if args.enabled is not None:
        site["enabled"] = args.enabled

    routes = dict(site.get("routes", {}))
    if args.create_post_path is not None:
        routes["create_post"] = normalize_path(args.create_post_path)
    if args.list_communities_path is not None:
        routes["list_communities"] = normalize_path(args.list_communities_path)
    site["routes"] = routes

    auth = dict(site.get("auth", {}))
    if args.auth_type is not None:
        auth["type"] = args.auth_type
    if args.auth_token_env is not None:
        auth["token_env"] = args.auth_token_env
    if args.auth_header_name is not None:
        auth["header_name"] = args.auth_header_name
    site["auth"] = auth

    if args.extra_header:
        site["extra_headers"] = parse_headers(args.extra_header)
    elif "extra_headers" not in site:
        site["extra_headers"] = {}

    return site


def validate_site(site: Dict[str, Any]) -> None:
    required_fields = ["site_id", "display_name", "api_base_url"]
    for field in required_fields:
        if not site.get(field):
            raise ValueError(f"Missing required site field: {field}")
    if "routes" not in site:
        raise ValueError("Missing routes")
    if not site["routes"].get("create_post"):
        raise ValueError("Missing route: routes.create_post")
    if not site["routes"].get("list_communities"):
        raise ValueError("Missing route: routes.list_communities")
    auth_type = site.get("auth", {}).get("type", "none")
    if auth_type not in {"none", "bearer", "header"}:
        raise ValueError(f"Unsupported auth type: {auth_type}")


def command_add(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.sites_file).resolve()
    data = load_registry(path, auto_init=args.auto_init)
    if find_site(data, args.site_id):
        print(f"[error] site already exists: {args.site_id}", file=sys.stderr)
        return 1
    site = build_site_from_args(args)
    validate_site(site)
    data.setdefault("sites", []).append(site)
    if args.make_default:
        data["default_site_id"] = args.site_id
    save_registry(path, data)
    print(f"[ok] added site: {args.site_id}")
    return 0


def command_update(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.sites_file).resolve()
    data = load_registry(path, auto_init=args.auto_init)
    site = find_site(data, args.site_id)
    if not site:
        print(f"[error] site not found: {args.site_id}", file=sys.stderr)
        return 1
    updated = build_site_from_args(args, current=site)
    validate_site(updated)
    site.clear()
    site.update(updated)
    if args.make_default:
        data["default_site_id"] = args.site_id
    save_registry(path, data)
    print(f"[ok] updated site: {args.site_id}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage publish website registry for news-writing skill.")
    parser.add_argument(
        "--sites-file",
        default=str(default_sites_file()),
        help="Path to site registry JSON file.",
    )
    parser.add_argument(
        "--auto-init",
        action="store_true",
        help="Auto create default registry when --sites-file does not exist.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize default site registry.")
    init_parser.add_argument("--force", action="store_true", help="Overwrite if file already exists.")
    init_parser.set_defaults(func=command_init)

    list_parser = subparsers.add_parser("list", help="List configured sites.")
    list_parser.set_defaults(func=command_list)

    show_parser = subparsers.add_parser("show", help="Show a site config as JSON.")
    show_parser.add_argument("--site-id", required=True)
    show_parser.set_defaults(func=command_show)

    default_parser = subparsers.add_parser("set-default", help="Set default publish site.")
    default_parser.add_argument("--site-id", required=True)
    default_parser.set_defaults(func=command_set_default)

    remove_parser = subparsers.add_parser("remove", help="Remove a site.")
    remove_parser.add_argument("--site-id", required=True)
    remove_parser.set_defaults(func=command_remove)

    add_parser = subparsers.add_parser("add", help="Add a site.")
    add_parser.add_argument("--site-id", required=True)
    add_parser.add_argument("--display-name", required=True)
    add_parser.add_argument("--web-base-url", default="")
    add_parser.add_argument("--docs-url", default="")
    add_parser.add_argument("--api-base-url", required=True)
    add_parser.add_argument("--create-post-path", default="/posts")
    add_parser.add_argument("--list-communities-path", default="/communities")
    add_parser.add_argument("--auth-type", choices=["none", "bearer", "header"], default="none")
    add_parser.add_argument("--auth-token-env", default="")
    add_parser.add_argument("--auth-header-name", default="Authorization")
    add_parser.add_argument("--extra-header", action="append", default=[])
    add_parser.add_argument("--default-author", default="News Bot")
    add_parser.add_argument("--default-community-id", default="")
    add_parser.add_argument("--notes", default="")
    add_parser.add_argument(
        "--enabled",
        type=lambda value: value.lower() in {"1", "true", "yes", "y"},
        default=True,
    )
    add_parser.add_argument("--make-default", action="store_true")
    add_parser.set_defaults(func=command_add)

    update_parser = subparsers.add_parser("update", help="Update a site.")
    update_parser.add_argument("--site-id", required=True)
    update_parser.add_argument("--display-name")
    update_parser.add_argument("--web-base-url")
    update_parser.add_argument("--docs-url")
    update_parser.add_argument("--api-base-url")
    update_parser.add_argument("--create-post-path")
    update_parser.add_argument("--list-communities-path")
    update_parser.add_argument("--auth-type", choices=["none", "bearer", "header"])
    update_parser.add_argument("--auth-token-env")
    update_parser.add_argument("--auth-header-name")
    update_parser.add_argument("--extra-header", action="append", default=[])
    update_parser.add_argument("--default-author")
    update_parser.add_argument("--default-community-id")
    update_parser.add_argument("--notes")
    update_parser.add_argument(
        "--enabled",
        type=lambda value: value.lower() in {"1", "true", "yes", "y"},
    )
    update_parser.add_argument("--make-default", action="store_true")
    update_parser.set_defaults(func=command_update)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, FileNotFoundError) as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
