#!/usr/bin/env python3
"""Scan the public package for common secrets and private local paths."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
	"private_user_path": re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/"),
	"github_token": re.compile(r"\b(?:gh[opurs]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
	"openai_key": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
	"aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
	"pem_private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
	"bearer_literal": re.compile(r"Bearer\s+(?!<token>|\$|\{)[A-Za-z0-9._~-]{24,}", re.I),
}


def scan(root: Path) -> dict:
	findings = []
	skipped = []
	for path in sorted(root.rglob("*")):
		if not path.is_file() or any(part in {".git", ".tmp", "__pycache__"} for part in path.parts):
			continue
		try:
			text = path.read_text(encoding="utf-8")
		except UnicodeDecodeError:
			skipped.append(str(path.relative_to(root)))
			continue
		for line_no, line in enumerate(text.splitlines(), 1):
			for kind, pattern in PATTERNS.items():
				if pattern.search(line):
					findings.append({"kind": kind, "file": str(path.relative_to(root)), "line": line_no})
	return {
		"ok": not findings,
		"trust_report": "pass" if not findings else "block",
		"package": root.name,
		"findings": findings,
		"binary_files_skipped": skipped,
		"notes": ["Runtime Canvas API tokens are intentionally not read by this scan.", "Binary screenshots are listed but require separate visual review."],
	}


def main() -> None:
	parser = argparse.ArgumentParser(description="Scan skill files for secrets and private paths.")
	parser.add_argument("skill_dir", nargs="?", default=".")
	parser.add_argument("--output", "-o")
	args = parser.parse_args()
	root = Path(args.skill_dir).resolve()
	result = scan(root)
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
