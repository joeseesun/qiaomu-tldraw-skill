# qiaomu-tldraw-skill

**中文** | [English](#english)

![qiaomu-tldraw-skill 的真实 tldraw 交互画布](docs/assets/product-screenshot.png)

> 把一句需求、草图或参考图，交付为真实可编辑、可交互、可验证的 tldraw 画布或 SDK 应用。
>
> Turn a brief, sketch, or reference into an editable, interactive, verified tldraw canvas or SDK app.

[![License: MIT](https://img.shields.io/badge/License-MIT-2563eb.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-compatible-0f766e.svg)](SKILL.md)

**已验证（2026-07-29）：** tldraw offline 1.12.0、官方 `tq` Canvas API helper、`create-tldraw` 5.2.5、包验证、触发评估、安全扫描、真实交互画布，以及从公开 GitHub 仓库回装。SDK starter kits 的生成命令已核对；各模板的端到端构建为 `missing evidence`。

## 为什么值得用

很多 tldraw 提示词只会“说怎么画”，或生成一张看起来像画布的扁平图片。这个 skill 关注最终交付：选得中、改得动、连线有 binding、脚本能重开、按钮真的会改变持久状态，而且有截图和检查结果可以复核。

它把三类能力接成一条稳定路径：

- tldraw offline 的真实文件与本地 Canvas API；
- 原生 shape、document script、custom `ShapeUtil` 的交互画布；
- 官方 `create-tldraw` CLI 生成的 React / TypeScript SDK 应用。

## 一行安装

```bash
npx skills add joeseesun/qiaomu-tldraw-skill -g -y
```

验证：

```bash
test -f ~/.agents/skills/qiaomu-tldraw-skill/SKILL.md
python3 ~/.agents/skills/qiaomu-tldraw-skill/scripts/qiaomu_tldraw.py doctor
```

## 你可以直接这样说

- “用 qiaomu-tldraw-skill 把这个流程做成可编辑的 tldraw 图，连线必须真实绑定。”
- “把这张截图复刻成 PPT 可继续编辑的 tldraw 画布，并给我同裁切对比截图。”
- “在当前 tldraw 文件里做一个可点击的注意力机制演示，重开后仍能工作。”
- “用官方 CLI 建一个 tldraw workflow starter，再改造成我的可视化应用。”
- “检查这个 `.tldraw` 的脚本、未知 shapes、lint、可编辑性和发布风险。”

## 核心能力

| 能力 | 你得到什么 |
|---|---|
| 原生可编辑画布 | 文本、图形、分组、frame 和真实 bindings，而不是一张背景图 |
| 参考图复刻 | 以真实像素、构图、裁切和颜色为依据的语义化重建 |
| 交互与动画 | 状态写入 props、脚本 applied、真实事件和重开验证 |
| Canvas API 工作流 | 精确发现目标文档、读 records、执行、截图、lint 与保存 |
| SDK 应用 | 官方 starter kit、项目命令、类型/构建/浏览器验证路径 |
| 恢复与治理 | 多窗口误写保护、冷注册策略、secret scan、回滚边界 |

## 前置条件

- [ ] Node.js 满足当前 `create-tldraw` 要求：`node --version`
- [ ] Python 3.10+：`python3 --version`
- [ ] 创作本地 `.tldraw` 时已安装并启动 [tldraw offline](https://offline.tldraw.com/)
- [ ] tldraw offline 的官方 Agent Skill 已安装；运行 `python3 scripts/qiaomu_tldraw.py doctor`
- [ ] 需要新 SDK 项目时可运行：`npx create-tldraw@latest --help`

本 skill 不需要云端 API key。图像生成、联网资料或 AI starter kit 可能需要第三方模型凭据与费用；它们不应写入画布、日志或仓库。

## 它会怎么工作

1. 识别交付面：已有画布、新建文件、参考图复刻、document script 或 SDK 应用。
2. 锁定真实文档身份、页面、选择区和边界。
3. 读取官方 skill、Canvas API recipe 或 SDK 文档中的当前模式。
4. 用原生 shape 优先实现；只有真正的交互、动画或算法图形才升级到 custom shape。
5. 运行 records、bindings、lint、脚本、视觉、交互和重开门禁。
6. 返回文件、截图、可编辑范围、验证证据和 `missing evidence`。

## 示例输出

```text
Canvas: /path/to/attention-demo.tldraw
Editable: one custom dashboard shape; state stored in shape props
Verified: script=applied, lints=0, selectedToken 5→0, temperature 1→1.6
Visual proof: docs/assets/product-screenshot.png
Missing evidence: Windows/Linux Canvas API smoke test
```

示例脚本见 [`examples/`](examples/README.md)。

## 安装上游能力

本项目不打包 tldraw offline、官方 skill 或社区 skill。建议按需组合：

```bash
# 社区创作/复刻 skill
npx skills add Zluowa/tldraw-ai-drawing-skills -g \
  --skill tldraw-create tldraw-recreate -y

# tldraw 官方 SDK 迁移 skill
npx skills add tldraw/tldraw -g --skill tldraw-migrate -y --full-depth

# 官方 SDK 项目 CLI
npx create-tldraw@latest --help
```

tldraw offline 的 Canvas API skill 与 `tq` helper 由桌面应用的 Agent Setup 安装。完整来源和许可证边界见 [Installation and Lineage](references/installation-lineage.md)。

## 验证

```bash
python3 scripts/validate_skill.py .
python3 scripts/trigger_eval.py . --output reports/trigger-eval.json
python3 scripts/export_skill_ir.py . --output reports/skill-ir.json
python3 scripts/security_scan.py . --output reports/trust-report.json
python3 scripts/qiaomu_tldraw.py doctor --json
```

视觉与交互属于人工/真实运行时门禁，不能由静态检查替代。当前证据记录在 [`reports/output_quality_scorecard.md`](reports/output_quality_scorecard.md)。

## 风险、隐私与边界

- Canvas API token 只应从本机运行时配置读取，并只发送到 `localhost`。
- `.tldraw` document script 是随文件打开执行的代码；只打开可信来源，分享时明确告知。
- tldraw offline 不是开源软件；本仓库不重新分发应用、官方 skill 或其内部 API 实现。
- tldraw SDK 使用 tldraw 自己的许可证；生产使用可能需要 license key。请阅读 [tldraw license](https://tldraw.dev/community/license)。
- MIT 只覆盖本仓库原创代码和文档，不改变任何上游许可证。
- 参考图、字体、品牌与素材的使用权由使用者确认。

## Troubleshooting

| 症状 | 常见原因 | 处理 |
|---|---|---|
| `server.json not found` | tldraw offline 未运行或未启用 Agent Setup | 启动应用，在设置中安装/更新 Agent Skill，再跑 doctor |
| `401 Unauthorized` | 复用了上一次启动的 token | 每次请求重新读取运行时配置，或使用官方 `tq` helper |
| `Document not found` | 目标窗口关闭，doc id 已失效 | 重新列文档并核对名称、路径、`documentId`，不要写入别的窗口 |
| `script-status: pending` | watcher 还未应用 | 短暂轮询；若转 error，读取 `lastApplyError` / error log |
| `Some shapes unavailable` | custom type 未注册或旧类型残留 | 用新模块名与新 type 冷注册，迁移/删除旧记录后再重开 |
| 点击后读不到变化 | 事件或 React 提交是异步的 | 等待约 30–180 ms，再读 props 或截图 |
| SDK 工程不能构建 | Node、模板或 tldraw 版本变化 | 核对当前官方 CLI 要求，运行项目自己的 typecheck/build；迁移用 `tldraw-migrate` |

## 贡献与安全

欢迎提交 issue 和 PR。先阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [SECURITY.md](SECURITY.md)。不要在公开 issue 粘贴 Canvas API token、私有画布或本机数据库。

## 致谢与来源

- [tldraw offline](https://github.com/tldraw/tldraw-offline)：桌面文件、Canvas API、官方 Agent Skill 与 document scripts。
- [tldraw/tldraw](https://github.com/tldraw/tldraw)：SDK、`create-tldraw`、starter kits 与 `tldraw-migrate`。
- [Zluowa/tldraw-ai-drawing-skills](https://github.com/Zluowa/tldraw-ai-drawing-skills)：可编辑创作与参考图复刻的社区方法。
- `qiaomu-meta-skill`：Skill IR、触发评估、公开发布与治理门禁；方法上受到 `yaojingang/yao-meta-skill` 启发。

## 关于向阳乔木

- 网站：[qiaomu.ai](https://qiaomu.ai/)
- 博客：[blog.qiaomu.ai](https://blog.qiaomu.ai/)
- 推荐：[tuijian.qiaomu.ai](https://tuijian.qiaomu.ai/)
- X：[@vista8](https://x.com/vista8)
- GitHub：[@joeseesun](https://github.com/joeseesun/)

Copyright (c) 向阳乔木 · [MIT](LICENSE)

---

<a name="english"></a>

# English

`qiaomu-tldraw-skill` turns a brief, sketch, reference image, or application idea into a real editable tldraw canvas or SDK app. It focuses on live document identity, native editable shapes, bound connections, durable document scripts, visual proof, interaction readback, recovery, and public trust boundaries.

## Install

```bash
npx skills add joeseesun/qiaomu-tldraw-skill -g -y
python3 ~/.agents/skills/qiaomu-tldraw-skill/scripts/qiaomu_tldraw.py doctor
```

## Example prompts

- “Build an editable tldraw architecture diagram with real bound arrows.”
- “Recreate this slide as editable tldraw shapes and show a same-crop comparison.”
- “Create a clickable attention-mechanism demo that still works after reopening.”
- “Scaffold a tldraw workflow app with the official CLI and verify its build.”

## Verified scope and limits

Verified on 2026-07-29 with tldraw offline 1.12.0, its official `tq` Canvas API helper, and `create-tldraw` 5.2.5. Package validation, routing eval, trust scan, a live interactive canvas workflow, and a clean reinstall from the public GitHub repository were checked. End-to-end builds for every SDK starter kit and Windows/Linux Canvas API behavior remain `missing evidence`.

The MIT license covers only this repository's original code and documentation. tldraw offline, the tldraw SDK, community skills, model providers, fonts, and reference media retain their own terms. See [Security and Governance](references/security-governance.md) and [Installation and Lineage](references/installation-lineage.md).
