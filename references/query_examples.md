# Query Examples and Best Practices

## For Thesis Literature Reviews

### Example 1: Finding Recent Deep Learning Papers

**Use Case**: Writing thesis on deep learning applications in computer vision

```python
search(
    keywords=["deep learning", "convolutional neural networks"],
    category="cs.CV",
    year_min=2020,
    year_max=2024,
    sources=["arxiv", "semantic"],
    max_results=100,
    output_format="markdown",
    save_to_file=True,
)
```

**Why this works**:
- Specific keywords narrow results to relevant papers
- Year range ensures recent work
- cs.CV category filters to computer vision domain
- Both sources provide complementary data (preprints + published + citations)
- Markdown output ready for thesis integration

### Example 2: Finding Papers by Specific Authors

**Use Case**: Researching work from known pioneers in your field

```python
search(
    keywords=["reinforcement learning"],
    authors="Richard Sutton",
    sources=["semantic"],  # Semantic Scholar better for author discovery
    max_results=50,
    output_format="json",
)
```

### Example 3: Multi-Keyword Literature Review

**Use Case**: Comprehensive review combining multiple concepts

```python
search(
    keywords=["federated learning", "privacy", "decentralized"],
    category="cs.LG",
    year_min=2019,
    year_max=2024,
    sources=["arxiv"],  # More preprints in this active area
    max_results=150,
)
```

Then run additional searches:

```python
search(
    keywords=["federated learning", "communication efficiency"],
    category="cs.LG",
    year_min=2019,
    year_max=2024,
    sources=["semantic"],  # Get citation metrics for second pass
    max_results=100,
)
```

Combine results manually, removing duplicates.

## API Rate Limits and Considerations

### arXiv
- **Rate Limit**: ~2 requests per second
- **Delay**: Automatically enforced (3 seconds between requests)
- **Best For**: Preprints, recent work, large result sets
- **Note**: No API key required

### Semantic Scholar
- **Rate Limit**: 100 requests per 5 minutes (free tier)
- **API Key**: Optional (improves rate limits)
- **Delay**: Automatically enforced (1 second between requests)
- **Best For**: Published papers, citation metrics, rich metadata

### Strategy
1. **First Pass**: Use arXiv for keyword discovery (broader coverage)
2. **Second Pass**: Use Semantic Scholar for citation metrics
3. **Combine**: Merge results, dedup by title

## Query Construction Tips

### Effective Keywords
✅ **Good**: "transformer architecture", "attention mechanism", "BERT"
❌ **Avoid**: "AI", "deep learning" alone (too broad)

### Boolean Operators
- **AND**: Narrow results (both terms must appear)
  - Example: `["neural networks", "graph"]` → papers on graph neural networks
- **OR**: Broaden results (at least one term)
  - Example: `["CNN", "RNN"]` → convolutional OR recurrent networks

### Year Ranges
- **Last 2 years** (2022-2024): Latest methods and improvements
- **Last 5 years** (2019-2024): Established trends with maturity
- **Since 2015**: Major paradigm shifts (if looking for historical context)

### Category Selection
- **Single category** (cs.AI): Focused results
- **Multiple categories** (cs.AI + cs.LG): Broader coverage
- **None**: Searches across all arXiv (not recommended for active areas)

## Handling Large Result Sets

If a search returns 500+ papers:

1. **Narrow keywords**: Use more specific terms or combinations
2. **Tighten year range**: Focus on most recent work
3. **Use category filters**: Reduce noise
4. **Post-process results**: Filter by citation count, author reputation

## Saving and Organizing Results

### File Naming Convention
```
papers_KEYWORDS_YYYYMMDD_HHMMSS.md  # Auto-generated
papers_federated_learning_20240421_143022.md
```

### Directory Organization
```
./outputs/
├── literature_review/
│   ├── transformer_papers_2024.md
│   ├── attention_mechanisms_2024.md
│   └── nlp_survey_2024.md
└── specific_author/
    └── lecun_papers_all.json
```

## Troubleshooting

### "No results found"
- Check keyword spelling
- Try broader keywords or remove year constraints
- Verify category exists (see arxiv_categories.md)
- Try Semantic Scholar instead (better for some domains)

### "Too many results (>1000)"
- Add more specific keywords
- Narrow the year range
- Use author filters
- Split into multiple searches

### "API timeout"
- Increase delay between requests
- Reduce max_results per search
- Run searches sequentially instead of parallel

## Semantic Scholar Citation Metrics

When using Semantic Scholar, you get citation counts:
- **High citations** (>100): Well-cited influential papers
- **Medium citations** (10-100): Solid contributions
- **Low citations** (<10): Recent or niche papers

Use this to prioritize reading for thesis background.

## Example Workflow for Thesis

1. **Identify key concepts** from your thesis topic
2. **Run initial broad search** for each concept (arXiv)
3. **Save Markdown results** for easy reference
4. **Run targeted searches** by important authors
5. **Export to JSON** and import into reference manager (Zotero, Mendeley, etc.)
6. **Review citations** in Semantic Scholar results to find "hidden" influential papers
7. **Save final curated list** as structured JSON for analysis

## Chinese Literature Search Examples

### Example 4: 中文深度学习文献搜索

**Use Case**: 撰写中文论文的深度学习章节

```python
search(
    keywords=["深度学习", "卷积神经网络"],
    year_min=2020,
    year_max=2024,
    sources=["cnki", "baidu_scholar"],  # 知网 + 百度千帆
    max_results=50,
    output_format="markdown",
    save_to_file=True,
)
```

**Why this works**:
- 知网提供中文核心期刊和学位论文
- 百度千帆补充中文学术搜索
- 中文关键词返回中文元数据
- Markdown 格式便于直接引用

### Example 5: 中英文文献综合搜索

**Use Case**: 全面综述需要中英文文献

```python
# 第一轮：英文文献
search(
    keywords=["federated learning"],
    year_min=2020,
    sources=["arxiv", "semantic", "openalex"],
    output_format="markdown",
    save_to_file=True,
)

# 第二轮：中文文献
search(
    keywords=["联邦学习"],
    year_min=2020,
    sources=["cnki", "baidu_scholar"],
    output_format="markdown",
    save_to_file=True,
)
```

## OpenAlex Examples

### Example 6: 全球开放学术目录搜索

**Use Case**: 查找跨学科的全球研究成果

```python
search(
    keywords=["machine learning", "healthcare"],
    year_min=2020,
    sources=["openalex"],  # OpenAlex 覆盖全球学术目录
    max_results=100,
    output_format="json",  # JSON 便于数据分析
    save_to_file=True,
)
```

**Why OpenAlex**:
- 覆盖 Crossref、PubMed、arXiv 等多个来源
- 提供开放获取状态标识
- 包含作者机构信息
- 适合跨学科研究

### Example 7: 综合所有 API 的搜索

**Use Case**: 最全面的文献检索

```python
search(
    keywords=["neural networks"],
    year_min=2020,
    sources=[
        "arxiv",           # 预印本
        "semantic",        # 已发表论文 + 引用
        "serpapi",         # Google Scholar
        "core",            # 开放获取论文
        "cnki",            # 中文文献
        "baidu_scholar",   # 中文学术搜索
        "openalex"         # 全球学术目录
    ],
    max_results=50,
    output_format="json",
    save_to_file=True,
)
```

**Note**: 此搜索会返回最全面的结果，但耗时较长（约 30-60 秒）。建议仅在需要 exhaustive search 时使用。
