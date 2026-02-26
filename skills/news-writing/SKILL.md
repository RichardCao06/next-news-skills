---
name: news-writing
description: 新闻采编全链路技能：按“新闻类型模板 + 数据源白名单 + 事实核验 + 图片审核裁剪 + API发布”完成从选题到上线。用于生成简报/深度/专题采访/实时新闻/人物专访，统一图文排版，并可将稿件通过接口发布到指定站点（含站点管理与发布回执）。
---

# News Writing

统一执行以下模块，确保“可发布、可追溯、可复核、可上线”。

## 0) 模块读取顺序（必须遵循）

模块索引：`references/skill-module-map.md`

1. 本文件（流程总控）
2. 新闻类型路由：`references/news-type-playbook.md`
3. 数据源白名单：`references/source-whitelist-env-energy-lca.md`
4. 事实核验细则：`references/fact-check.md`
5. 图文与截图：`references/image-layout.md` + `assets/screenshot-validation-card-template.md`
6. 站点发布（仅发布任务）：`references/lca-echo-api-publishing.md`

## 1) 任务约束采集

先记录：
- 新闻类型：`简报` / `深度报道` / `专题采访` / `实时新闻` / `人物专访`
- 发布渠道、目标读者、字数、语气、截止时间、是否双语
- 展示形态：`发布版（少标题）` / `编辑版（结构化）`
- 是否需要 API 发布到网站

默认值（信息不全时）：
- 中性客观语气
- `发布版（少标题）`
- Markdown 输出

## 2) 新闻类型自动路由与模板

先读取：`references/news-type-playbook.md`

| 类型 | 模板 |
|---|---|
| 简报 | `assets/brief-news-template.md` |
| 深度报道 | `assets/in-depth-report-template.md` |
| 专题采访 | `assets/thematic-interview-template.md` |
| 实时新闻 | `assets/live-news-template.md` |
| 人物专访 | `assets/profile-interview-template.md` |

规则：
- 用户只给“话题”时，必须自动判型（关键词 -> 评分 -> 平分决策）
- 输出正文前先给 `类型判定卡`
- 信号不足时才降级为 `简报`

## 3) 白名单取材与事实核验

白名单入口：
- `环境与能源 > LCA生命周期`：`references/source-whitelist-env-energy-lca.md`

硬约束：
- 仅用白名单来源；非白名单只能放“候选来源”
- 每条事实必须落 `source_id + 层级路径 + 链接`
- 正文仅写“已核实”事实；未核实进入“待确认列表”

素材表字段（固定）：
- `编号` `事实陈述` `来源层级路径` `source_id` `来源链接/出处` `时间` `地点` `可核实状态` `备注`

最小核验标准：
- 关键事实至少双来源交叉验证（原始来源优先）
- 人名/机构/地名/数字/时间逐项核对
- 引述保留语境，不改写原意

## 4) 图片与截图审核流程（强制门禁）

图片清单字段（固定）：
- `图片编号` `用途` `文件路径或链接` `来源` `source_id` `版权状态` `图注` `alt文本` `可用状态`

截图执行标准（适用于任何新闻类型）：
1. 先建 `截图校验卡`（模板：`assets/screenshot-validation-card-template.md`）
2. 页面文本预检（must/exclude/audit deny）
3. 再截图（优先 `element`，其次 `fullPage`）
4. 统一裁剪为新闻版式尺寸（默认 `1200x720`）
5. 发布前审核（命中拦截页/验证码/错误页必须剔除）

脚本：
- `scripts/capture_web_screenshots.py`

关键参数：
- `--strict-validation`
- `--match-mode all|any|threshold`
- `--min-keyword-hit`
- `--audit-deny-keywords`
- `--layout-size` `--layout-mode` `--layout-anchor`
- `--entry ...|exclude_keywords|layout_opts`

## 5) 写作与排版

写作模板：
- 主模板按第2节路由强制执行
- 通用兜底模板：`assets/news-article-template.md` / `assets/rich-media-news-template.md`

发布版排版约束：
- 少标题防碎片：`简报<=0`、`实时<=1`、`深度<=2`、`专题<=2`、`专访<=2`
- 结构：标题 -> 导语 -> 连续正文 -> 必要配图
- 采编标签（核验方法、待补充）放附录，不进入正文段落

风格参考：
- `references/writing-style.md`
- `references/chinese-style-variants.md`

## 6) 发布前终检

终检清单：
- 事实准确、逻辑完整、语言无歧义
- 法律合规（无隐私泄露、无未证实指控）
- 图片合规（版权、图注、alt、无误导裁切）
- 超链接可点击且无污染（URL 不拼接说明文字）

## 7) API发布与站点管理（按需启用）

先读取：`references/lca-echo-api-publishing.md`

脚本：
- 站点管理：`scripts/manage_publish_sites.py`
- 新闻发布：`scripts/publish_news_via_api.py`

标准流程：
1. 初始化站点：`python3 scripts/manage_publish_sites.py init`
2. 查看站点：`python3 scripts/manage_publish_sites.py list`
3. 发布预检：`python3 scripts/publish_news_via_api.py ... --dry-run`
4. 正式发布：去掉 `--dry-run`
5. 回执入档：至少包含 `site_id` `post_id` `post_url` `community_id` `status`

默认集成站点：
- `lca-echo`（`https://lca-echo.lovable.app`）

## 8) 输出规范

默认输出 5 段：
1. `新闻正文`（发布版）
2. `图片与版式清单`
3. `事实核验摘要`
4. `待补充信息`
5. `风格与模板执行说明`

按需附加：
6. `数据源使用清单`（启用白名单时）
7. `发布回执`（启用 API 发布时）
