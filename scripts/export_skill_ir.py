#!/usr/bin/env python3
"""Export a compact, platform-neutral Skill IR document."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


def files(root: Path, folder: str) -> list[str]:
	base = root / folder
	return [
		str(path.relative_to(root))
		for path in sorted(base.rglob("*"))
		if path.is_file() and "__pycache__" not in path.parts
	] if base.exists() else []


def frontmatter(text: str) -> dict[str, str]:
	match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
	if not match:
		return {}
	block = match.group(1)
	name = re.search(r"^name:\s*(.+)$", block, re.M)
	description = re.search(r"^description:\s*\|\n((?:\s+.*\n?)+)", block, re.M)
	return {
		"name": name.group(1).strip() if name else "",
		"description": " ".join(line.strip() for line in description.group(1).splitlines()) if description else "",
	}


def build(root: Path) -> dict:
	manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
	cases = json.loads((root / "evals/trigger_cases.json").read_text(encoding="utf-8"))
	front = frontmatter((root / "SKILL.md").read_text(encoding="utf-8"))
	return {
		"schema_version": "2.0.0-qiaomu-lite",
		"generated_at": date.today().isoformat(),
		"package": {key: manifest.get(key) for key in ("name", "version", "owner", "maturity_tier", "lifecycle_stage", "upstream_inspiration")},
		"intent": {"description": front.get("description"), **manifest.get("intent", {})},
		"triggers": {key: [item.get("text", item) if isinstance(item, dict) else item for item in cases.get(key, [])] for key in ("should_trigger", "should_not_trigger", "near_neighbor")},
		"workflow": ["route delivery surface", "confirm target identity", "read live recipe or SDK source", "build editable semantics", "verify records, visual, interaction, and persistence", "report evidence and gaps"],
		"output_contract": ["artifact path", "real screenshot", "editable surface", "verification evidence", "license and trust boundary", "missing evidence"],
		"resources": {folder: files(root, folder) for folder in ("references", "scripts", "examples", "evals", "reports")},
		"portability": {
			"targets": ["openai", "claude", "generic", "agent-skills-compatible"],
			"local_canvas_dependency": "tldraw offline; bundled Python stdlib client reads its live official API",
			"sdk_dependency": "official create-tldraw CLI and generated project",
			"documentation": "official tldraw.dev LLM exports cached and searched by bundled stdlib tooling",
			"third_party_skill_dependencies": [],
			"degradation": "without a live app, do not claim live canvas verification",
		},
		"trust": {
			"token": "runtime-only, loopback-only, redacted",
			"document_scripts": "trusted-code-only",
			"rollback_boundary": "confirmed shape ids, preserved script content, user backup or feature branch",
			"public_claim_policy": "claim only current recorded evidence; otherwise mark missing evidence",
		},
	}


def main() -> None:
	parser = argparse.ArgumentParser(description="Export Skill IR.")
	parser.add_argument("skill_dir", nargs="?", default=".")
	parser.add_argument("--output", "-o")
	args = parser.parse_args()
	root = Path(args.skill_dir).resolve()
	rendered = json.dumps(build(root), ensure_ascii=False, indent=2) + "\n"
	if args.output:
		output = Path(args.output)
		if not output.is_absolute():
			output = root / output
		output.parent.mkdir(parents=True, exist_ok=True)
		output.write_text(rendered, encoding="utf-8")
	print(rendered, end="")


if __name__ == "__main__":
	main()
