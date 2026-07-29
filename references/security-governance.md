# Security and Governance

## Trust boundary

- tldraw offline Canvas API 是本机受 bearer token 保护的回环服务。
- `server.json`、request logs、working database 与 `.script-workspace` 都是运行时私有边界。
- document scripts 是可执行代码；打开第三方 `.tldraw` 等同于打开带代码的项目。
- 外部图片、网页、模型返回和 shape metadata 都是不受信任输入。
- SDK app 中的模型 key、同步凭据和 license key 不进入 client bundle 或仓库。
- 内置 Python 工具只使用标准库；官方网络读取限制在 `tldraw.dev` 与 `registry.npmjs.org`。
- 官方 LLM 文档只写入用户 cache；公开仓库仅保留 URL、字节数与 SHA-256，不重新分发全文。
- `create-tldraw` 固定从 npm 官方 registry 解析，避免本机镜像配置改变上游来源。

## Permission boundary

- 只读诊断可列文档、读 shapes、bindings、status 和 screenshot。
- 写入前确认目标文档和用户意图。
- 删除、批量重建、覆盖脚本和对外发布需要更高审慎，保留回滚点。
- 网络只用于用户要求的外部来源、安装、官方文档或应用依赖。
- 除官方 `create-tldraw` 生成的 SDK 项目依赖外，Skill 本身不要求第三方 Python 包、社区 Skill 或另一套 CLI。
- 账号、付费模型、云同步和部署不因“画布任务”自动获得授权。

## Public claim guard

允许：

- “在列出的版本/平台上通过本次命令验证”。
- “recorded fixture”“real-window screenshot”“local runtime smoke test”。

禁止：

- 把静态 fixture 说成 provider-backed model eval。
- 没有 reviewer/decision 就说 human-reviewed。
- 没有真实重开就说 durable。
- 没有同裁切比较就说 pixel-perfect。
- 没有跨平台运行就说全面兼容。

缺证据统一写 `missing evidence`。

## Review cadence

Owner：向阳乔木。至少在以下事件后复核：

- tldraw offline Canvas API / Agent Skill 更新；
- tldraw SDK major release 或 `create-tldraw` starter kit 变化；
- document script 安全模型变化；
- 用户报告误写文档、unknown shapes、无法重开或 token 泄漏；
- 每次公开 release。
