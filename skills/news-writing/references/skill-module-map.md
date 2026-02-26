# News-Writing Skill 模块总览

## 模块与入口

| 模块 | 作用 | 入口文件 |
|---|---|---|
| 类型路由 | 自动判定新闻类型并选择模板 | `references/news-type-playbook.md` |
| 数据源白名单 | 限定可用来源与 `source_id` | `references/source-whitelist-env-energy-lca.md` |
| 事实核验 | 双来源交叉核验与字段检查 | `references/fact-check.md` |
| 图文排版 | 图注、混排、截图策略 | `references/image-layout.md` |
| 截图校验卡 | 截图前后审核模板 | `assets/screenshot-validation-card-template.md` |
| 截图脚本 | 页面校验 + 审核 + 裁剪输出 | `scripts/capture_web_screenshots.py` |
| 发布站点管理 | 站点增删改查、默认站点 | `scripts/manage_publish_sites.py` |
| API发布 | dry-run 与正式发布、回执输出 | `scripts/publish_news_via_api.py` |
| API参考 | LCA Echo 接口字段与链路 | `references/lca-echo-api-publishing.md` |

## 常用流程速查

### A. 仅写作（不发布）
1. 判型 -> 选模板
2. 白名单取材 -> 事实核验
3. 图片审核与裁剪
4. 生成发布版正文

### B. 写作 + API发布
1. 完成 A 流程
2. `manage_publish_sites.py list`
3. `publish_news_via_api.py --dry-run`
4. 正式发布并记录回执

### C. 截图重做（问题排查）
1. 使用截图校验卡重建 `must/exclude/layout`
2. 开启 `--strict-validation`
3. 设置 `--audit-deny-keywords`
4. 生成 `--audit-report` 并据此剔除无关截图
