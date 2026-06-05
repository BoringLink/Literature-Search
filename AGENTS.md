# Literature Search Agent - Project Knowledge Base

**Generated:** 2026-06-05
**Commit:** main branch
**Project Type:** Academic Literature Search Agent Skill

## OVERVIEW

学术文献检索 Agent Skill，集成 Serp API、百度千帆学术 API、知网研学开放平台 API、ArXiv API、Semantic Scholar API、Core API、OpenAlex API 进行多源文献检索。Python 3.8+ 项目，1700 行代码，10 个核心模块。

## STRUCTURE

```
literature-search/
├── python/literature_search/  # 核心搜索包（11 个 Python 文件，1700 行）
│   ├── __init__.py            # 包入口，导出 LiteratureSearcher
│   ├── __main__.py            # 支持 python -m literature_search
│   └── *_searcher.py          # 各 API 源客户端
├── scripts/                   # 旧版本（向后兼容）
├── references/                # API 文档、查询示例、分类参考
├── outputs/                   # 搜索结果输出目录
├── SKILL.md                   # Agent Skill 元数据和指令
├── README.md                  # 用户使用指南
├── package.json               # npm 发布配置
├── .claude-skill.json         # Claude Code Skill 元数据
├── install-skill.js           # 安装脚本
└── uninstall-skill.js         # 卸载脚本
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| 执行文献搜索 | `python/literature_search/combined_search.py` | 主入口，统一接口 |
| 添加新 API 源 | `python/literature_search/` 下新建 `*_searcher.py` | 遵循现有模式 |
| 修改输出格式 | `python/literature_search/result_formatter.py` | Markdown/JSON/CSV/BibTeX |
| API 密钥配置 | `.env.example` + 环境变量 | 6 个 API 需要密钥（Semantic Scholar, SerpApi, Core, 知网，百度千帆，OpenAlex） |
| 查询示例 | `references/query_examples.md` | 高级查询模式 |
| arXiv 分类 | `references/arxiv_categories.md` | CS/ML/AI 分类表 |
| API 限制 | `references/api_limits.md` | 速率限制和最佳实践 |
| npm 安装配置 | `package.json` + `.claude-skill.json` | npm 发布和多平台安装 |

## CODE MAP

| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `LiteratureSearcher` | Class | `python/literature_search/combined_search.py:15` | 主编排器，协调多 API 搜索 |
| `ArxivSearcher` | Class | `python/literature_search/arxiv_searcher.py` | arXiv OAI-PMH API 客户端 |
| `SemanticSearcher` | Class | `python/literature_search/semantic_searcher.py` | Semantic Scholar REST API |
| `SerpApiSearcher` | Class | `python/literature_search/serpapi_searcher.py` | Google Scholar via SerpApi |
| `CNKISearcher` | Class | `python/literature_search/cnki_searcher.py` | 知网研学 API（JWT 认证，合并版） |
| `BaiduScholarSearcher` | Class | `python/literature_search/baidu_scholar_searcher.py` | 百度千帆学术 API |
| `CoreSearcher` | Class | `python/literature_search/core_searcher.py` | Core API 开放获取论文 |
| `OpenAlexSearcher` | Class | `python/literature_search/openalex_searcher.py` | OpenAlex 开放学术目录 |
| `ResultFormatter` | Class | `python/literature_search/result_formatter.py` | 结果格式转换 |

## CONVENTIONS

### API 客户端模式
- 每个 API 源独立 `*_searcher.py` 文件
- 统一接口：`search(keywords, year_min, year_max, ...)` → `List[Dict]`
- 错误处理：捕获 API 异常，返回空列表不中断其他源
- 速率限制：每个客户端内置延迟（arXiv 3 秒，Semantic 1 秒）

### 输出命名
- 格式：`papers_{关键词}_{时间戳}.{格式}`
- 示例：`papers_machine_learning_20260421_225100.json`

### 环境变量
```bash
SEMANTIC_SCHOLAR_KEY=xxx
SERPAPI_KEY=xxx
CORE_API_KEY=xxx
CNKI_USERNAME=xxx
CNKI_PASSWORD=xxx
BAIDU_API_KEY=xxx
OPENALEX_API_KEY=xxx
```

## ANTI-PATTERNS

- ❌ 直接修改 `combined_search.py` 的 API 初始化逻辑 - 应添加新 `*_searcher.py`
- ❌ 硬编码 API 密钥 - 必须使用环境变量
- ❌ 跳过错误处理 - 每个 API 调用必须 try/except
- ❌ 返回未解析的原始响应 - 必须标准化为统一字典格式
- ❌ 并发调用同一 API - 遵守速率限制，顺序调用

## UNIQUE STYLES

### 多源融合
- 默认同时搜索所有可用 API
- 通过 `sources` 参数指定子集：`sources=["arxiv", "semantic"]`
- 自动去重：基于标题 + 年份 + 作者指纹

### 结果标准化
所有 API 响应统一映射到：
```python
{
    "title": str,
    "authors": List[str],
    "year": int,
    "abstract": str,
    "arxiv_id": Optional[str],
    "doi": Optional[str],
    "citations": Optional[int],
    "source": str
}
```

## COMMANDS

```bash
# 安装依赖
pip install requests feedparser

# 基本搜索
python scripts/combined_search.py "deep learning" --year-min 2020 --format markdown

# 多关键词
python scripts/combined_search.py "federated learning" "privacy" --authors "Yann LeCun"

# 指定 API 源
python scripts/combined_search.py "transformer" --sources semantic --max-results 100
```

## NOTES

### API 限制
- **arXiv**: 3 秒/请求，无密钥限制
- **Semantic Scholar**: 100 请求/天（免费），需密钥提升
- **SerpApi**: 100 搜索/月（免费）
- **Core API**: 500 请求/天
- **知网**: JWT 令牌 24 小时过期，需重认证
- **百度千帆**: QPS 限制，需申请配额

### 已知问题
- 知网 API 需要有效账号密码，不支持机构登录
- 百度千帆学术 API 返回格式不稳定，需额外解析
- OpenAlex 免费层有速率限制

### 性能优化
- 结果自动保存到 `outputs/`，避免重复搜索
- 测试脚本：`scripts/test_skill.py`（已移除，需重新添加）