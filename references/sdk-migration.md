# SDK Migration with Official Sources

本 skill 内置迁移方法，不要求另装 migration skill。它不复制一份会漂移的 API rename 清单，而是在每次迁移时读取官方 releases export 与项目实际 type definitions。

## Workflow

1. 运行 `project-info`，记录 package manager、所有 `tldraw` / `@tldraw/*` 版本和 scripts。
2. 同步官方 releases：

```bash
python3 scripts/qiaomu_tldraw.py docs-sync --bundle releases --bundle docs
python3 scripts/qiaomu_tldraw.py docs-search "Migration guide" --bundle releases
```

3. 确定 from → target；通过 npm 官方 metadata 验证 target，不把 `latest` 当成记忆值。
4. 只升级项目已经使用的 tldraw packages，并保持它们版本一致。
5. 运行项目 typecheck，按错误代码、symbol、文件分组。
6. 对每个 symbol 搜索 `llms-releases.txt` 的 migration guide，再核对安装包 `.d.ts` 和官方 examples。
7. 优先修 React types、shape/binding registration、API rename/removal、TipTap，再处理剩余错误和 deprecated APIs。
8. 跑 typecheck、lint、test、build 和浏览器 smoke；审查新增 casts、module augmentation、stubs 与 diff。

## Type-safety gate

- 禁止 `as any`、`as unknown`、`@ts-ignore`、`@ts-expect-error` 用来压掉迁移错误。
- 优先 `as const`、`satisfies`、正确 generics 与官方 module augmentation。
- symbol 在官方 release/doc/type definitions 都找不到时，标记 documentation gap；不私造 public API。

## Output

报告 from → target、修改文件、修复的 TS error codes、casts、module augmentations、deprecated symbols、未记录的官方文档缺口、测试与 `missing evidence`。
