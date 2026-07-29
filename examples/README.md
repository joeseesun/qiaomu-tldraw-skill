# Examples

这些是可读、可改的最小片段，不是完整应用模板：

- `static-diagram.js`：放进 tldraw offline `/exec` 的原生 shapes + bound arrows 示例。
- `clickable-dashboard/`：document script 的 `config.js`、`main.js` 和 custom shape 结构示例。

运行前必须先读取当前 tldraw offline skill 和 live `api.recipes`。版本变化时，recipe 和 workspace types 高于此示例。

不要把示例直接写进用户当前文档：先确认目标，并给 IDs 加任务特有前缀。完成后验证 lints、script status、props readback 和真实截图。
