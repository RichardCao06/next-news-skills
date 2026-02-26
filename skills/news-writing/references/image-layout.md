# Image Insertion And Mixed Layout Guide

模块总览：`references/skill-module-map.md`

## 图片使用原则

- 先事实后配图：图片服务新闻事实，不反客为主
- 先版权后发布：不明版权图片一律标记“不可用”
- 先说明后展示：每图必须有图注、来源、alt文本
- 先入库后使用：仅使用已进入“图片素材清单”的图片，不临时加图
- 先出处后插图：每图必须标注 `来源名称 + source_id + 链接/文件路径`

## 图片素材清单模板

| 图片编号 | 用途 | 文件路径/链接 | 来源 | source_id | 版权状态 | 图注 | alt文本 | 可用状态 |
|---|---|---|---|---|---|---|---|---|
| P01 | 首图 |  |  |  | 已授权/待确认/禁用 |  |  | 可用/不可用 |

## 图文混排规则（Markdown）

- 首图放在导语后，优先横图
- 段中图放在对应段落后，不跨主题插图
- 图注格式统一：`图N：说明（来源：来源名称，source_id：XXX，链接：XXX）`
- 图片语法：`![alt文本](图片路径或URL)`

示例：

```markdown
![某园区光伏屋顶全景](/absolute/path/solar-plant.jpg)
*图1：某园区新增分布式光伏设施（来源：企业供图，source_id：ENV-LCA-CN-006，链接：https://www.nea.gov.cn/）*
```

## 网页截图功能（外链或下载）

当素材只提供网页且没有可用图片时，使用脚本生成截图外链或下载本地截图。

### 通用“内容匹配校验”流程（适配任意新闻类型）

每一张网页截图都必须经过以下 5 步：
- 第1步：提取本段新闻的“目标事实”（要证明什么）
- 第2步：构建截图校验卡（必含词/排除词/期望区域）
- 第3步：先做页面文本校验，再截图（失败则不截图）
- 第4步：优先 `element` 定点截图，再考虑 `fullPage`
- 第5步：统一裁剪到新闻排版尺寸（默认 `1200x720`）并人工复核图注与正文对应

可直接复制的模板： [assets/screenshot-validation-card-template.md](../assets/screenshot-validation-card-template.md)

截图校验卡字段建议：
- `目标事实` `must_keywords` `exclude_keywords` `capture_opts` `source_id` `对应正文段落`

按新闻类型配置关键词建议：
- 简报：主体机构 + 事件名 + 日期/时间
- 深度报道：争议焦点词 + 指标词 + 对照词
- 专题采访：受访对象 + 核心问题词 + 回应词
- 实时新闻：时间戳 + 状态词（更新/通报/修正）
- 人物专访：人名 + 头衔 + 观点关键词

命中策略建议：
- `--match-mode all`：高精度（政策、财务、合规、定价场景）
- `--match-mode any`：高召回（突发/追踪线索初筛）
- `--match-mode threshold --min-keyword-hit N`：平衡模式（中长稿常用）
- `--audit-deny-keywords`：全局拦截词，命中即不通过（如 `blocked,captcha,access denied`）

#### 示例1：严格模式（推荐发布前）

```bash
python3 scripts/capture_web_screenshots.py \
  --entry "SimaPro计划卡片区|ENV-LCA-VENDOR-002|SimaPro|https://simapro.com/plans/|element=.plans-pricing-overview-template__items;waitForSelector=.plans-pricing-overview-template__items|simapro craft,compare plans,contact us for a quote|404,access denied|size=1200x720;mode=cover;anchor=top" \
  --entry "ecoinvent企业许可表|ENV-LCA-LCIDB-001|ecoinvent|https://ecoinvent.org/licenses/enterprise/|element=.licenses-table-container;waitForSelector=.licenses-table-container|licensing & pricing,enterprise-wide,subscription|404,not found|size=1200x720;mode=contain;anchor=top" \
  --provider microlink \
  --match-mode all \
  --audit-deny-keywords "blocked,access denied,verify you are human,captcha" \
  --strict-validation \
  --layout-size 1200x720 \
  --layout-mode cover \
  --layout-anchor center \
  --audit-report outputs/screenshots/news-images-audit.json \
  --markdown-out outputs/screenshots/news-images.md
```

`--entry` 字段格式：
- `label|source_id|source_name|page_url|capture_opts|keywords|exclude_keywords|layout_opts`
- `capture_opts` 支持 `key=value;key=value`，例如 `element=.licenses-table-container;waitForSelector=.licenses-table-container`
- `keywords`（必含关键词）用逗号分隔
- `exclude_keywords`（排除词）用逗号分隔，命中则校验失败
- `layout_opts` 可覆盖单图裁剪参数，如 `size=1200x720;mode=cover;anchor=top`

#### 示例2：阈值模式（适合复杂议题）

```bash
python3 scripts/capture_web_screenshots.py \
  --entry "某政策发布页|POL-001|某机构|https://example.com/policy|element=.policy-body|政策,发布时间,实施范围,解读|404,access denied|size=1200x720;mode=cover;anchor=top" \
  --provider microlink \
  --match-mode threshold \
  --min-keyword-hit 3 \
  --audit-deny-keywords "blocked,captcha,access denied" \
  --strict-validation \
  --markdown-out outputs/screenshots/policy-images.md
```

如需保证预览稳定，建议下载到本地并在稿件中使用绝对路径：

```bash
python3 scripts/capture_web_screenshots.py \
  --entry "SimaPro计划卡片区|ENV-LCA-VENDOR-002|SimaPro|https://simapro.com/plans/|element=.plans-pricing-overview-template__items;waitForSelector=.plans-pricing-overview-template__items|simapro craft,compare plans,contact us for a quote|404,access denied|size=1200x720;mode=cover;anchor=top" \
  --entry "ecoinvent企业许可表|ENV-LCA-LCIDB-001|ecoinvent|https://ecoinvent.org/licenses/enterprise/|element=.licenses-table-container;waitForSelector=.licenses-table-container|licensing & pricing,enterprise-wide,subscription|404,not found|size=1200x720;mode=contain;anchor=top" \
  --provider microlink \
  --match-mode all \
  --audit-deny-keywords "blocked,access denied,verify you are human,captcha" \
  --strict-validation \
  --download \
  --out-dir "/abs/path/to/screenshots" \
  --audit-report "/abs/path/to/screenshots/news-images-audit.json" \
  --markdown-out "/abs/path/to/screenshots/news-images-local.md"
```

## 版式节奏建议

- 快讯：1-2张图
- 标准新闻：2-4张图
- 深度稿：4-8张图（含数据图/时间线图）

图片与段落比例建议：
- 每300-500字插入1张有效信息图
- 连续两张图之间至少有1段实质性文字

## 图片审校清单

发布前逐图检查：
- 图片内容与对应段落事实一致
- 图注无错别字、无歧义、时间地点准确
- 来源、source_id、链接/路径、授权信息完整
- alt文本可读，能独立描述关键信息
- 未暴露隐私信息（车牌、人脸、联系方式等）
- 未命中拦截页/验证码/错误页特征词（如 `blocked` `captcha` `access denied`）

## 常见问题与修复

- 问题：图片与文字主题不一致
  修复：替换为同主题图或移动到对应段落
- 问题：无版权证明
  修复：改用可商用图库或删除该图
- 问题：图注过于口号化
  修复：改为可核实描述，加入来源
