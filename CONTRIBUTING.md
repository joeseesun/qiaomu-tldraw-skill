# Contributing

感谢你改进 `qiaomu-tldraw-skill`。

## 提交前

1. 新建 feature branch，不直接推送 `main`。
2. 只提交可公开的示例；不要加入 `.tldraw` 私有文件、运行数据库、Canvas API token、本机日志或未经授权的图片。
3. 如果更改路由，补 `evals/trigger_cases.json` 的 should-trigger、should-not-trigger 或 near-neighbor case。
4. 如果更改 Canvas API / custom shape 方法，说明核验的 tldraw offline 与 SDK 版本。
5. 运行：

```bash
python3 -m py_compile scripts/*.py
python3 scripts/validate_skill.py .
python3 scripts/trigger_eval.py .
python3 scripts/security_scan.py .
```

## Pull request

PR 请说明：

- 用户场景和边界；
- 修改文件；
- 验证命令和结果；
- 有视觉变化时附真实截图；
- 许可证/来源；
- 尚缺的证据。

提交贡献即表示你有权按本项目 MIT License 提供这些改动。
