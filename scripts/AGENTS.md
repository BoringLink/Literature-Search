# Scripts Module - Core Search Implementation

**Scope:** API integration, search orchestration, result formatting

## OVERVIEW

10 个 Python 模块，1700 行代码，实现 7 个学术 API 的搜索、编排和格式化。

## WHERE TO LOOK

| Task | File | Notes |
|------|------|-------|
| 主入口/编排 | `combined_search.py` | `LiteratureSearcher` 类，协调所有 API |
| arXiv 搜索 | `arxiv_searcher.py` | OAI-PMH 协议，feedparser 解析 |
| Semantic Scholar | `semantic_searcher.py` | REST API，引用指标 |
| Google Scholar | `serpapi_searcher.py` | SerpApi 代理 |
| 知网研学 | `cnki_searcher.py` | JWT 认证，中文文献（合并版） |
| 百度千帆 | `baidu_scholar_searcher.py` | 中文学术搜索 |
| Core API | `core_searcher.py` | 开放获取论文 |
| OpenAlex | `openalex_searcher.py` | 开放学术目录 |
| 格式化 | `result_formatter.py` | MD/JSON/CSV/BibTeX 输出 |
| 测试 | `test_skill.py` | 评估和验证 |

## CONVENTIONS

### 统一接口
```python
def search(
    keywords: str,
    year_min: Optional[int] = None,
    year_max: Optional[int] = None,
    authors: Optional[str] = None,
    max_results: int = 50
) -> List[Dict[str, Any]]
```

### 错误处理
```python
try:
    # API call
except Exception as e:
    print(f"Error calling {api_name}: {e}")
    return []  # 不中断其他源
```

### 速率限制
- arXiv: `time.sleep(3)` 每请求
- Semantic: `time.sleep(1)` 每请求
- 其他：遵循各 API 文档

## ANTI-PATTERNS

- ❌ 在 `combined_search.py` 中硬编码新 API - 应创建独立 `*_searcher.py`
- ❌ 跳过 `try/except` - API 调用必须防御性编程
- ❌ 返回原始响应 - 必须标准化为统一字典
- ❌ 并发调用同一 API - 违反速率限制
- ❌ 忽略 `max_results` 参数 - 尊重用户限制

## UNIQUE STYLES

### 标准化响应
所有 searcher 必须返回：
```python
{
    "title": str,
    "authors": List[str],
    "year": int,
    "abstract": str,
    "arxiv_id": Optional[str],
    "doi": Optional[str],
    "citations": Optional[int],
    "source": str  # 标识来源 API
}
```

### 去重逻辑
`combined_search.py` 基于 `title + year + authors` 指纹去重。

## TESTING

```bash
# 运行测试（需重新添加测试脚本）
python scripts/test_skill.py
```

## NOTES

- `core_searcher.py` 最简单（40 行），适合作为新 API 模板
- `combined_search.py` 469 行，复杂度最高，修改前需全面测试
- `cnki_searcher.py` 已合并原 `cnki_xuetang_searcher.py` 功能