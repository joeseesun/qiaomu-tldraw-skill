# Release Proof

Date: 2026-07-29

## GitHub

- Repository: `https://github.com/joeseesun/qiaomu-tldraw-skill`
- Initial release PR: `https://github.com/joeseesun/qiaomu-tldraw-skill/pull/1`
- Initial merge commit: `9d9d9fd0252042e7dbc5292fe8e7e660a3a28463`
- Default branch: `main`
- Visibility: public
- License detected by GitHub: MIT

## v1.1.0 official integration

- Integration PR: `https://github.com/joeseesun/qiaomu-tldraw-skill/pull/3`
- Merge commit: `ef6457a1d01a79dfe55f820b5babe6eb59c44569`
- Release: `https://github.com/joeseesun/qiaomu-tldraw-skill/releases/tag/v1.1.0`
- Release state: published, not draft, not prerelease
- Tag target: merge commit above

## v1.1.0 clean install proof

Command:

```bash
npx skills add joeseesun/qiaomu-tldraw-skill -g \
  --skill qiaomu-tldraw-skill --agent codex -y --copy
```

Observed:

- installed at `~/.agents/skills/qiaomu-tldraw-skill`;
- source recorded as `joeseesun/qiaomu-tldraw-skill`;
- package validator passed from the installed directory;
- dependency audit passed with standard-library-only Python and no third-party skill dependencies;
- 6/6 bundled unit tests passed;
- `doctor` passed against tldraw offline 1.12.0 and the live loopback API (8 open docs, 9 recipes, 9 helpers);
- installed files matched GitHub `main` by SHA-256:
  - `SKILL.md`: `bd9e3b86933e39dc9ab67e59eab62c91b9ba94810c3f49e579109cb2f13e341a`
  - `scripts/qiaomu_tldraw.py`: `bec91357adcdb6343bd7a23ca5426eb7e526219812c756814c0cc81af3c07502`
  - `reports/official-source-lock.json`: `22c03f61826e9209da9b617ab9162c09b261559d2ad6771f2f2b42da6b514406`

The earlier v1.0.0 install proof used `SKILL.md` SHA-256
`a57b32b32951c029df63cd06be7c84266b7762d66fdbdbc95b7b471a37121a93`.

## Manual GitHub setting

`missing evidence`: GitHub social preview cannot be set through the verified CLI/API path in this run. A maintainer can upload `docs/assets/product-screenshot.png` or a 1280×640 derivative in Repository Settings → Social preview.
