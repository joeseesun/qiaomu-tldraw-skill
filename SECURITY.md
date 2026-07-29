# Security Policy

## 支持范围

安全修复优先覆盖最新 `main` 和最新 release。历史版本按影响和可复现性决定是否回补。

## 私密报告

请使用 GitHub repository 的 **Security → Report a vulnerability** 私密报告功能。如果该功能不可用，请通过维护者公开资料中的联系方式先索取私密渠道，不要在公开 issue 粘贴敏感内容。

报告请包含：受影响版本、复现步骤、影响、最小化日志和建议修复。请先删除：

- Canvas API bearer token；
- `server.json` 原文；
- 私有 `.tldraw` 文件和脚本；
- 本机用户名、绝对路径、数据库和 request logs；
- 模型、同步、部署或 license keys。

## 责任边界

本仓库不分发 tldraw offline、tldraw SDK 或第三方 skills。上游产品漏洞也请同步报告给对应维护者。document script 是可执行代码：只打开可信 `.tldraw` 文件，并在分享时明确告知其中包含脚本。
