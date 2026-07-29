# Official tldraw Offline Canvas API

## 自包含读取顺序

本 skill 不需要社区 API helper。运行中应用是权威来源：

```bash
python3 scripts/qiaomu_tldraw.py doctor
python3 scripts/qiaomu_tldraw.py offline-readme
python3 scripts/qiaomu_tldraw.py list
python3 scripts/qiaomu_tldraw.py recipe custom-shape-config-js
```

标准库工具会从当前操作系统的 tldraw runtime config 读取 port/token，token 始终 redacted，并只发送到 `127.0.0.1`。每个请求重新读取 runtime config，避免应用重启后复用旧 token。

## API hierarchy

- `/readme`：当前应用的完整 Canvas API 文档。
- `/api/search`：文档发现、open docs、shapes、bindings、screenshots、imports、recipes。
- `/api/docs/create`：创建并打开新 `.tldraw`，不覆盖已有文件。
- `/api/doc/:id/exec`：对已确认 live Editor 执行一次性代码。
- `/api/doc/:id/script-workspace`：编辑随文件持久化的 document script。
- `/api/doc/:id/script-status`：检查 watcher、digest、pending/error/applied。

具体 endpoint 和 helper 可能随应用更新；不要把这张列表当完整 API，先读 live `/readme`。

## Runtime trust

- `server.json`、token、request logs、working database、WAL 和 `.script-workspace` 属于本机私有运行时。
- 只编辑 `script-workspace` 返回的 `editable` 范围；不改 app-owned 文件。
- 不打印 token，不将 runtime config 或 error log 原文提交到仓库。
- 多文档时核对 name、file path、documentId、page 和 shape content。
- 文档关闭后旧 doc id 失效，重新发现；不能写入“唯一剩下的窗口”。
