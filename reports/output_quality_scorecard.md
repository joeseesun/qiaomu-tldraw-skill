# Output Quality Scorecard

## Release candidate: 1.0.0

Date: 2026-07-29
Mode: Governed
Owner: 向阳乔木

## Evidence

| Gate | Result | Evidence |
|---|---|---|
| Package structure | pass | `scripts/validate_skill.py` |
| Trigger boundary | pass after regression fix | should-trigger / should-not-trigger / near-neighbor fixtures |
| Skill IR | pass | `reports/skill-ir.json` |
| Trust report | pass | `reports/trust-report.json`; no detected secret or private path |
| Official offline skill | pass | installed skill and `tq` helper discovered |
| Local Canvas API | pass | 4 docs, 9 live recipes, 9 helpers in the recorded run |
| Durable script | pass | `state=applied`, no `lastApplyError` |
| Canvas lint | pass | 0 actionable lints in the recorded attention dashboard |
| Interaction | pass | selected token `4 → 0`; temperature `1 → 1.6`; restored to original state after async waits |
| Visual proof | pass | `docs/assets/product-screenshot.png`, real canvas screenshot |
| Packaged counter example | pass | fresh `.tldraw`; script applied; count `0 → 1`; restored to `0`; lints 0; saved |
| SDK CLI discovery | pass | `create-tldraw` 5.2.5 help and starter list checked |
| Clean GitHub install | pass | source `joeseesun/qiaomu-tldraw-skill`; installed `SKILL.md` hash matches GitHub `main` |

## Human quality notes

The attention demo presents a clear teaching sequence: choose a Query, compare Query × Keys, observe Softmax, then read the weighted context vector. The interface has a strong selected state, readable semantic color roles, and visible temperature controls. It is a real custom shape rendered in tldraw offline, not a mock image.

## Missing evidence

- Provider-backed model eval: `missing evidence`.
- Blind human review with named reviewer and decision: `missing evidence`.
- Windows and Linux Canvas API smoke test: `missing evidence`.
- End-to-end typecheck/build/browser smoke for every official starter kit: `missing evidence`.
- Cold-reopen proof for the packaged minimal counter example: `missing evidence`; its fresh-document apply, interaction, lint, and save checks passed.

## Rollback boundary

The live interaction test restored the original shape props. Public package changes remain on a feature branch until validation and PR review; install proof is repeated after merge.
