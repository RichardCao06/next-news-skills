# Data Source Whitelist

## 领域路径

- 一级领域：`环境与能源`
- 二级领域：`LCA 生命周期`

## 使用规则

1. 仅从本清单中的 `source_id` 取材；白名单外来源只可作为线索，不可直接入稿。
2. 每条事实至少绑定 1 个 `A` 级来源；使用 `B/C` 级来源时，必须配套 `A` 级来源交叉核验。
3. 素材台账必须记录：`来源层级路径`、`source_id`、`来源网址`、`引用片段/指标`、`抓取时间`。
4. 当清单无法覆盖任务信息时，在“待补充信息”中提出新增来源申请，不擅自扩展来源。
5. 涉及中国“双碳”主题时，优先使用 `ENV-LCA-CN-*` 数据源，且至少包含 1 个 `A` 级中国官方来源。
6. 社交论坛类来源（`ENV-LCA-SOCIAL-*`）仅用于线索发现与观点观察，不可单独作为事实依据，必须回溯到 `A/B` 级来源核验。

等级定义：
- `A`：标准/官方数据库/官方披露，可直接作为事实依据。
- `B`：权威机构报告，可作为事实补充与背景解释。
- `C`：学术与行业研究，用于方法解释与趋势补充。

## 三级领域与数据源清单

### 1) 方法标准与核算框架（METHOD）

| source_id | 层级路径 | 数据源 | 网址 | 机构 | 等级 | 典型用途 |
|---|---|---|---|---|---|---|
| ENV-LCA-METHOD-001 | 环境与能源>LCA生命周期>方法标准 | ISO 14040 | https://www.iso.org/search.html?q=ISO%2014040 | ISO | A | 生命周期评价原则与框架定义 |
| ENV-LCA-METHOD-002 | 环境与能源>LCA生命周期>方法标准 | ISO 14044 | https://www.iso.org/search.html?q=ISO%2014044 | ISO | A | 生命周期评价要求与指南 |
| ENV-LCA-METHOD-003 | 环境与能源>LCA生命周期>方法标准 | ISO 14067 | https://www.iso.org/search.html?q=ISO%2014067 | ISO | A | 产品碳足迹核算与报告 |
| ENV-LCA-METHOD-004 | 环境与能源>LCA生命周期>方法标准 | GHG Protocol Product Standard | https://ghgprotocol.org/product-standard | WRI/WBCSD | A | 产品层面温室气体核算口径 |
| ENV-LCA-METHOD-005 | 环境与能源>LCA生命周期>方法标准 | PEF/OEF 方法体系 | https://environment.ec.europa.eu/topics/circular-economy/product-environmental-footprint_en | European Commission | A | 欧盟产品/组织环境足迹方法 |
| ENV-LCA-METHOD-006 | 环境与能源>LCA生命周期>方法标准 | Life Cycle Initiative 指南 | https://www.lifecycleinitiative.org/ | UNEP/SETAC | B | LCA 方法更新、术语解释 |

### 2) 生命周期清单数据库（LCI-DB）

| source_id | 层级路径 | 数据源 | 网址 | 机构 | 等级 | 典型用途 |
|---|---|---|---|---|---|---|
| ENV-LCA-LCIDB-001 | 环境与能源>LCA生命周期>LCI数据库 | ecoinvent | https://ecoinvent.org/ | ecoinvent Association | A | 多行业背景数据库与过程数据 |
| ENV-LCA-LCIDB-002 | 环境与能源>LCA生命周期>LCI数据库 | USLCI Database | https://www.nrel.gov/lci/ | NREL | A | 美国本土生命周期清单数据 |
| ENV-LCA-LCIDB-003 | 环境与能源>LCA生命周期>LCI数据库 | Federal LCA Commons | https://www.lcacommons.gov/ | US EPA | A | 美国联邦生命周期数据库门户 |
| ENV-LCA-LCIDB-004 | 环境与能源>LCA生命周期>LCI数据库 | AGRIBALYSE | https://agribalyse.ademe.fr/ | ADEME | A | 农食链生命周期清单数据 |
| ENV-LCA-LCIDB-005 | 环境与能源>LCA生命周期>LCI数据库 | ProBas | https://www.probas.umweltbundesamt.de/php/index.php | UBA Germany | A | 德国过程与材料环境数据 |
| ENV-LCA-LCIDB-006 | 环境与能源>LCA生命周期>LCI数据库 | ÖKOBAUDAT | https://www.oekobaudat.de/en.html | Germany (construction) | A | 建材与建筑产品环境数据 |
| ENV-LCA-LCIDB-007 | 环境与能源>LCA生命周期>LCI数据库 | IDEA | https://www.idea-lca.com/ | AIST/JEMAI | B | 日本产业过程数据库 |
| ENV-LCA-LCIDB-008 | 环境与能源>LCA生命周期>LCI数据库 | CLCD | https://www.clcd.cn/ | 中国生命周期数据库（需授权） | B | 中国场景背景参数与行业清单 |

### 3) 能源与排放因子数据库（FACTOR-DB）

| source_id | 层级路径 | 数据源 | 网址 | 机构 | 等级 | 典型用途 |
|---|---|---|---|---|---|---|
| ENV-LCA-FACTOR-001 | 环境与能源>LCA生命周期>排放因子 | IPCC EFDB | https://www.ipcc-nggip.iges.or.jp/EFDB/main.php | IPCC | A | 温室气体排放因子参考 |
| ENV-LCA-FACTOR-002 | 环境与能源>LCA生命周期>排放因子 | eGRID | https://www.epa.gov/egrid | US EPA | A | 美国电网排放因子 |
| ENV-LCA-FACTOR-003 | 环境与能源>LCA生命周期>排放因子 | UK GHG Conversion Factors | https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting | UK DESNZ | A | 能源与活动数据换算因子 |
| ENV-LCA-FACTOR-004 | 环境与能源>LCA生命周期>排放因子 | UNFCCC GHG Inventory Data | https://di.unfccc.int/ | UNFCCC | A | 国家温室气体清单时序数据 |
| ENV-LCA-FACTOR-005 | 环境与能源>LCA生命周期>能源统计 | IEA Data and Statistics | https://www.iea.org/data-and-statistics | IEA | B | 能源平衡与国际对比数据 |
| ENV-LCA-FACTOR-006 | 环境与能源>LCA生命周期>能源统计 | U.S. EIA Open Data | https://www.eia.gov/opendata/ | U.S. EIA | B | 美国能源供需与价格数据 |
| ENV-LCA-FACTOR-007 | 环境与能源>LCA生命周期>能源统计 | Eurostat Energy Database | https://ec.europa.eu/eurostat/web/energy/data/database | Eurostat | B | 欧盟能源结构与强度数据 |
| ENV-LCA-FACTOR-008 | 环境与能源>LCA生命周期>能源统计 | IRENA Data & Statistics | https://www.irena.org/Data | IRENA | B | 可再生能源装机与发电统计 |

### 4) 政策披露与产品声明（POLICY-EPD）

| source_id | 层级路径 | 数据源 | 网址 | 机构 | 等级 | 典型用途 |
|---|---|---|---|---|---|---|
| ENV-LCA-POLICY-001 | 环境与能源>LCA生命周期>政策披露 | EU EPD (ECO Platform) | https://www.eco-platform.org/ | ECO Platform | A | 欧洲 EPD 项目与产品声明核验 |
| ENV-LCA-POLICY-002 | 环境与能源>LCA生命周期>政策披露 | The International EPD System | https://www.environdec.com/ | EPD International AB | A | 国际 EPD 注册信息 |
| ENV-LCA-POLICY-003 | 环境与能源>LCA生命周期>政策披露 | EPA GHGRP | https://www.epa.gov/ghgreporting | US EPA | A | 企业温室气体排放披露数据 |
| ENV-LCA-POLICY-004 | 环境与能源>LCA生命周期>政策披露 | CDP Disclosure | https://www.cdp.net/en/disclosure | CDP | B | 企业环境披露与转型进展 |
| ENV-LCA-POLICY-005 | 环境与能源>LCA生命周期>政策披露 | SEC Climate Disclosures | https://www.sec.gov/spotlight/climate-esg | U.S. SEC | B | 上市公司气候相关披露材料 |
| ENV-LCA-POLICY-006 | 环境与能源>LCA生命周期>政策披露 | ESRS/EFRAG Guidance | https://www.efrag.org/en/sustainability-reporting/esrs | EFRAG | B | 欧盟可持续披露实施口径 |

### 5) 学术与技术评审（LITERATURE）

| source_id | 层级路径 | 数据源 | 网址 | 机构 | 等级 | 典型用途 |
|---|---|---|---|---|---|---|
| ENV-LCA-LIT-001 | 环境与能源>LCA生命周期>学术评审 | The International Journal of Life Cycle Assessment | https://link.springer.com/journal/11367 | Springer | C | LCA 方法与案例研究 |
| ENV-LCA-LIT-002 | 环境与能源>LCA生命周期>学术评审 | Journal of Cleaner Production | https://www.sciencedirect.com/journal/journal-of-cleaner-production | Elsevier | C | 清洁生产与生命周期研究 |
| ENV-LCA-LIT-003 | 环境与能源>LCA生命周期>学术评审 | Resources, Conservation & Recycling | https://www.sciencedirect.com/journal/resources-conservation-and-recycling | Elsevier | C | 资源循环与环境影响研究 |
| ENV-LCA-LIT-004 | 环境与能源>LCA生命周期>学术评审 | Nature Sustainability | https://www.nature.com/natsustain/ | Nature Portfolio | C | 高影响力可持续研究 |
| ENV-LCA-LIT-005 | 环境与能源>LCA生命周期>学术评审 | Joule | https://www.cell.com/joule/home | Cell Press | C | 能源系统与减排技术评估 |

### 6) 中国双碳与碳数据（CN-DOUBLE-CARBON）

| source_id | 层级路径 | 数据源 | 网址 | 机构 | 等级 | 典型用途 |
|---|---|---|---|---|---|---|
| ENV-LCA-CN-001 | 环境与能源>LCA生命周期>中国双碳政策 | 生态环境部应对气候变化专题 | https://www.mee.gov.cn/ywgz/ydqhbh/ | 生态环境部 | A | 全国碳市场政策、核算核查规范、扩围文件 |
| ENV-LCA-CN-002 | 环境与能源>LCA生命周期>中国碳市场数据 | 全国碳市场管理平台 | https://www.cets.org.cn/ | 全国碳市场管理平台 | A | 重点排放单位名录、履约与管理信息 |
| ENV-LCA-CN-003 | 环境与能源>LCA生命周期>中国碳市场数据 | 全国碳排放权交易系统（上海环境能源交易所） | https://www.cneeex.com/ | 上海环境能源交易所 | A | CEA 市场行情、交易公告与规则 |
| ENV-LCA-CN-004 | 环境与能源>LCA生命周期>中国自愿减排 | 全国温室气体自愿减排（CCER）专题 | https://www.mee.gov.cn/ywgz/ydqhbh/wsqtkz/ | 生态环境部 | A | CCER 方法学、登记进展、政策口径 |
| ENV-LCA-CN-005 | 环境与能源>LCA生命周期>中国宏观与行业活动数据 | 国家数据 | https://data.stats.gov.cn/ | 国家统计局 | A | 能源消费、工业与地区活动数据基线 |
| ENV-LCA-CN-006 | 环境与能源>LCA生命周期>中国能源统计 | 国家能源局 | https://www.nea.gov.cn/ | 国家能源局 | A | 电力装机、发电结构、能源运行统计 |
| ENV-LCA-CN-007 | 环境与能源>LCA生命周期>中国碳足迹因子 | 2024年全国电力碳足迹因子公告 | https://www.mee.gov.cn/xxgk2018/xxgk/xxgk01/202510/t20251024_1130734.html | 生态环境部/国家统计局/国家能源局 | A | 产品与组织核算电力排放因子引用 |
| ENV-LCA-CN-008 | 环境与能源>LCA生命周期>中国标准规范 | 国家标准全文公开系统 | https://openstd.samr.gov.cn/bzgk/std/ | 国家市场监管总局/国家标准委 | A | 检索 GB/T 24040、GB/T 24044 等 LCA/碳核算标准 |
| ENV-LCA-CN-009 | 环境与能源>LCA生命周期>中国LCI数据库 | 中国生命周期基础数据库（CLCD） | https://www.clcd.cn/ | CLCD（需授权） | B | 中国本地化生命周期清单参数 |
| ENV-LCA-CN-010 | 环境与能源>LCA生命周期>中国碳核算数据库 | 中国碳核算数据库（CEADs） | https://www.ceads.net.cn/ | 清华大学团队 | B | 省市/行业碳排放清单与历史序列分析 |
| ENV-LCA-CN-011 | 环境与能源>LCA生命周期>中国产品环境声明 | EPD促进中心（EPD中国） | https://www.epdchina.cn/ | EPD促进中心 | B | 中国产品环境声明与 LCA 披露案例 |
| ENV-LCA-CN-012 | 环境与能源>LCA生命周期>中国双碳政策 | 中国政府网政策库 | https://www.gov.cn/zhengce/ | 国务院及各部委 | A | 双碳顶层政策与部门政策原文检索 |

### 7) LCA/碳数据企业工具与咨询机构（VENDOR-CONSULTING）

| source_id | 层级路径 | 数据源 | 网址 | 机构 | 等级 | 典型用途 |
|---|---|---|---|---|---|---|
| ENV-LCA-VENDOR-001 | 环境与能源>LCA生命周期>企业工具与数据库 | CarbonMinds | https://www.carbonminds.com/ | Carbon Minds GmbH | B | LCA/PCF 数据、方法与行业洞察 |
| ENV-LCA-VENDOR-002 | 环境与能源>LCA生命周期>企业工具与数据库 | SimaPro | https://simapro.com/ | PRé Sustainability | B | LCA 建模工具与方法资料 |
| ENV-LCA-VENDOR-003 | 环境与能源>LCA生命周期>企业工具与数据库 | Sphera (GaBi) | https://sphera.com/life-cycle-assessment-lca-software/ | Sphera | B | GaBi LCA 软件与数据库信息 |
| ENV-LCA-VENDOR-004 | 环境与能源>LCA生命周期>企业工具与数据库 | openLCA | https://www.openlca.org/ | GreenDelta | B | 开源 LCA 工具与生态 |
| ENV-LCA-VENDOR-005 | 环境与能源>LCA生命周期>企业工具与数据库 | One Click LCA | https://oneclicklca.com/ | One Click LCA | B | 建筑与制造业 LCA/EPD 场景 |
| ENV-LCA-VENDOR-006 | 环境与能源>LCA生命周期>企业工具与数据库 | Ecochain | https://ecochain.com/ | Ecochain | B | 产品碳足迹与供应链碳管理 |
| ENV-LCA-VENDOR-007 | 环境与能源>LCA生命周期>咨询机构 | Carbon Trust | https://www.carbontrust.com/ | Carbon Trust | B | 碳核算方法、转型咨询与案例 |
| ENV-LCA-VENDOR-008 | 环境与能源>LCA生命周期>咨询机构 | ERM Sustainability | https://www.erm.com/ | ERM | B | 企业 ESG/碳管理与生命周期咨询 |
| ENV-LCA-VENDOR-009 | 环境与能源>LCA生命周期>咨询机构 | South Pole | https://www.southpole.com/ | South Pole | B | 碳项目、核算方法与市场洞察 |
| ENV-LCA-VENDOR-010 | 环境与能源>LCA生命周期>咨询机构 | Quantis | https://quantis.com/ | Quantis | B | 科学碳目标与 LCA 咨询洞察 |
| ENV-LCA-VENDOR-011 | 环境与能源>LCA生命周期>企业资讯 | Carbon Brief | https://www.carbonbrief.org/ | Carbon Brief | B | 碳政策与气候数据新闻解读 |
| ENV-LCA-VENDOR-012 | 环境与能源>LCA生命周期>企业资讯 | edie | https://www.edie.net/ | edie | C | 可持续与净零行业资讯线索 |

### 8) 社交论坛与社区板块（SOCIAL-COMMUNITY）

| source_id | 层级路径 | 数据源 | 网址 | 机构 | 等级 | 典型用途 |
|---|---|---|---|---|---|---|
| ENV-LCA-SOCIAL-001 | 环境与能源>LCA生命周期>社交社区>Reddit | r/LCA | https://www.reddit.com/r/LCA/ | Reddit 社区 | C | LCA 工具实践、问题线索与案例讨论 |
| ENV-LCA-SOCIAL-002 | 环境与能源>LCA生命周期>社交社区>Reddit | r/sustainability | https://www.reddit.com/r/sustainability/ | Reddit 社区 | C | 可持续议题趋势与外部线索 |
| ENV-LCA-SOCIAL-003 | 环境与能源>LCA生命周期>社交社区>Reddit | r/climate | https://www.reddit.com/r/climate/ | Reddit 社区 | C | 气候政策与数据话题跟踪 |
| ENV-LCA-SOCIAL-004 | 环境与能源>LCA生命周期>社交社区>LinkedIn | #lifecycleassessment | https://www.linkedin.com/feed/hashtag/lifecycleassessment/ | LinkedIn | C | LCA 行业动态与机构发声 |
| ENV-LCA-SOCIAL-005 | 环境与能源>LCA生命周期>社交社区>LinkedIn | #carbonfootprint | https://www.linkedin.com/feed/hashtag/carbonfootprint/ | LinkedIn | C | 碳足迹方法、工具更新线索 |
| ENV-LCA-SOCIAL-006 | 环境与能源>LCA生命周期>社交社区>LinkedIn | #decarbonization | https://www.linkedin.com/feed/hashtag/decarbonization/ | LinkedIn | C | 减碳项目、行业案例线索 |
| ENV-LCA-SOCIAL-007 | 环境与能源>LCA生命周期>社交社区>Facebook | LCA 相关群组检索页 | https://www.facebook.com/search/groups/?q=life%20cycle%20assessment | Facebook | C | 检索 LCA 群组与讨论线索 |
| ENV-LCA-SOCIAL-008 | 环境与能源>LCA生命周期>社交社区>Facebook | Carbon Footprint 相关群组检索页 | https://www.facebook.com/search/groups/?q=carbon%20footprint | Facebook | C | 检索碳足迹主题群组线索 |
| ENV-LCA-SOCIAL-009 | 环境与能源>LCA生命周期>社交社区>X(Twitter) | #lca 话题 | https://x.com/hashtag/lca | X (Twitter) | C | LCA 从业者动态与工具更新线索 |
| ENV-LCA-SOCIAL-010 | 环境与能源>LCA生命周期>社交社区>X(Twitter) | #carbonfootprint 话题 | https://x.com/hashtag/carbonfootprint | X (Twitter) | C | 碳足迹方法与案例讨论线索 |
| ENV-LCA-SOCIAL-011 | 环境与能源>LCA生命周期>社交社区>X(Twitter) | #decarbonization 话题 | https://x.com/hashtag/decarbonization | X (Twitter) | C | 脱碳政策与项目进展线索 |
| ENV-LCA-SOCIAL-012 | 环境与能源>LCA生命周期>社交社区>知乎 | LCA 检索页 | https://www.zhihu.com/search?type=content&q=LCA | 知乎 | C | 中文 LCA 问答线索与术语辨析 |
| ENV-LCA-SOCIAL-013 | 环境与能源>LCA生命周期>社交社区>知乎 | 碳足迹 检索页 | https://www.zhihu.com/search?type=content&q=%E7%A2%B3%E8%B6%B3%E8%BF%B9 | 知乎 | C | 碳足迹概念、案例与争议线索 |
| ENV-LCA-SOCIAL-014 | 环境与能源>LCA生命周期>社交社区>知乎 | 双碳 检索页 | https://www.zhihu.com/search?type=content&q=%E5%8F%8C%E7%A2%B3 | 知乎 | C | 双碳政策与行业实践线索 |
| ENV-LCA-SOCIAL-015 | 环境与能源>LCA生命周期>社交社区>微信公众号 | 微信公众号平台入口 | https://mp.weixin.qq.com/ | 微信公众号 | C | 公众号原文核验与发布主体识别 |
| ENV-LCA-SOCIAL-016 | 环境与能源>LCA生命周期>社交社区>微信公众号 | 搜狗微信检索（LCA） | https://weixin.sogou.com/weixin?type=2&query=LCA | 搜狗微信 | C | 检索 LCA 相关文章与账号线索 |
| ENV-LCA-SOCIAL-017 | 环境与能源>LCA生命周期>社交社区>微信公众号 | 搜狗微信检索（双碳） | https://weixin.sogou.com/weixin?type=2&query=%E5%8F%8C%E7%A2%B3 | 搜狗微信 | C | 检索双碳政策解读与行业案例线索 |
| ENV-LCA-SOCIAL-018 | 环境与能源>LCA生命周期>社交社区>微信公众号 | 搜狗微信检索（碳足迹） | https://weixin.sogou.com/weixin?type=2&query=%E7%A2%B3%E8%B6%B3%E8%BF%B9 | 搜狗微信 | C | 检索碳足迹核算方法与应用线索 |

## 输出时的最小字段要求

引用上述来源时，至少输出：
- `source_id`
- `来源层级路径`
- `来源网址`
- `来源名称`
- `引用事实`
- `核验状态`（已核验/待核验/存疑）
