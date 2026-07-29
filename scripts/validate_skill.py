#!/usr/bin/env python3
"""Validate the public qiaomu-tldraw-skill package contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED = [
	"SKILL.md",
	"README.md",
	"LICENSE",
	"manifest.json",
	"agents/interface.yaml",
	"evals/trigger_cases.json",
	"references/installation-lineage.md",
	"references/official-cli.md",
	"references/official-docs.md",
	"references/official-offline-api.md",
	"references/sdk-migration.md",
	"references/security-governance.md",
	"scripts/test_qiaomu_tldraw.py",
	"scripts/dependency_audit.py",
]


def validate(root: Path) -> dict:
	root = root.resolve()
	failures: list[str] = []
	warnings: list[str] = []
	for rel in REQUIRED:
		if not (root / rel).is_file():
			failures.append(f"missing required file: {rel}")

	skill = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").exists() else ""
	match = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
	frontmatter = match.group(1) if match else ""
	if "name: qiaomu-tldraw-skill" not in frontmatter:
		failures.append("SKILL.md frontmatter name mismatch")
	for term in ["description:", "tldraw", "workflow", "qiaomu"]:
		if term.lower() not in frontmatter.lower():
			failures.append(f"frontmatter missing routing term: {term}")

	readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").exists() else ""
	for term in ["npx skills add", "你可以直接这样说", "Troubleshooting", "# English", "product-screenshot.png", "零额外第三方依赖"]:
		if term not in readme:
			failures.append(f"README missing public surface: {term}")

	public_text = "\n".join(
		path.read_text(encoding="utf-8")
		for path in [root / "SKILL.md", root / "README.md", *sorted((root / "references").glob("*.md"))]
		if path.is_file()
	)
	for forbidden in ["Zluowa/tldraw-ai-drawing-skills", "tldraw-create", "tldraw-recreate"]:
		if forbidden.lower() in public_text.lower():
			failures.append(f"public package retains third-party runtime dependency: {forbidden}")

	try:
		manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
		if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
			failures.append("manifest version is not semver")
		if manifest.get("maturity_tier") != "Governed":
			failures.append("manifest maturity_tier must be Governed")
	except (OSError, json.JSONDecodeError) as exc:
		failures.append(f"invalid manifest.json: {exc}")

	for link in re.findall(r"\]\(([^)#]+\.md)\)", skill + "\n" + readme):
		if not link.startswith(("http://", "https://")) and not (root / link).exists():
			failures.append(f"broken markdown link: {link}")

	for path in root.rglob("*"):
		if any(part in {".git", ".tmp", "__pycache__"} for part in path.parts):
			continue
		if path.is_file() and path.stat().st_size > 5_000_000:
			warnings.append(f"large file: {path.relative_to(root)}")
	return {"ok": not failures, "package": root.name, "failures": failures, "warnings": warnings}


def main() -> None:
	parser = argparse.ArgumentParser(description="Validate qiaomu-tldraw-skill.")
	parser.add_argument("skill_dir", nargs="?", default=".")
	args = parser.parse_args()
	result = validate(Path(args.skill_dir))
	print(json.dumps(result, ensure_ascii=False, indent=2))
	if not result["ok"]:
		raise SystemExit(2)


if __name__ == "__main__":
	main()
