# Durable Scripts

## 文件职责

- `script/config.js`：编辑器 mount 前注册 custom shapes、bindings、overlays、tools、components。
- `script/main.js`：编辑器 mount 后创建/迁移记录、监听事件、运行状态逻辑。
- sibling modules：承载 custom util / component；由 `config.js` 导入。

先读 live recipe：`custom-shape-config-js`、`clickable-card-or-button-ui`、`animation-simulation-loop` 等。

## 状态与事件

- 把选择项、温度、步骤、播放状态等持久状态放入 validated shape props。
- React component 根据 props 渲染，通过 `editor.updateShape` 更新。
- 如果内部 DOM pointer 被锁定或画布事件抢占，用 `editor.on('event')` + page-coordinate hit testing 作为可靠路径。
- 测试 synthetic event 后等待 30–70 ms 再读 props；视觉截图可等待 100–180 ms。
- 使用 `AbortSignal` 或等价 cleanup 管理监听器和 timer，rerun 不叠加。
- document script 不调用 `helpers.saveDoc()`；由 watcher/用户保存模型负责。

## Cold registration 恢复策略

document script 的模块可能在热重载时复用旧 module/type：

1. 先查看 `script-status`、`lastApplyError` 和 error log。
2. 如果更改 util/component 后仍渲染旧实现，换新的 sibling module 文件名。
3. 同时换新的 custom shape `type` / class static type；只换 shape id 不够。
4. 创建/迁移新 type 记录，再删除确认过的旧 type 记录。
5. 保存、关闭并重新打开，确认无 unknown-shape placeholder。

新增 required props 到已有 type 时，旧 records 可能不再通过 schema。优先显式迁移，不要假设 default props 会修复所有旧记录。

## Custom shape 最小门禁

- props 有 validators 和 defaults。
- `getGeometry` 与可点击区域一致。
- component 的 DOM 不泄漏画布外事件。
- rerun 不重复创建 shape 或 event listener。
- script status 为 `applied`，`lastApplyError` 为空。
- props readback 证明至少一条交互转换。
- 冷重开无占位符、无旧 type 警告、状态符合设计。
