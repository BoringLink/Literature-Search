# Literature Search Skill - Agent Specification

**For AI Agents**: This document provides complete installation and usage instructions for the Literature Search Skill.

---

## Quick Summary

**What this skill does**: Multi-source academic paper search across arXiv, Semantic Scholar, SerpApi (Google Scholar), Core API, 知网 (CNKI), 百度千帆学术，and OpenAlex.

**Best for**: Thesis literature reviews, author publication tracking, systematic reviews, academic background research.

**Output**: Markdown (thesis-ready), JSON (structured), CSV (spreadsheet), or BibTeX (reference managers).

---

## Installation

### Option 1: npx skills add (Recommended)

```bash
npx skills add BoringLink/Literature-Search
```

### Option 2: Manual Copy

Copy the `python/literature_search/` directory to your IDE's skills folder:

- **Claude Code**: `~/.claude/skills/literature-search/`
- **Cursor**: `~/.cursor/skills/literature-search/` or `.agents/skills/literature-search/`
- **OpenCode**: `.agents/skills/literature-search/`

### Option 3: pip install (Development)

```bash
pip install -e .
```

### Step 1: Install Dependencies

```bash
pip install requests feedparser
```

### Step 2: Configure API Keys (Optional but Recommended)

```bash
# Semantic Scholar (improves rate limits)
export SEMANTIC_SCHOLAR_KEY="your-key-here"

# SerpApi (Google Scholar proxy)
export SERPAPI_KEY="your-key-here"

# Core API (open access papers)
export CORE_API_KEY="your-key-here"

# 知网研学 (Chinese literature)
export CNKI_USERNAME="your-username"
export CNKI_PASSWORD="your-password"

# 百度千帆学术 (Chinese academic search)
export BAIDU_API_KEY="your-key-here"

# OpenAlex (open academic catalog)
export OPENALEX_API_KEY="your-key-here"
```

**Note**: arXiv requires no API key.

### Step 2: Verify Installation

```bash
cd literature-search
python -m literature_search --help
```

Expected output: Command-line argument help.

---

## Usage for Agents

### Method 1: Python API (Recommended for Agents)

```python
from python.literature_search import LiteratureSearcher

# Initialize
searcher = LiteratureSearcher(
    output_dir="./outputs",      # Where to save results
    semantic_api_key=None,       # or pass key directly
)
```

### Method 2: Command Line

```bash
# Basic search
python -m literature_search "deep learning" \
    --year-min 2020 \
    --year-max 2024 \
    --category cs.AI \
    --format markdown \
    --output-dir ./outputs

# Multi-keyword search
python -m literature_search "federated learning" "privacy" \
    --authors "Yann LeCun" \
    --format json \
    --max-results 100

# Specific source only
python -m literature_search "transformer" \
    --sources semantic \
    --semantic-key "your-key" \
    --format markdown
```

---

## Search Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keywords` | str or List[str] | ✅ Yes | - | Search terms (AND logic for multiple) |
| `year_min` | int | ❌ No | None | Minimum publication year |
| `year_max` | int | ❌ No | None | Maximum publication year |
| `category` | str | ❌ No | None | arXiv category (e.g., `cs.AI`, `cs.LG`) |
| `authors` | str | ❌ No | None | Author name filter |
| `max_results` | int | ❌ No | 50 | Maximum papers to return |
| `sources` | List[str] | ❌ No | None | APIs to query: `["arxiv", "semantic", "serpapi", "core", "cnki", "baidu", "openalex"]` |
| `output_format` | str | ❌ No | `"markdown"` | Output format: `markdown`/`json`/`csv`/`bibtex` |
| `save_to_file` | bool | ❌ No | True | Auto-save results to file |
| `output_dir` | str | ❌ No | `"./outputs"` | Directory to save results |

---

## Output Formats

### Markdown (Recommended for Thesis)
Human-readable format with:
- Paper title, authors, year
- Abstract
- Citation count (if available)
- Direct links to paper/PDF
- Source API label

**Use case**: Direct integration into thesis background/related work sections.

### JSON (Recommended for Programmatic Use)
Structured data with full metadata:
```json
{
  "title": "Attention Is All You Need",
  "authors": ["Vaswani A", "Shazeer N", ...],
  "year": 2017,
  "abstract": "...",
  "citations": 58000,
  "arxiv_id": "1706.03762",
  "doi": "...",
  "source": "semantic",
  "url": "https://arxiv.org/abs/1706.03762"
}
```

**Use case**: Citation analysis, data processing, building bibliographies.

### CSV (Recommended for Spreadsheets)
Excel/Google Sheets compatible.

**Use case**: Literature review spreadsheets, sorting/filtering.

### BibTeX (Recommended for Reference Managers)
Compatible with Zotero, Mendeley, JabRef.

**Use case**: Import into reference management software.

---

## Common Search Patterns

### Pattern 1: Thesis Literature Review
```python
results = searcher.search(
    keywords=["neural networks", "deep learning"],
    category="cs.AI",
    year_min=2020,
    output_format="markdown",
    save_to_file=True
)
# Output: papers_neural_networks_deep_learning_*.md
```

### Pattern 2: Author Publication History
```python
results = searcher.search(
    keywords=["machine learning"],  # Optional
    authors="Geoffrey Hinton",
    year_min=2010,
    sources=["semantic"],  # Better for author discovery
    output_format="json",
    max_results=100
)
```

### Pattern 3: Systematic Multi-Keyword Review
```python
queries = [
    ["reinforcement learning", "policy gradient"],
    ["reinforcement learning", "Q-learning"],
    ["reinforcement learning", "actor-critic"],
]

all_results = []
for kw in queries:
    results = searcher.search(
        keywords=kw,
        category="cs.LG",
        year_min=2015,
        output_format="json"
    )
    all_results.extend(results["results"])
# Results automatically deduplicated by title+year+authors
```

### Pattern 4: Chinese Literature Search
```python
results = searcher.search(
    keywords="联邦学习",  # Chinese keywords
    sources=["cnki", "baidu"],  # Chinese APIs only
    year_min=2020,
    output_format="markdown"
)
```

---

## API Rate Limits

| API | Rate Limit | API Key | Delay Enforced |
|-----|------------|---------|----------------|
| arXiv | ~2 req/s | Not required | 3 seconds |
| Semantic Scholar | 100 req/5min (free) | Optional | 1 second |
| SerpApi | 100 searches/month (free) | Required | Built-in |
| Core API | 500 req/day | Required | Built-in |
| 知网 (CNKI) | JWT expires 24h | Username+Password | Built-in |
| 百度千帆 | QPS limit (apply for quota) | Required | Built-in |
| OpenAlex | Rate limited (free) | Optional | Built-in |

**Strategy**: Use all sources for comprehensive coverage. Built-in caching minimizes redundant queries.

---

## Error Handling

### Common Issues

**"No results found"**
- Try broader keywords
- Check spelling
- Remove year constraints
- Try different sources

**"Rate limit exceeded"**
- Automatic backoff implemented
- Wait before retrying
- Consider API key for Semantic Scholar

**"Missing citations data"**
- Some papers lack citation counts
- Use Semantic Scholar source for full metrics

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## File Structure

```
literature-search/
├── SPEC.md                          # This file (Agent instructions)
├── README.md                        # User guide (human-readable)
├── SKILL.md                         # Skill metadata
├── python/literature_search/        # Core Python package
│   ├── __init__.py                  # Package entry, exports LiteratureSearcher
│   ├── __main__.py                  # Enables python -m literature_search
│   ├── combined_search.py           # Main orchestrator
│   ├── arxiv_searcher.py            # arXiv client
│   ├── semantic_searcher.py         # Semantic Scholar client
│   ├── serpapi_searcher.py          # Google Scholar via SerpApi
│   ├── cnki_searcher.py             # 知网研学 client
│   ├── baidu_scholar_searcher.py    # 百度千帆学术 client
│   ├── core_searcher.py             # Core API client
│   ├── openalex_searcher.py         # OpenAlex client
│   └── result_formatter.py          # Output formatter
├── references/
│   ├── arxiv_categories.md          # Category reference
│   ├── query_examples.md            # Query patterns
│   └── api_limits.md                # Rate limits detail
├── package.json                     # npm publish config
├── .claude-skill.json               # Claude Code Skill metadata
├── install-skill.js                 # Install script
├── uninstall-skill.js               # Uninstall script
└── outputs/                         # Auto-saved results
```

---

## Testing

### Run Evaluation Tests
```bash
bash run_evals.sh  # If available
```

### Manual Test
```python
from python.literature_search import LiteratureSearcher

searcher = LiteratureSearcher()
results = searcher.search(
    keywords="deep learning",
    year_min=2023,
    max_results=5,
    output_format="markdown"
)
print(f"Found {len(results['results'])} papers")
```

---

## Integration with Reference Managers

### Zotero
1. Search with `output_format="bibtex"`
2. Copy BibTeX output
3. Paste into Zotero as new collection

### Mendeley
1. Export as CSV
2. Import CSV into Mendeley
3. Mendeley auto-fetches metadata

---

## Performance Tips

### Speed Up Searches
- Use specific keywords (avoid broad terms like "machine learning")
- Limit year range
- Use category filters
- Set lower `max_results`

### Reduce API Calls
- Leverage built-in caching
- Batch multiple searches
- Reuse previous results

### Memory Usage
- Process in batches for >500 papers
- Enable file saving (auto-saves to disk)
- Clear cache periodically

---

## Best Practices for Agents

1. **Always specify year range** - Prevents overwhelming results
2. **Use category filters** - Improves relevance (e.g., `cs.AI` for AI papers)
3. **Start with arXiv** - Fast, no API key, recent preprints
4. **Add Semantic Scholar for citations** - Better metadata, citation counts
5. **Save results to file** - Avoid re-searching same topic
6. **Handle empty results gracefully** - Suggest broader keywords
7. **Respect rate limits** - Built-in delays are automatic
8. **Use Markdown for thesis work** - Ready for direct integration

---

## Support & Documentation

- **User Guide**: `README.md` (detailed usage examples)
- **API Reference**: `references/api_limits.md`
- **Query Examples**: `references/query_examples.md`
- **Categories**: `references/arxiv_categories.md`

---

## License

- Uses open APIs: arXiv, Semantic Scholar, SerpApi, Core, CNKI, Baidu, OpenAlex
- Respects all API ToS and rate limits
- Suitable for academic research purposes