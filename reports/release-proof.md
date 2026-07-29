# Release Proof

Date: 2026-07-29

## GitHub

- Repository: `https://github.com/joeseesun/qiaomu-tldraw-skill`
- Initial release PR: `https://github.com/joeseesun/qiaomu-tldraw-skill/pull/1`
- Initial merge commit: `9d9d9fd0252042e7dbc5292fe8e7e660a3a28463`
- Default branch: `main`
- Visibility: public
- License detected by GitHub: MIT

## Clean install proof

Command:

```bash
npx skills add joeseesun/qiaomu-tldraw-skill -g \
  --skill qiaomu-tldraw-skill --agent codex -y --copy
```

Observed:

- installed at `~/.agents/skills/qiaomu-tldraw-skill`;
- source recorded as `joeseesun/qiaomu-tldraw-skill`;
- package validator passed from the installed directory;
- `doctor` passed against the running official offline skill/helper;
- installed `SKILL.md` SHA-256 matched GitHub `main`:
  `a57b32b32951c029df63cd06be7c84266b7762d66fdbdbc95b7b471a37121a93`.

## Manual GitHub setting

`missing evidence`: GitHub social preview cannot be set through the verified CLI/API path in this run. A maintainer can upload `docs/assets/product-screenshot.png` or a 1280×640 derivative in Repository Settings → Social preview.
