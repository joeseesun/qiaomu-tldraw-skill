# Official Documentation Integration

tldraw 为 coding agents 发布 LLM-friendly 文档。它们是本 skill 的优先技术来源：

| Bundle | 官方 URL | 用途 |
|---|---|---|
| `index` | `https://tldraw.dev/llms.txt` | 页面、reference、release、example 索引 |
| `docs` | `https://tldraw.dev/llms-docs.txt` | SDK features、概念与 API 工作流 |
| `examples` | `https://tldraw.dev/llms-examples.txt` | 官方可运行例子与源码 |
| `releases` | `https://tldraw.dev/llms-releases.txt` | 版本变化与 migration guides |
| `full` | `https://tldraw.dev/llms-full.txt` | 需要完整上下文时使用 |

## 同步

```bash
python3 scripts/qiaomu_tldraw.py docs-sync \
  --bundle index --bundle docs --bundle examples --bundle releases
```

默认缓存到 `~/.cache/qiaomu-tldraw-skill/official-docs/`，每个 bundle 记录 URL、bytes 与 SHA-256。全文不提交到本仓库，避免许可证、体积与漂移问题。

需要全部资料时再同步 `full`；不要同时把 `full` 和所有分包塞进 agent context。

## 搜索路由

```bash
python3 scripts/qiaomu_tldraw.py docs-search "custom ShapeUtil" --bundle docs
python3 scripts/qiaomu_tldraw.py docs-search "arrow bindings" --bundle docs
python3 scripts/qiaomu_tldraw.py docs-search "createShape example" --bundle examples
python3 scripts/qiaomu_tldraw.py docs-search "Migration guide" --bundle releases
```

选择：

- API 行为、props、Editor、persistence、bindings、events：`docs`。
- 需要当前写法的代码：`examples`，再核对对应 SDK 版本。
- 升级、deprecated、breaking change：`releases`。
- 不知道资料在哪：先 `index`。

## Evidence and trust

- downloader 只允许 `tldraw.dev`。
- 搜索在本机缓存上离线完成，不把 query 或项目代码上传。
- cache 不是永恒真相；版本任务开始前刷新。
- 文档描述与安装包 type definitions 冲突时，以项目安装的版本、release migration guide 和实际类型检查为准。
- `reports/official-source-lock.json` 只是当次抓取证据，不代表未来内容。
