# Official create-tldraw CLI

## 权威入口

官方推荐命令：

```bash
npm create tldraw@latest
```

本 skill 的标准库 wrapper 提供非交互、可审计的等价入口：

```bash
python3 scripts/qiaomu_tldraw.py cli-help --version latest
python3 scripts/qiaomu_tldraw.py scaffold ./my-canvas --template basic --version latest --dry-run
python3 scripts/qiaomu_tldraw.py scaffold ./my-canvas --template basic --version latest
```

wrapper 实际执行 `npx --yes --registry=https://registry.npmjs.org create-tldraw@<version> ...`，不引入另一个 npm package，也不继承可能指向第三方镜像的 npm registry。默认加 `--no-telemetry`；只有用户明确允许时才传 `--telemetry` 给 wrapper。

## 当前 templates 的选择逻辑

不要只相信静态列表，先运行 `cli-help`。2026-07-29 的官方 5.2.5 CLI 返回：

| Template | 适用场景 | 额外边界 |
|---|---|---|
| `basic` | Vite + React + TypeScript 最小画布 | 推荐默认 |
| `multiplayer` | 自托管实时协作 | 服务器、身份、存储、部署 |
| `agent` | AI agent 操作 canvas | 模型凭据、费用、输入清理 |
| `workflow` | 节点和连接的可视化流程 | 执行引擎与状态语义 |
| `chat` | 草图/图片作为聊天上下文 | 上传、模型与隐私 |
| `image-pipeline` | 图像生成/处理节点管线 | provider、成本、素材权利 |
| `branching-chat` | 分支会话树 | 数据持久化与分支一致性 |
| `shader` | 响应 shapes 的 WebGL 视觉 | GPU、性能、降级 |

## Scaffold safety

- 目标目录非空时 wrapper 直接停止，避免官方 CLI 自动改用后缀目录造成误写。
- version/tag 与 template id 必须通过字符白名单。
- subprocess 使用参数数组，不经过 shell。
- 先 `--dry-run` 检查命令、路径、template 与 telemetry。
- 创建后运行 `project-info`，确认 package manager、tldraw 版本和 scripts。
- 安装依赖、运行 dev/build 之前读生成项目的 README、LICENSE、package scripts。

## 生成后验证

```bash
python3 scripts/qiaomu_tldraw.py project-info ./my-canvas
```

随后使用生成项目自己的包管理器。npm 路径应先检查 `npm config get registry`；需要严格官方来源时使用 `npm install --registry=https://registry.npmjs.org --no-audit`。再依次运行存在的 typecheck、lint、test、build，并用真实浏览器检查首次加载、编辑、刷新和关键交互。

## License

CLI 生成的 starter code 与 SDK 许可证边界要在生成项目内重新核对。tldraw SDK 本身是 source-available，不是 MIT SDK；生产部署通常需要有效 license key。不要因为本 skill 是 MIT 就把 SDK 或生成项目一概描述为 MIT。
