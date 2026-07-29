# Installation and Lineage

## 经过核验的能力面

| 能力 | 权威来源 | 本次核验 | 许可证/边界 |
|---|---|---|---|
| tldraw offline | `tldraw/tldraw-offline`、`offline.tldraw.com` | 1.12.0，2026-07-27 release | 应用闭源、All rights reserved，不由本仓库分发 |
| offline Agent Skill + `tq` | 桌面应用 Agent Setup 安装的 `tldraw-offline` | 本机可列文档、recipe、helper | 属于应用分发物；本仓库只调用公开的本地接口 |
| SDK CLI | npm `create-tldraw` / `npm create tldraw` | 5.2.5；Node `>=22.12.0` | `SEE LICENSE IN LICENSE.md`，遵循 tldraw license |
| SDK migration skill | `tldraw/tldraw/skills/tldraw-migrate` | 可由 `npx skills` 发现安装 | tldraw monorepo 的许可证边界；实验性、需 review |
| 创作/复刻社区 skill | `Zluowa/tldraw-ai-drawing-skills` | `tldraw-create`、`tldraw-recreate` | MIT；独立社区项目，非 tldraw 官方 |

版本会变化。公开文档中的“当前”只代表 2026-07-29 的验证结果；执行时重新运行：

```bash
npm view create-tldraw version engines license dist-tags --json
gh release view --repo tldraw/tldraw-offline --json tagName,publishedAt,url
npx skills add tldraw/tldraw --list --full-depth
```

## 推荐安装

```bash
npx skills add Zluowa/tldraw-ai-drawing-skills -g \
  --skill tldraw-create tldraw-recreate -y
npx skills add tldraw/tldraw -g --skill tldraw-migrate -y --full-depth
npx create-tldraw@latest --help
```

tldraw offline 的 skill 和 helper 应通过应用自身的 Agent Setup 安装/更新。常见共享位置是 `~/skills/tldraw-offline/`，各 agent 可能有副本或指针。不要从本仓库复制一个会随应用漂移的快照。

## 采用了什么，没有采用什么

采用：

- 社区仓库的“创作”和“严格复刻”分流、语义可编辑、同裁切比较、真实 app 测试。
- 官方 offline skill 的目标身份、records、bindings、recipes、script status 与保存模型。
- 官方 CLI / starter kits 的项目入口和官方迁移 skill 的版本化迁移职责。

没有采用：

- 不复制 tldraw offline 应用、官方 skill、token、runtime 数据库或私有 API 实现。
- 不把社区示例媒体或大段文本重新包装成自有内容。
- 不声称所有 starter kits、操作系统、agent harness 或 tldraw 版本都通过端到端测试。
