# News Skills Workspace

本项目是一个以 `skills/` 为核心的新闻生产工作区，目标是把“选题 -> 采集 -> 核验 -> 写作 -> 配图 -> 发布”流程标准化、可复用化。

当前重点 skill：
- `skills/news-writing`

非技术同事简版说明：
- [README_NONTECH.md](README_NONTECH.md)

---

## 一、整体框架设计

`news-writing` 采用“配置/知识/模板/执行脚本/产物”分层架构：

1. **流程编排层（Orchestration）**
   - 入口：`skills/news-writing/SKILL.md`
   - 作用：定义全流程顺序、门禁规则、输出格式、发布策略

2. **知识与规则层（References）**
   - 目录：`skills/news-writing/references/`
   - 作用：沉淀类型路由、白名单数据源、核验规范、图文规范、API 文档映射

3. **模板层（Assets）**
   - 目录：`skills/news-writing/assets/`
   - 作用：按新闻类型输出统一结构（简报/深度/采访/实时/专访），并提供截图校验卡

4. **执行层（Scripts）**
   - 目录：`skills/news-writing/scripts/`
   - 作用：将高频、易错流程脚本化（截图审核裁剪、站点管理、API 发布）

5. **产物层（Outputs）**
   - 目录：`skills/news-writing/outputs/`
   - 作用：保存截图、发布配置、审计报告、稿件中间件与最终稿

模块索引：`skills/news-writing/references/skill-module-map.md`

---

## 二、当前已实现功能

### 1) 新闻类型自动路由与模板写作
- 支持：`简报` / `深度报道` / `专题采访` / `实时新闻` / `人物专访`
- 可对“仅给话题”的输入自动判型并选择模板
- 支持发布版（少标题）与编辑版（结构化）输出

### 2) 白名单取材与事实核验
- 按领域-子领域-主题白名单取材（当前含环境与能源/LCA方向）
- 事实必须挂载 `source_id` 与来源路径
- 关键事实支持双来源交叉核验与待确认清单分流

### 3) 图片审核与截图标准化
- 网页截图支持内容匹配校验（must/exclude）
- 支持拦截页审查（如 `blocked` / `captcha` / `access denied`）
- 支持统一新闻排版裁剪（默认 `1200x720`）
- 支持输出截图审计报告（audit report）

### 4) API 发布与站点管理
- 已集成 `lca-echo` 发布链路
- 支持站点配置管理（增删改查、默认站点）
- 支持 `dry-run` 预检与正式发布
- 发布后输出结构化回执（`post_id`、`post_url` 等）

### 5) 链接与图注质量控制
- 图注支持可点击链接格式
- 避免将“内容校验说明”拼接进 URL 导致跳转错误

---

## 三、关键脚本

### `capture_web_screenshots.py`
路径：`skills/news-writing/scripts/capture_web_screenshots.py`  
用途：网页截图 + 内容审核 + 排版裁剪 + 审计报告输出

### `manage_publish_sites.py`
路径：`skills/news-writing/scripts/manage_publish_sites.py`  
用途：发布站点配置管理（默认站点、接口路径、认证策略等）

### `publish_news_via_api.py`
路径：`skills/news-writing/scripts/publish_news_via_api.py`  
用途：按站点配置进行 `dry-run` 和正式发布，输出发布回执

---

## 四、快速上手

### 1) 初始化发布站点配置
```bash
python3 skills/news-writing/scripts/manage_publish_sites.py init
python3 skills/news-writing/scripts/manage_publish_sites.py list
```

### 2) 截图（审核 + 裁剪）
```bash
python3 skills/news-writing/scripts/capture_web_screenshots.py \
  --entry "示例图|SRC-001|示例来源|https://example.com|fullPage=true|keyword1,keyword2|blocked,captcha|size=1200x720;mode=cover;anchor=top" \
  --strict-validation \
  --download \
  --out-dir "skills/news-writing/outputs/screenshots/demo" \
  --audit-report "skills/news-writing/outputs/screenshots/demo/audit.json"
```

### 3) 发布前预检
```bash
python3 skills/news-writing/scripts/publish_news_via_api.py \
  --site-id lca-echo \
  --title "测试标题" \
  --community-name "LCA_Software" \
  --author-name "News Desk" \
  --content-file "/absolute/path/to/article.md" \
  --extract-images-from-markdown \
  --dry-run
```

### 4) 正式发布
```bash
python3 skills/news-writing/scripts/publish_news_via_api.py \
  --site-id lca-echo \
  --title "测试标题" \
  --community-name "LCA_Software" \
  --author-name "News Desk" \
  --content-file "/absolute/path/to/article.md" \
  --extract-images-from-markdown
```

---

## 五、目录说明

- `skills/`：核心技能目录（版本化维护）
- `branding/`：非技能目录（已忽略）
- `.gitignore`：已忽略 `.DS_Store` 与 `branding/`

---

## 六、维护建议

- 新增能力优先落到 `scripts/` + `references/`，避免在 `SKILL.md` 堆叠细节
- 规则变更先更新 `references/`，再同步 `SKILL.md` 流程入口
- 发布链路变更先更新 `outputs/publishing/sites.json` 与 API 参考
