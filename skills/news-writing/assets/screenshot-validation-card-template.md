# 通用新闻截图校验卡（可直接复制填空）

> 用途：在截图前先定义“要证明的事实”，避免截图与正文不匹配。  
> 适用：简报 / 深度报道 / 专题采访 / 实时新闻 / 人物专访

## A. 单张截图校验卡（复制此块）

```markdown
### 截图校验卡 - [CARD_ID]
- 新闻类型：
- 对应稿件标题：
- 对应正文段落编号：
- 目标事实（一句话）：
- 证据类型（价格/许可/政策条文/时间戳/机构声明/数据指标/人物表态）：
- 来源名称：
- source_id：
- 页面URL：
- capture_opts（如 `element=.xxx;waitForSelector=.xxx` 或 `fullPage=true`）：
- layout_opts（如 `size=1200x720;mode=cover;anchor=top`）：
- must_keywords（逗号分隔）：
- exclude_keywords（逗号分隔，如 `404,access denied,not found`）：
- 匹配模式（`all` / `any` / `threshold`）：
- min_keyword_hit（threshold模式必填）：
- 截图用途（首图/段中证据图/对比图）：
- 图注草案（发布版可直接用）：
- alt文本：
- 预检结果（通过/不通过）：
- 截图后复核（通过/不通过）：
- 拦截页审查（通过/不通过，关键字）：
- 失败处理记录（换URL/换element/换关键词）：
```

---

## B. 多图任务总表（复制此表）

```markdown
| 卡片ID | 目标事实 | source_id | 页面URL | must_keywords | exclude_keywords | capture_opts | layout_opts | match_mode | min_hit | 预检 | 截图复核 | 拦截审查 | 备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CARD-01 |  |  |  |  |  |  |  | all | 0 | 待检 | 待检 | 待检 |  |
| CARD-02 |  |  |  |  |  |  |  | threshold | 2 | 待检 | 待检 | 待检 |  |
```

---

## C. 直接可用命令模板（复制后替换）

```bash
python3 scripts/capture_web_screenshots.py \
  --entry "[截图标签1]|[SOURCE_ID_1]|[来源名1]|[URL_1]|[CAPTURE_OPTS_1]|[MUST_KEYWORDS_1]|[EXCLUDE_KEYWORDS_1]|[LAYOUT_OPTS_1]" \
  --entry "[截图标签2]|[SOURCE_ID_2]|[来源名2]|[URL_2]|[CAPTURE_OPTS_2]|[MUST_KEYWORDS_2]|[EXCLUDE_KEYWORDS_2]|[LAYOUT_OPTS_2]" \
  --provider microlink \
  --match-mode threshold \
  --min-keyword-hit 2 \
  --audit-deny-keywords "blocked,access denied,verify you are human,captcha" \
  --strict-validation \
  --layout-size 1200x720 \
  --download \
  --out-dir "[截图输出目录绝对路径]" \
  --markdown-out "[图文块输出绝对路径].md"
```

---

## D. 最低通过标准（发布前）

- `预检通过`：must_keywords 命中满足策略，且未命中 exclude_keywords
- `截图复核通过`：截图可见目标事实字段（标题/表头/价格/时间戳/机构名）
- `拦截审查通过`：未命中 block/captcha/access denied 等拦截页特征
- `图注可追溯`：来源名 + source_id + 页面URL 完整
- 任一项不通过：不得入稿，必须重截或替换来源
