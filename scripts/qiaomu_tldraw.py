#!/usr/bin/env python3
"""Safe diagnostics and read-only queries for tldraw offline's local Canvas API."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


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


def doctor() -> dict[str, Any]:
	installed = []
	for root in skill_candidates():
		if (root / "SKILL.md").is_file():
			installed.append({"path": str(root), "tq": (root / "tq").is_file()})
	result: dict[str, Any] = {
		"ok": False,
		"platform": platform.system(),
		"python": platform.python_version(),
		"official_skill": installed,
		"runtime_config": None,
		"server": None,
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
		result["ok"] = bool(installed) and bool(probe.get("success"))
	except (OSError, RuntimeError, ValueError, urllib.error.URLError) as exc:
		result["error"] = str(exc)
	return result


def main() -> None:
	parser = argparse.ArgumentParser(description="Diagnose and query a local tldraw offline Canvas API without exposing its token.")
	sub = parser.add_subparsers(dest="command", required=True)
	doctor_parser = sub.add_parser("doctor", help="Check official skill, helper, runtime config, and server.")
	doctor_parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON (default output is also JSON).")
	sub.add_parser("list", help="List open documents (read-only).")
	recipe = sub.add_parser("recipe", help="Read one live Canvas API recipe.")
	recipe.add_argument("id", help="Recipe id, e.g. custom-shape-config-js.")
	args = parser.parse_args()

	if args.command == "doctor":
		output = doctor()
	elif args.command == "list":
		output = api_request("POST", "/api/search", {"code": "return await api.getDocs()"})
	else:
		code = "return api.recipes[" + json.dumps(args.id) + "] ?? null"
		output = api_request("POST", "/api/search", {"code": code})

	print(json.dumps(output, ensure_ascii=False, indent=2))
	if args.command == "doctor" and not output.get("ok"):
		raise SystemExit(2)


if __name__ == "__main__":
	main()
