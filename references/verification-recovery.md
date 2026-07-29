# Verification and Recovery

## 证据矩阵

| 层 | 证据 | 失败时 |
|---|---|---|
| Identity | name、file path、documentId、page、selection | 停止写入，重新发现 |
| Records | shape ids/types/props、unlocked | 修正 records / schema |
| Connections | bindings + lints | 重建 bound arrows |
| Script | state=applied、no apply error | 读 error log、冷注册 |
| Visual | real window screenshot | 修布局、等待渲染、重截 |
| Interaction | event → props/state readback | 查事件坐标、锁定、异步提交 |
| Persistence | save + cold reopen | 检查脚本 trust、旧 type、归档 |

## 关闭/失联文档

遇到 `Window closed before responding`、`Document not found` 或持续超时：

1. 不再使用旧 doc id。
2. 重新列文档。
3. 只在 name 与已记录 `documentId`/路径一致时恢复。
4. 如果只剩无关窗口，停止并报告；不能因为“它是唯一窗口”就复用。

## script 状态

- `applied`：当前文件已应用，可继续视觉/交互验证。
- `pending`：短暂轮询；不要立刻判失败。
- `error`：读取 `lastApplyError` 与 `errorLogPath`，修复后重新检查。

初始截图空白可能是 config remount race。确认 applied 后等待并重截；持续空白时加入 ErrorBoundary、检查 runtime log，并进行新 module + 新 type 冷注册。

## 交互验证

- 记录 before props。
- 通过真实 window、DOM event 或可解释的等价事件执行动作。
- 等待异步更新和 React commit。
- 读取 after props，断言预期变化。
- 恢复 neutral state，再截图。

纯调用内部 helper 函数不能证明用户点击路径正常。

## 回滚

- 原生 edits：用 editor history 或恢复已记录 shapes。
- 一次性 exec：只修改已确认 ids，必要时用保存前备份。
- document script：保留修改前内容；恢复脚本并等 watcher applied。
- custom type 迁移：在确认新 type 可渲染、可保存、可重开后删除旧 records。
- SDK app：feature branch、可审查 diff、项目测试通过后再合并。
