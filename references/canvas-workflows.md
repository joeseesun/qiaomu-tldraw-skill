# Canvas Workflows

## 先读官方本机 skill

对 live canvas 任务，先找到并完整读取 `tldraw-offline/SKILL.md`。它随桌面应用更新，是端点、recipes、helper 和安全模型的当前来源。本 reference 只给决策骨架。

## 选择实现层

| 需求 | 首选 |
|---|---|
| 排列、文字、普通图形、静态图表 | 原生 shapes + `/exec` |
| 有意义的流程关系 | 原生 shapes + bound arrows |
| 点击、动画、模拟、重开执行 | document script |
| 新 shape schema / React DOM UI | `config.js` + custom `ShapeUtil` + `main.js` |
| 独立部署、多用户、产品级 UI | tldraw SDK app |

静态视觉不要因为“写 React 更快”就变成 custom shape。可选中、可编辑、可导出和可迁移通常在原生 shapes 上更好。

## Live canvas 顺序

1. `doctor` 检查 app、skill、helper 和 server。
2. 列出文档；用文件名、路径、`documentId` 和当前内容确认目标。
3. 读取当前 page 的 shapes；批量/破坏性修改前再次确认数量和内容。
4. 需要 durable behavior 时先获取 `script-workspace`，读取已有 `main.js` / `config.js`，不要覆盖既有脚本。
5. 读取匹配的 `api.recipes['...']` 全文。
6. 用稳定语义 id 创建或更新；rerun 更新而非复制。
7. `/exec` 变更末尾 `await helpers.saveDoc()`；document script 内不要调用它。
8. 跑 lints、bindings、script status、screenshot 和交互验证。

## 图表连接

连接是数据，不是装饰：

- 在 offline API 中用 `helpers.createArrowBetweenShapes(fromId, toId, options)`。
- 检查 arrow bindings，而不是只看箭头视觉上靠近盒子。
- 只有明确的装饰箭头才允许无 binding，并给出局部 lint 说明。
- 连接标签独立、简短、方向明确。

## 画布信息架构

- 先建立标题、主路径、辅助解释、图例/控制的层级。
- 选择 4–6 个语义颜色角色，颜色不能成为唯一编码。
- 统一间距、圆角、线宽和字体层级。
- 重要文字保持独立；需要后续修改的对象保持解锁。
- 适合演示/课件的 frame 使用明确宽高和一致内边距。
- 复杂可视化先做“读懂一条路径”的 MVP，再补全部细节。
