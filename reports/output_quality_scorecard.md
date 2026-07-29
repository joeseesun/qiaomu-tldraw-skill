# Output Quality Scorecard

## Release candidate: 1.1.0

Date: 2026-07-29
Mode: Governed
Owner: 向阳乔木

## Evidence

| Gate | Result | Evidence |
|---|---|---|
| Package structure | pass | `scripts/validate_skill.py` |
| Trigger boundary | pass | 18/18 should-trigger / should-not-trigger / near-neighbor fixtures |
| Skill IR | pass | `reports/skill-ir.json` |
| Trust report | pass | `reports/trust-report.json`; no detected secret or private path |
| Dependency audit | pass | Python stdlib only; no `shell=True`; no community skill dependency; official host allowlist |
| Bundled tool tests | pass | 6/6; URL rejection, Range resume, CLI parsing, docs search, project inspection, offline app probe |
| Local Canvas API | pass | bundled stdlib client; clean-install run returned 8 open docs, 9 live recipes, 9 helpers |
| Official offline app probe | pass | macOS app `com.tldraw.desktop` version/build 1.12.0 found with OS-provided `plutil` |
| Durable script | pass | `state=applied`, no `lastApplyError` |
| Canvas lint | pass | 0 actionable lints in the recorded attention dashboard |
| Interaction | pass | selected token `4 → 0`; temperature `1 → 1.6`; restored to original state after async waits |
| Visual proof | pass | `docs/assets/product-screenshot.png`, real canvas screenshot |
| Packaged counter example | pass | fresh `.tldraw`; script applied; count `0 → 1`; restored to `0`; lints 0; saved |
| Official CLI metadata | pass | `create-tldraw` 5.2.5 from `registry.npmjs.org`; Node requirement `>=22.12.0`; 8 templates parsed from live help |
| Official docs sync | pass | index/docs/examples/releases/full downloaded with length and SHA-256 verification |
| Official docs search | pass | located current custom ShapeUtil/bindings sections and release migration guides |
| Partial-download recovery | pass | Range-resume regression test plus live complete sync after repeated CDN truncation |
| Official basic scaffold | pass | forced npmjs registry; telemetry off; official `tldraw/vite-template`; project-info correct |
| Official basic build | pass with warning | npm install from official registry; `tsc && vite build`; 805 modules; main chunk 1.86 MB warning retained |
| Official basic browser smoke | pass | Vite dev server ready; HTML loaded; 1440×1000 real Chrome screenshot showed canvas UI |
| Clean GitHub install | pass | installed from merged `main`; validator, dependency audit, 6/6 tests and doctor passed; three file hashes matched |
| GitHub release | pass | v1.1.0 published from merge commit `ef6457a`; not draft or prerelease |

## Human quality notes

The attention demo presents a clear teaching sequence: choose a Query, compare Query × Keys, observe Softmax, then read the weighted context vector. The interface has a strong selected state, readable semantic color roles, and visible temperature controls. It is a real custom shape rendered in tldraw offline, not a mock image.

## Missing evidence

- Provider-backed model eval: `missing evidence`.
- Blind human review with named reviewer and decision: `missing evidence`.
- Windows and Linux Canvas API smoke test: `missing evidence`.
- End-to-end typecheck/build/browser smoke for `multiplayer`, `agent`, `workflow`, `chat`, `image-pipeline`, `branching-chat`, and `shader`: `missing evidence`.
- Cold-reopen proof for the packaged minimal counter example: `missing evidence`; its fresh-document apply, interaction, lint, and save checks passed.

## Rollback boundary

The live interaction test restored the original shape props. Public package changes remain on a feature branch until validation and PR review; install proof is repeated after merge.
