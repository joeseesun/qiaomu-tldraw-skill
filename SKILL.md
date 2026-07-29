---
name: qiaomu-tldraw-skill
description: |
  Official-first Qiaomu tldraw creation skill and workflow for building, editing,
  recreating, scripting, linting, testing, migrating, and packaging tldraw canvases
  or tldraw SDK apps with the official CLI and official LLM-friendly documentation.
  Use when the user asks to 画 tldraw、复刻成可编辑画布、制作流程图/信息图/课件、
  创建交互或动画画布、写 custom ShapeUtil/document script、检查 .tldraw 文件，
  or scaffold and migrate a tldraw React application using official sources only.
---

# Qiaomu tldraw Skill

把需求交付为真实、可编辑、可验证的 tldraw 画布或画布程序，而不是只描述怎么画。

Copyright (c) 向阳乔木

## Router Rules

先判断交付面，再读取对应 reference。不要路由到社区 skill 或第三方包装器：

- 正在运行的 tldraw offline 画布：读 [Official Offline API](references/official-offline-api.md) 与 [Canvas Workflows](references/canvas-workflows.md)；优先读取运行中应用的 `/readme` 和 live recipe。
- 根据图片严格复刻：直接执行 [Visual Quality](references/visual-quality.md) 的测量、语义重建和同裁切比较。
- 从需求或草图创作：直接执行原生 shape 优先的创作流程，不要求另一个 skill。
- 可点击、动画、模拟器、仪表盘、自定义形状：读 [Durable Scripts](references/durable-scripts.md)。
- React / TypeScript tldraw SDK 应用：读 [Official CLI](references/official-cli.md)、[Official Docs](references/official-docs.md) 与 [SDK Apps](references/sdk-apps.md)。
- 升级现有 tldraw SDK：读 [SDK Migration](references/sdk-migration.md)，同步官方 releases 文档后再迁移；不要凭记忆猜 API。
- 只要 PNG/SVG 图，不需要 tldraw 可编辑源文件：不要触发本 skill。

先运行环境检查：

```bash
python3 scripts/qiaomu_tldraw.py doctor
```

SDK / API 工作开始前同步或搜索官方文档：

```bash
python3 scripts/qiaomu_tldraw.py official-info
python3 scripts/qiaomu_tldraw.py docs-sync --bundle index --bundle docs --bundle examples --bundle releases
python3 scripts/qiaomu_tldraw.py docs-search "custom ShapeUtil" --bundle docs
```

## Compact Workflow

1. 明确交付：现有画布修改、新建 `.tldraw`、参考图复刻、耐久交互，或 SDK 应用。
2. 锁定目标文档、页面、选择区和输出路径；多窗口时按名称、`documentId`、路径交叉确认。
3. 读取真实记录、运行中应用的官方 recipe，或缓存的官方 SDK docs；再选择原生 shapes、`/exec`、document script 或 SDK 工程。
4. 先搭语义结构与视觉层级，再补连接、状态、动画和细节。
5. 保存并验证记录、绑定、lint、脚本状态、真实窗口和交互状态。
6. 交付路径、截图、可编辑范围、验证结果、限制和恢复办法。

## Non-Negotiables

- 不直接编辑已打开的 `.tldraw` 归档、运行时数据库、WAL、锁文件或 `.script-workspace/**` 生成文件。
- 不把“只有一个打开窗口”当成“目标窗口”；文档关闭后必须重新发现并核对身份。
- 语义连接必须有真实 bindings；在 tldraw offline 中优先用 `helpers.createArrowBetweenShapes`。
- 画布程序的持久状态放进 shape props；`/exec` 监听器和全局变量不是持久交付。
- 自定义 shape/config 先读官方 live recipe，再写代码；不凭记忆猜当前 SDK API。
- SDK 工程只通过官方 `create-tldraw` CLI 或项目已有依赖创建；默认带 `--no-telemetry`。
- 文档只从 `tldraw.dev` 同步，CLI 元数据只从 `registry.npmjs.org` 读取；不调用第三方镜像、第三方 skill 或第三方 Python 包。
- 不以“保存成功”“脚本 applied”代替视觉和交互证据。
- 不发布 token、`server.json`、本机绝对路径、私有画布、运行数据库或未经授权的参考素材。
- 未实测的平台、模型、starter kit 或交互只能标记 `missing evidence`。

## Verification Ladder

按风险从低到高验证：

1. **Identity**：文档名、路径、`documentId`、页面、选择区正确。
2. **Records**：shape 类型、数量、文本、props、解锁状态符合预期。
3. **Connections**：有意义的箭头两端有 bindings；lint 无未处理问题。
4. **Durability**：`script-status.state === "applied"`，无 `lastApplyError`；保存后可重新打开。
5. **Visual**：真实窗口截图无裁切、遮挡、占位符、旧 shape 警告。
6. **Interaction**：真实点击/键盘或等价 DOM 事件改变持久 props，等待渲染后再读取和截图。
7. **App**：SDK 工程的 typecheck、lint、tests、build 和浏览器 smoke test 通过。

详细恢复路径见 [Verification and Recovery](references/verification-recovery.md)。

## Output Contract

交付必须包含：

1. `.tldraw` 文件或 SDK 项目的绝对路径；
2. 完成后的真实截图，视觉项目不可省略；
3. 主要 shape、交互与可编辑范围；
4. 已运行的验证及结果；
5. 外部素材、官方许可证、网络、凭据和持久脚本边界；
6. 仍为 `missing evidence` 的事项。

## Trust and Rollback Boundary

- 本地 Canvas API bearer token 只在运行时读取，只发往回环地址，不打印、不写入包。
- 破坏性修改前先读取目标记录并保存当前文档；只删除已确认的 shape ids。
- document script 会随文件打开执行，只在受信任文件中启用；对外分享前说明脚本存在。
- 回滚边界是：撤销本次 shape 变更、恢复本次脚本文件、关闭而不保存，或从用户已有备份恢复；不得擅自覆盖用户唯一副本。

## References

- [Installation and Lineage](references/installation-lineage.md)
- [Official CLI](references/official-cli.md)
- [Official Docs](references/official-docs.md)
- [Official Offline API](references/official-offline-api.md)
- [Canvas Workflows](references/canvas-workflows.md)
- [Durable Scripts](references/durable-scripts.md)
- [Visual Quality](references/visual-quality.md)
- [SDK Apps](references/sdk-apps.md)
- [SDK Migration](references/sdk-migration.md)
- [Verification and Recovery](references/verification-recovery.md)
- [Security and Governance](references/security-governance.md)
