#!/usr/bin/env python3
"""Deterministic routing smoke eval for qiaomu-tldraw-skill."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def norm(text: str) -> str:
	return re.sub(r"\s+", " ", text.lower()).strip()


def phrases(text: str, values: list[str]) -> list[str]:
	value = norm(text)
	return [item for item in values if norm(item) in value]


def evaluate(root: Path, cases_path: Path) -> dict:
	cases = json.loads(cases_path.read_text(encoding="utf-8"))
	frontmatter = (root / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
	terms = cases["terms"]
	description_hits = {group: phrases(frontmatter, values) for group, values in terms.items()}
	results = []
	for bucket in ("should_trigger", "should_not_trigger", "near_neighbor"):
		expected = bucket == "should_trigger"
		for raw in cases[bucket]:
			text = raw["text"] if isinstance(raw, dict) else raw
			hits = {group: phrases(text, values) for group, values in terms.items()}
			has_tldraw = bool(hits["tldraw"])
			has_canvas_action = bool(hits["canvas_action"])
			has_sdk_action = bool(hits["sdk_action"])
			excluded = bool(hits["negative"])
			predicted = has_tldraw and (has_canvas_action or has_sdk_action) and not excluded
			passed = predicted == expected
			results.append({
				"bucket": bucket,
				"prompt": text,
				"expected_trigger": expected,
				"predicted_trigger": predicted,
				"passed": passed,
				"hits": {key: value for key, value in hits.items() if value},
			})
	failures = [item for item in results if not item["passed"]]
	return {
		"ok": not failures and all(description_hits[group] for group in ("tldraw", "canvas_action", "sdk_action")),
		"description_hits": description_hits,
		"summary": {"total": len(results), "passed": len(results) - len(failures), "failed": len(failures)},
		"failures": failures,
		"results": results,
	}


def main() -> None:
	parser = argparse.ArgumentParser(description="Run trigger boundary cases.")
	parser.add_argument("skill_dir", nargs="?", default=".")
	parser.add_argument("--cases", default="evals/trigger_cases.json")
	parser.add_argument("--output")
	args = parser.parse_args()
	root = Path(args.skill_dir).resolve()
	cases = Path(args.cases)
	if not cases.is_absolute():
		cases = root / cases
	result = evaluate(root, cases)
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
