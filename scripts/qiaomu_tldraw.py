#!/usr/bin/env python3
"""Official-first, zero-third-party-dependency tools for qiaomu-tldraw-skill.

The script uses only the Python standard library. SDK scaffolding invokes the
official create-tldraw npm package through npx. Documentation is downloaded
only from tldraw.dev, cached locally, hashed, and searched offline.
"""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OFFICIAL_DOCS = {
    "index": "https://tldraw.dev/llms.txt",
    "docs": "https://tldraw.dev/llms-docs.txt",
    "examples": "https://tldraw.dev/llms-examples.txt",
    "releases": "https://tldraw.dev/llms-releases.txt",
    "full": "https://tldraw.dev/llms-full.txt",
}
OFFICIAL_WEB_HOSTS = {"tldraw.dev", "registry.npmjs.org"}
OFFICIAL_PACKAGE = "create-tldraw"
FALLBACK_TEMPLATES = [
    "basic",
    "multiplayer",
    "agent",
    "workflow",
    "chat",
    "image-pipeline",
    "branching-chat",
    "shader",
]
USER_AGENT = "qiaomu-tldraw-skill/1.1 (+https://github.com/joeseesun/qiaomu-tldraw-skill)"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def cache_root() -> Path:
    configured = os.environ.get("QIAOMU_TLDRAW_CACHE")
    if configured:
        return Path(configured).expanduser()
    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "qiaomu-tldraw-skill"


def config_candidates() -> list[Path]:
    if sys.platform == "darwin":
        return [Path.home() / "Library/Application Support/tldraw/server.json"]
    if os.name == "nt":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
        return [base / "tldraw/server.json"]
    return [Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "tldraw/server.json"]


def skill_candidates() -> list[Path]:
    return [
        Path.home() / "skills/tldraw-offline",
        Path.home() / ".agents/skills/tldraw-offline",
        Path.home() / ".codex/skills/tldraw-offline",
        Path.home() / ".claude/skills/tldraw-offline",
    ]


def offline_app_info() -> dict[str, Any]:
    """Return best-effort metadata for an installed official offline app."""
    candidates: list[Path] = []
    if sys.platform == "darwin":
        candidates = [
            Path("/Applications/tldraw offline.app"),
            Path.home() / "Applications/tldraw offline.app",
        ]
    for app in candidates:
        plist = app / "Contents/Info.plist"
        if not plist.is_file():
            continue
        metadata: dict[str, str | None] = {}
        plutil = shutil.which("plutil")
        for output_key, plist_key in [
            ("bundle_id", "CFBundleIdentifier"),
            ("version", "CFBundleShortVersionString"),
            ("build", "CFBundleVersion"),
        ]:
            value = None
            if plutil:
                completed = subprocess.run(
                    [plutil, "-extract", plist_key, "raw", "-o", "-", str(plist)],
                    text=True,
                    capture_output=True,
                    check=False,
                    timeout=5,
                )
                if completed.returncode == 0:
                    value = completed.stdout.strip() or None
            metadata[output_key] = value
        return {
            "installed": True,
            "path": str(app),
            **metadata,
        }
    return {"installed": False}


def ensure_official_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in OFFICIAL_WEB_HOSTS:
        raise ValueError(f"refusing non-official URL: {url}")


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    ensure_official_url(url)
    content = bytearray()
    expected_total: int | None = None
    last_error: Exception | None = None
    for _ in range(8):
        headers = {"user-agent": USER_AGENT, "accept-encoding": "identity", "connection": "close"}
        if content:
            headers["range"] = f"bytes={len(content)}-"
        request = urllib.request.Request(
            url,
            headers=headers,
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                status = getattr(response, "status", 200)
                content_range = response.headers.get("content-range")
                if content and status != 206:
                    content.clear()
                if content_range:
                    match = re.search(r"/(\d+)$", content_range)
                    expected_total = int(match.group(1)) if match else None
                elif status == 200 and response.headers.get("content-length"):
                    expected_total = int(response.headers["content-length"])
                try:
                    content.extend(response.read())
                except http.client.IncompleteRead as exc:
                    content.extend(exc.partial)
                    last_error = exc
                    continue
                if expected_total is None or len(content) == expected_total:
                    return bytes(content)
                if len(content) > expected_total:
                    raise IOError(f"response exceeded expected size for {url}: got {len(content)}, expected {expected_total}")
                last_error = IOError(f"incomplete response from {url}: got {len(content)}, expected {expected_total}")
        except (OSError, http.client.IncompleteRead, urllib.error.URLError) as exc:
            last_error = exc
    raise urllib.error.URLError(f"failed to download complete official response after range retries: {last_error}")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    path.write_text(rendered, encoding="utf-8")


def load_runtime() -> tuple[Path, dict[str, Any]]:
    for path in config_candidates():
        if path.is_file():
            payload = json.loads(path.read_text(encoding="utf-8"))
            port = payload.get("port")
            token = payload.get("token")
            if not isinstance(port, int) or not 1 <= port <= 65535:
                raise RuntimeError(f"invalid local port in {path}")
            if not isinstance(token, str) or not token:
                raise RuntimeError(f"missing runtime token in {path}")
            return path, payload
    raise FileNotFoundError("tldraw server.json not found; start tldraw offline and install Agent Setup")


def api_request(method: str, path: str, body: dict[str, Any] | None = None) -> Any:
    _, runtime = load_runtime()
    url = f"http://127.0.0.1:{runtime['port']}{path}"
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"authorization": f"Bearer {runtime['token']}"}
    if data is not None:
        headers["content-type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def offline_readme() -> str:
    _, runtime = load_runtime()
    url = f"http://127.0.0.1:{runtime['port']}/readme"
    request = urllib.request.Request(url, headers={"user-agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=5) as response:
        return response.read().decode("utf-8")


def doctor() -> dict[str, Any]:
    installed = []
    for root in skill_candidates():
        if (root / "SKILL.md").is_file():
            installed.append({"path": str(root), "tq": (root / "tq").is_file()})
    result: dict[str, Any] = {
        "ok": False,
        "platform": platform.system(),
        "python": platform.python_version(),
        "node": command_version("node", "--version"),
        "npx": command_version("npx", "--version"),
        "optional_official_agent_setup": installed,
        "official_offline_app": offline_app_info(),
        "runtime_config": None,
        "server": None,
        "third_party_python_dependencies": [],
    }
    try:
        config, runtime = load_runtime()
        result["runtime_config"] = {"path": str(config), "port": runtime["port"], "token": "<redacted>"}
        probe = api_request(
            "POST",
            "/api/search",
            {"code": "return {docs:(await api.getDocs()).length, recipes:Object.keys(api.recipes).length, helpers:api.helperCount}"},
        )
        result["server"] = probe.get("result", probe)
        result["ok"] = bool(probe.get("success"))
    except (OSError, RuntimeError, ValueError, urllib.error.URLError) as exc:
        result["error"] = str(exc)
    return result


def command_version(command: str, flag: str) -> str | None:
    executable = shutil.which(command)
    if not executable:
        return None
    completed = subprocess.run([executable, flag], text=True, capture_output=True, check=False, timeout=10)
    output = (completed.stdout or completed.stderr).strip()
    return output.splitlines()[0] if output else None


def npm_package_info(requested: str = "latest") -> dict[str, Any]:
    metadata = json.loads(fetch_bytes("https://registry.npmjs.org/create-tldraw").decode("utf-8"))
    dist_tags = metadata.get("dist-tags", {})
    resolved = dist_tags.get(requested, requested)
    version = metadata.get("versions", {}).get(resolved)
    if not isinstance(version, dict):
        raise ValueError(f"create-tldraw version or dist-tag not found: {requested}")
    dist = version.get("dist", {}) if isinstance(version.get("dist"), dict) else {}
    return {
        "name": version.get("name"),
        "requested": requested,
        "version": version.get("version"),
        "engines": version.get("engines", {}),
        "license": version.get("license"),
        "bin": version.get("bin"),
        "repository": version.get("repository"),
        "dist_tags": dist_tags,
        "tarball": dist.get("tarball"),
        "integrity": dist.get("integrity"),
        "registry": "https://registry.npmjs.org/",
    }


def safe_cli_version(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value):
        raise ValueError(f"invalid create-tldraw version or tag: {value}")
    return value


def cli_command(version: str, *args: str) -> list[str]:
    npx = shutil.which("npx")
    if not npx:
        raise FileNotFoundError("npx not found; install a Node.js version supported by create-tldraw")
    return [
        npx,
        "--yes",
        "--registry=https://registry.npmjs.org",
        f"{OFFICIAL_PACKAGE}@{safe_cli_version(version)}",
        *args,
    ]


def cli_help(version: str) -> str:
    completed = subprocess.run(
        cli_command(version, "--help"),
        text=True,
        capture_output=True,
        check=False,
        timeout=120,
    )
    if completed.returncode != 0:
        raise RuntimeError((completed.stderr or completed.stdout).strip() or "create-tldraw --help failed")
    return completed.stdout


def parse_templates(help_text: str) -> list[dict[str, str]]:
    templates = []
    in_templates = False
    for raw in help_text.splitlines():
        line = re.sub(r"\x1b\[[0-9;]*m", "", raw)
        if line.strip() == "Available starter kits:":
            in_templates = True
            continue
        if not in_templates:
            continue
        match = re.match(r"\s*[•*]\s+([a-z0-9-]+)\s+(.*)$", line, re.I)
        if match:
            templates.append({"id": match.group(1), "description": match.group(2).strip()})
        elif templates and not line.strip():
            break
    return templates


def official_info(version: str = "latest", docs_manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    package = npm_package_info(version)
    help_text = cli_help(version)
    templates = parse_templates(help_text)
    public_docs_manifest = None
    if docs_manifest:
        public_docs_manifest = dict(docs_manifest)
        public_docs_manifest["cache_dir"] = "<user-cache>/qiaomu-tldraw-skill/official-docs"
    return {
        "generated_at": now_iso(),
        "official_only": True,
        "python_runtime_dependencies": [],
        "create_tldraw": package,
        "templates": templates or [{"id": item, "description": "fallback; refresh cli-help"} for item in FALLBACK_TEMPLATES],
        "documentation": OFFICIAL_DOCS,
        "documentation_cache": public_docs_manifest,
        "source_of_truth": {
            "sdk_repo": "https://github.com/tldraw/tldraw",
            "offline_repo": "https://github.com/tldraw/tldraw-offline",
            "docs": "https://tldraw.dev/docs/llm-docs",
            "license": "https://tldraw.dev/community/license",
        },
    }


def docs_sync(bundles: list[str], destination: Path) -> dict[str, Any]:
    destination.mkdir(parents=True, exist_ok=True)
    records = []
    for bundle in bundles:
        url = OFFICIAL_DOCS[bundle]
        content = fetch_bytes(url, timeout=120)
        target = destination / f"llms-{bundle}.txt"
        with tempfile.NamedTemporaryFile(dir=destination, prefix=f".{target.name}.", delete=False) as handle:
            handle.write(content)
            temporary = Path(handle.name)
        temporary.replace(target)
        records.append(
            {
                "bundle": bundle,
                "url": url,
                "file": target.name,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    manifest = {
        "generated_at": now_iso(),
        "official_hosts": sorted(OFFICIAL_WEB_HOSTS),
        "cache_dir": str(destination),
        "bundles": records,
    }
    write_json(destination / "manifest.json", manifest)
    return manifest


def split_sections(text: str) -> list[tuple[int, str, str]]:
    lines = text.splitlines()
    sections: list[tuple[int, str, str]] = []
    start = 0
    heading = "Document start"
    for index, line in enumerate(lines):
        if re.match(r"^#{1,4}\s+", line):
            if index > start:
                sections.append((start + 1, heading, "\n".join(lines[start:index]).strip()))
            start = index
            heading = re.sub(r"^#{1,4}\s+", "", line).strip()
    sections.append((start + 1, heading, "\n".join(lines[start:]).strip()))
    return [section for section in sections if section[2]]


def docs_search(query: str, bundle: str, destination: Path, limit: int) -> dict[str, Any]:
    target = destination / f"llms-{bundle}.txt"
    if not target.is_file():
        docs_sync([bundle], destination)
    text = target.read_text(encoding="utf-8")
    terms = [term.casefold() for term in re.findall(r"[\w.-]+", query, re.UNICODE) if term]
    if not terms:
        raise ValueError("search query must contain at least one word")
    matches = []
    for line, heading, body in split_sections(text):
        haystack = f"{heading}\n{body}".casefold()
        counts = [haystack.count(term) for term in terms]
        if not all(counts):
            continue
        score = sum(counts) + sum(2 for term in terms if term in heading.casefold())
        excerpt = re.sub(r"\s+", " ", body)[:900]
        matches.append({"heading": heading, "line": line, "score": score, "excerpt": excerpt})
    matches.sort(key=lambda item: (-item["score"], item["line"]))
    return {
        "query": query,
        "bundle": bundle,
        "source": OFFICIAL_DOCS[bundle],
        "cache": str(target),
        "results": matches[:limit],
    }


def project_info(directory: Path) -> dict[str, Any]:
    root = directory.expanduser().resolve()
    package_path = root / "package.json"
    if not package_path.is_file():
        raise FileNotFoundError(f"package.json not found: {package_path}")
    package = json.loads(package_path.read_text(encoding="utf-8"))
    manager = "npm"
    for lockfile, name in [
        ("pnpm-lock.yaml", "pnpm"),
        ("yarn.lock", "yarn"),
        ("bun.lock", "bun"),
        ("bun.lockb", "bun"),
        ("package-lock.json", "npm"),
    ]:
        if (root / lockfile).exists():
            manager = name
            break
    dependencies = {}
    for bucket in ("dependencies", "devDependencies", "peerDependencies"):
        for name, value in package.get(bucket, {}).items():
            if name == "tldraw" or name.startswith("@tldraw/"):
                dependencies[name] = {"range": value, "bucket": bucket}
    return {
        "root": str(root),
        "name": package.get("name"),
        "package_manager": manager,
        "tldraw_dependencies": dependencies,
        "scripts": package.get("scripts", {}),
        "license": package.get("license"),
    }


def scaffold(directory: Path, template: str, version: str, telemetry: bool, dry_run: bool) -> dict[str, Any]:
    target = directory.expanduser().resolve()
    if target.exists() and any(target.iterdir()):
        raise FileExistsError(f"target directory is not empty: {target}")
    if not re.fullmatch(r"[a-z0-9-]+", template):
        raise ValueError(f"invalid template id: {template}")
    command = cli_command(version, str(target), "--template", template)
    if not telemetry:
        command.append("--no-telemetry")
    display = [Path(command[0]).name, *command[1:]]
    if dry_run:
        return {"dry_run": True, "command": display, "target": str(target)}
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"create-tldraw exited with code {completed.returncode}")
    return {"dry_run": False, "command": display, "target": str(target), "project": project_info(target)}


def emit(payload: Any, output: str | None = None) -> None:
    if output:
        write_json(Path(output), payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Operate tldraw offline and the official tldraw CLI/docs with Python stdlib only."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    doctor_parser = sub.add_parser("doctor", help="Check official offline skill, local API, Node, and npx.")
    doctor_parser.add_argument("--json", action="store_true", help="Compatibility flag; output is always JSON.")
    sub.add_parser("list", help="List open tldraw offline documents (read-only).")
    sub.add_parser("offline-readme", help="Print the running app's official local Canvas API documentation.")
    recipe = sub.add_parser("recipe", help="Read one live official Canvas API recipe.")
    recipe.add_argument("id", help="Recipe id, e.g. custom-shape-config-js.")

    info = sub.add_parser("official-info", help="Resolve official CLI metadata, templates, docs, and sources.")
    info.add_argument("--version", default="latest", help="create-tldraw version or dist-tag.")
    info.add_argument("--sync-docs", action="store_true", help="Also cache and hash all five official LLM bundles.")
    info.add_argument("--cache-dir", type=Path, default=cache_root() / "official-docs")
    info.add_argument("--output", help="Optional JSON evidence path.")

    help_parser = sub.add_parser("cli-help", help="Print the current official create-tldraw help.")
    help_parser.add_argument("--version", default="latest")

    scaffold_parser = sub.add_parser("scaffold", help="Create a project with the official create-tldraw CLI.")
    scaffold_parser.add_argument("directory")
    scaffold_parser.add_argument("--template", default="basic")
    scaffold_parser.add_argument("--version", default="latest")
    scaffold_parser.add_argument("--telemetry", action="store_true", help="Allow official CLI telemetry; disabled by default.")
    scaffold_parser.add_argument("--dry-run", action="store_true")

    sync = sub.add_parser("docs-sync", help="Cache official LLM-friendly tldraw documentation.")
    sync.add_argument("--bundle", action="append", choices=sorted(OFFICIAL_DOCS), dest="bundles")
    sync.add_argument("--cache-dir", type=Path, default=cache_root() / "official-docs")
    sync.add_argument("--output", help="Optional JSON evidence path.")

    search = sub.add_parser("docs-search", help="Search cached official documentation offline.")
    search.add_argument("query")
    search.add_argument("--bundle", choices=sorted(OFFICIAL_DOCS), default="docs")
    search.add_argument("--cache-dir", type=Path, default=cache_root() / "official-docs")
    search.add_argument("--limit", type=int, default=8)

    project = sub.add_parser("project-info", help="Inspect package manager, scripts, and tldraw versions.")
    project.add_argument("directory", nargs="?", default=".")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == "doctor":
            payload = doctor()
            emit(payload)
            if not payload.get("ok"):
                raise SystemExit(2)
        elif args.command == "list":
            emit(api_request("POST", "/api/search", {"code": "return await api.getDocs()"}))
        elif args.command == "offline-readme":
            print(offline_readme(), end="")
        elif args.command == "recipe":
            code = "return api.recipes[" + json.dumps(args.id) + "] ?? null"
            emit(api_request("POST", "/api/search", {"code": code}))
        elif args.command == "official-info":
            docs_manifest = None
            if args.sync_docs:
                docs_manifest = docs_sync(["index", "docs", "examples", "releases", "full"], args.cache_dir.expanduser())
            emit(official_info(args.version, docs_manifest), args.output)
        elif args.command == "cli-help":
            print(cli_help(args.version), end="")
        elif args.command == "scaffold":
            emit(scaffold(Path(args.directory), args.template, args.version, args.telemetry, args.dry_run))
        elif args.command == "docs-sync":
            bundles = args.bundles or ["index", "docs", "examples", "releases"]
            emit(docs_sync(bundles, args.cache_dir.expanduser()), args.output)
        elif args.command == "docs-search":
            emit(docs_search(args.query, args.bundle, args.cache_dir.expanduser(), max(1, args.limit)))
        elif args.command == "project-info":
            emit(project_info(Path(args.directory)))
    except (FileNotFoundError, FileExistsError, RuntimeError, ValueError, urllib.error.URLError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
