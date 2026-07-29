# Installation and Official Lineage

本 skill 的运行方法只依赖 tldraw 官方产品与操作系统已有运行时，不依赖社区 skill、第三方 Python 包或第三方 CLI 包装器。

## 官方能力面

| 能力 | 官方来源 | 集成方式 | 许可证/边界 |
|---|---|---|---|
| tldraw offline | `tldraw/tldraw-offline`、`offline.tldraw.com` | 本地文件、Canvas API、document scripts | 应用闭源、All rights reserved；本仓库不分发 |
| offline Canvas API 文档 | 运行中应用的 `/readme`、`api.recipes` | `offline-readme`、`recipe` | 运行时读取，不复制 token 或内部数据库 |
| SDK CLI | npm `create-tldraw` / `npm create tldraw` | `cli-help`、`scaffold` | 官方包；遵循包内 tldraw license |
| SDK 文档 | `tldraw.dev/llms*.txt` | `docs-sync`、`docs-search` | 缓存到用户 cache；本仓库不重新发布全文 |
| SDK 源码/版本 | `tldraw/tldraw`、npm `tldraw` | official metadata 与 source links | SDK 使用 tldraw license |

## 安装

只需安装本 skill：

```bash
npx skills add joeseesun/qiaomu-tldraw-skill -g -y
```

使用 SDK CLI 时需要 Node.js / npx；本 skill 会按官方包的 `engines.node` 报告要求：

```bash
python3 scripts/qiaomu_tldraw.py official-info
python3 scripts/qiaomu_tldraw.py cli-help
```

使用 live `.tldraw` 文件时安装并启动 tldraw offline。若应用提供 Agent Setup，可安装它的官方共享 skill/helper；但本 skill 已集成 `/readme`、live recipes 和经过认证的标准库请求路径，不要求任何社区 skill。

## Zero-third-party contract

- Python scripts 只 import 标准库。
- SDK scaffolding 只调用官方 npm 包 `create-tldraw`。
- 文档只允许 `https://tldraw.dev/`。
- npm metadata 只允许 `https://registry.npmjs.org/`。
- Canvas API 只访问运行中应用声明的 loopback port。
- 不下载或执行社区 skill、第三方 npm CLI、浏览器扩展或远程 shell script。

## 版本漂移

CLI、templates、SDK API 和许可证可能变化。每次 SDK 任务前用 `official-info` 与 `docs-sync` 刷新，不把本文件记录的版本当永远正确。公开 claim 以 `reports/official-source-lock.json` 和当前运行结果为准。
