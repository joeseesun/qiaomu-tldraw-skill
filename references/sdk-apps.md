# SDK Apps

## 官方入口

执行时先核对当前 CLI：

```bash
npm view create-tldraw version engines license dist-tags --json
npx create-tldraw@latest --help
```

2026-07-29 核验的 starter kits：`basic`、`multiplayer`、`agent`、`workflow`、`chat`、`image-pipeline`、`branching-chat`、`shader`。不要假设这个列表永远不变。

创建示例：

```bash
npm create tldraw@latest my-canvas -- --template basic
# 等价显式形式
npx create-tldraw@latest my-canvas --template basic
```

## 选模板

- `basic`：自定义画布产品、编辑器组件、最小 SDK 起点。
- `workflow`：节点/连接、状态机、自动化流程。
- `agent`：模型理解和操作 canvas；需要 provider 配置与额外安全边界。
- `chat` / `branching-chat`：视觉上下文对话或分支会话。
- `multiplayer`：实时协作；需要服务器、身份、数据与部署设计。
- `image-pipeline`：图像处理节点工作流。
- `shader`：GPU/视觉实验。

## 开发门禁

1. 读取项目的 `AGENTS.md`、`package.json`、lockfile、scripts 和当前 tldraw 版本。
2. 使用项目已有包管理器与脚本，不自创另一套命令。
3. 自定义 shape props 使用 validators 和 module augmentation；遵循当前 type definitions。
4. 输入到模型或外部 API 的 canvas 数据必须最小化、清理和明确授权。
5. 依次跑项目配置的 typecheck、lint、unit tests、build。
6. 启动真实浏览器 smoke test，检查首次加载、编辑、保存/刷新与关键交互。
7. 需要版本升级时用官方 `tldraw-migrate`，并 review diff。

## 许可证提醒

tldraw SDK 不是本仓库的 MIT 组件。开发可免费使用，生产使用和 watermark/license key 要求以当前 [tldraw license](https://tldraw.dev/community/license) 为准。starter kit 自身的许可证也应在生成项目里重新核对。
