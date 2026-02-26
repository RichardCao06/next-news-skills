# LCA Echo API 发布参考

更新时间：2026-02-26  
文档来源：`https://lca-echo.lovable.app/api-docs`

## 1) 已确认基础信息

- 文档页展示的 `Base URL`：  
  `https://meezfvpwfzzpibkecrvj.supabase.co/functions/v1/api`
- 公开发布帖子接口（无需认证）：  
  `POST /api/posts`（文档示例 cURL 实际调用为 `${BaseURL}/posts`）
- 社区列表接口（用于按名称解析 `community_id`）：  
  `GET /api/communities`（文档示例 cURL 实际调用为 `${BaseURL}/communities`）

## 2) 关键接口（发布链路）

### 2.1 获取社区列表

- 方法：`GET`
- URL：`{BaseURL}/communities`
- 作用：获取 `community_id` 与社区名称映射

响应示例（节选）：

```json
{
  "data": [
    {
      "id": "a1000000-0000-0000-0000-000000000001",
      "name": "LCA_China"
    }
  ]
}
```

### 2.2 创建帖子（发布新闻）

- 方法：`POST`
- URL：`{BaseURL}/posts`
- Content-Type：`application/json`
- 必填字段：
  - `title` (string)
  - `community_id` (uuid)
  - `author_name` (string)
- 可选字段：
  - `content` (string)
  - `images` (string[])

请求示例：

```json
{
  "title": "社区端LCA工具信任与成本争议持续发酵",
  "community_id": "a1000000-0000-0000-0000-000000000005",
  "author_name": "LCA News Desk",
  "content": "新闻正文……",
  "images": [
    "https://example.com/figure-1.png"
  ]
}
```

成功响应示例：

```json
{
  "data": {
    "id": "uuid"
  }
}
```

## 3) 可用于发布后核验的公开接口

- `GET {BaseURL}/posts`：查看最新帖子列表
- `GET {BaseURL}/posts/{id}`：查看指定帖子详情

## 4) 与 skill 脚本的对应关系

- 站点管理：`scripts/manage_publish_sites.py`
  - 管理多个发布站点（增删改查、默认站点）
- 新闻发布：`scripts/publish_news_via_api.py`
  - 读取站点配置
  - 解析 `community_name -> community_id`
  - 调用创建帖子接口发布新闻

## 5) 注意事项

- 若目标站点需要认证，优先通过站点配置中的 `auth` 进行环境变量注入，不在命令行明文写 token。
- 发布前先执行 `--dry-run` 预检 payload，确认 `community_id`、`title`、`images` 正确。
- 若文档更新导致接口变化，先更新 `sites.json` 里的 `routes` 与认证策略，再发布。
