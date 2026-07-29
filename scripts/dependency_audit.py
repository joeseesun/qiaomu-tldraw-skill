#!/usr/bin/env python3
"""Audit qiaomu-tldraw-skill's zero-extra-third-party dependency contract."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any


FORBIDDEN_RUNTIME_REFERENCES = [
    "Zluowa/tldraw-ai-drawing-skills",
    "tldraw-create",
    "tldraw-recreate",
    "@kitschpatrol/tldraw-cli",
]
OFFICIAL_NETWORK_HOSTS = ["tldraw.dev", "registry.npmjs.org", "127.0.0.1"]


def imports_for(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    return imports


def has_shell_true(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for keyword in node.keywords:
            if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                return True
    return False


def audit(root: Path) -> dict[str, Any]:
    root = root.resolve()
    local_modules = {path.stem for path in (root / "scripts").glob("*.py")}
    allowed_modules = set(sys.stdlib_module_names) | local_modules | {"__future__"}
    python_files = sorted((root / "scripts").glob("*.py"))
    file_imports = {}
    nonstdlib = {}
    shell_true = []
    for path in python_files:
        imports = sorted(imports_for(path))
        relative = str(path.relative_to(root))
        file_imports[relative] = imports
        unexpected = sorted(set(imports) - allowed_modules)
        if unexpected:
            nonstdlib[relative] = unexpected
        if has_shell_true(path):
            shell_true.append(relative)

    public_paths = [root / "SKILL.md", root / "README.md", *sorted((root / "references").glob("*.md"))]
    public_text = "\n".join(path.read_text(encoding="utf-8") for path in public_paths if path.is_file())
    forbidden = [value for value in FORBIDDEN_RUNTIME_REFERENCES if value.casefold() in public_text.casefold()]

    runtime_source = (root / "scripts/qiaomu_tldraw.py").read_text(encoding="utf-8")
    discovered_urls = sorted(set(re.findall(r"https?://[^\s\"')]+", runtime_source)))
    fetched_hosts = []
    host_match = re.search(r"OFFICIAL_WEB_HOSTS\s*=\s*\{([^}]+)\}", runtime_source)
    if host_match:
        fetched_hosts = sorted(re.findall(r'["\']([^"\']+)["\']', host_match.group(1)))

    failures = []
    if nonstdlib:
        failures.append("non-standard-library Python imports found")
    if shell_true:
        failures.append("subprocess shell=True found")
    if forbidden:
        failures.append("third-party runtime references found in public instructions")
    if fetched_hosts != ["registry.npmjs.org", "tldraw.dev"]:
        failures.append("official fetch host allowlist changed unexpectedly")

    return {
        "ok": not failures,
        "package": root.name,
        "contract": "zero extra third-party runtime dependencies",
        "python": {
            "standard_library_only": not nonstdlib,
            "files": file_imports,
            "nonstdlib_imports": nonstdlib,
        },
        "subprocess": {
            "shell_true": shell_true,
            "allowed_executables": ["node", "npx"],
            "official_npm_package": "create-tldraw",
        },
        "network": {
            "enforced_fetch_hosts": fetched_hosts,
            "expected_hosts": OFFICIAL_NETWORK_HOSTS,
            "source_urls_in_runtime": discovered_urls,
        },
        "third_party_skill_dependencies": [],
        "forbidden_references": forbidden,
        "failures": failures,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit zero-extra-third-party dependency boundaries.")
    parser.add_argument("skill_dir", nargs="?", default=".")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()
    root = Path(args.skill_dir)
    result = audit(root)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
