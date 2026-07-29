# SDK Apps

## Official-first start

在写 SDK code 前：

```bash
python3 scripts/qiaomu_tldraw.py official-info
python3 scripts/qiaomu_tldraw.py docs-sync --bundle index --bundle docs --bundle examples --bundle releases
python3 scripts/qiaomu_tldraw.py docs-search "Quick start Editor persistence" --bundle docs
```

新项目使用 [Official CLI](official-cli.md)。已有项目先用 `project-info`，不要重新 scaffold 覆盖。

## Minimal official architecture

- `Tldraw` / `TldrawEditor`：canvas React surface。
- `Editor`：创建、更新、选择、页面、camera、export、events 的主接口。
- store/schema：持久记录、validation、migrations。
- `ShapeUtil` / `BindingUtil` / `OverlayUtil`：扩展类型与行为。
- tools / StateNode：用户交互状态机。
- UI components / overrides：产品界面扩展。
- persistence / sync：本地持久化和实时协作是不同架构选择。

具体 signatures 以同步的官方 docs、examples 和安装版本 `.d.ts` 为准。

## Implementation gates

1. 读取项目 `AGENTS.md`、package scripts、lockfile 和 tldraw 版本。
2. 通过官方 docs 搜索具体概念和 symbol；禁止只凭旧记忆写 API。
3. custom shape props 使用 validators、migrations 与当前 module augmentation 模式。
4. meaningful connections 使用 bindings，不把视觉接触误当数据关系。
5. persistence 明确 document data、session state、assets 和 multiplayer ownership。
6. 模型或外部 API 接收的 canvas 数据必须最小化、清理并获得授权。
7. 使用项目已有 package manager 运行 typecheck、lint、test、build。
8. 真实浏览器检查首次加载、编辑、undo/redo、保存/刷新、关键交互与控制台。

## License gate

tldraw SDK 的 source code 与 packages 使用 tldraw license。默认条款只允许 Development Environment；生产通常需要 trial、commercial 或 hobby license/key。生成 starter 的示例代码、SDK package 和第三方素材可能有不同许可证，逐项核对，不用本仓库 MIT 覆盖它们。
