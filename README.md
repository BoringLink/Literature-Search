# Literature Search Skill

**Multi-Source Academic Literature Search Tool** - Provides comprehensive literature discovery capabilities for thesis writing and research reports.

Integrates **7 Academic APIs**: arXiv, Semantic Scholar, SerpApi (Google Scholar), Core API, CNKI (China National Knowledge Infrastructure), Baidu Scholar, and OpenAlex.

---

## 🚀 Quick Start

### Note for AI Agent Users

> 💡 **Tip**: If you are using an AI Agent (such as Claude, Cursor, etc.), you can directly tell the Agent:
>
> **"Please read the SPEC.md file and follow the installation and usage instructions therein."**
>
> SPEC.md is a complete technical document written specifically for Agents, containing detailed installation steps, API configuration, usage examples, and best practices. The Agent will automatically execute all configuration and search tasks without requiring manual operation from you.

---

### Manual Installation

#### 1. Install Dependencies

```bash
pip install requests feedparser
```

#### 2. Configure API Keys (Optional, Recommended)

```bash
# Semantic Scholar (improved rate limits)
export SEMANTIC_SCHOLAR_KEY="your-key-here"

# SerpApi (Google Scholar proxy)
export SERPAPI_KEY="your-key-here"

# Core API (open access papers)
export CORE_API_KEY="your-key-here"

# CNKI (Chinese literature)
export CNKI_USERNAME="your-username"
export CNKI_PASSWORD="your-password"

# Baidu Scholar (Chinese academic search)
export BAIDU_API_KEY="your-key-here"

# OpenAlex (open academic catalog)
export OPENALEX_API_KEY="your-key-here"
```

**Note**: arXiv does not require an API key.

#### 3. Test Installation

```bash
python scripts/combined_search.py --help
```

---

## 📖 Basic Usage

### Method 1: Python API (Recommended)

```python
from scripts.combined_search import LiteratureSearcher

# Initialize
searcher = LiteratureSearcher(output_dir="./outputs")

# Search papers
results = searcher.search(
    keywords="deep learning",
    year_min=2020,
    year_max=2024,
    category="cs.AI",
    max_results=50,
    output_format="markdown",
    save_to_file=True
)

print(f"Found {len(results['results'])} papers")
print(f"Results saved to: {results['output_file']}")
```

### Method 2: Command Line

```bash
# Basic search
python scripts/combined_search.py "deep learning" \
    --year-min 2020 \
    --year-max 2024 \
    --category cs.AI \
    --format markdown

# Multi-keyword search
python scripts/combined_search.py "federated learning" "privacy" \
    --authors "Yann LeCun" \
    --format json

# Specify API source
python scripts/combined_search.py "transformer" \
    --sources semantic \
    --max-results 100
```

---

## 🎯 Common Use Cases

### Use Case 1: Thesis Literature Review

```python
results = searcher.search(
    keywords=["neural networks", "deep learning"],
    category="cs.AI",
    year_min=2020,
    output_format="markdown",
    save_to_file=True
)
```

**Output**: `outputs/papers_neural_networks_*.md` - Can be directly used for the background/related work sections of a thesis.

### Use Case 2: Find Papers by a Specific Author

```python
results = searcher.search(
    keywords=["machine learning"],
    authors="Geoffrey Hinton",
    year_min=2010,
    sources=["semantic"],  # Semantic Scholar is better for author discovery
    output_format="json",
    max_results=100
)
```

### Use Case 3: Chinese Literature Search

```python
results = searcher.search(
    keywords="联邦学习",
    sources=["cnki", "baidu"],  # Use Chinese APIs
    year_min=2020,
    output_format="markdown"
)
```

### Use Case 4: Systematic Multi-Keyword Review

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
# Results are automatically deduplicated (based on title + year + authors)
```

---

## 📊 Output Formats

| Format | Purpose | Use Case |
|--------|---------|----------|
| **Markdown** | Human-readable, thesis-friendly | Direct use in thesis writing |
| **JSON** | Structured data | Programmatic processing, citation analysis |
| **CSV** | Spreadsheet-compatible | Excel/Google Sheets import |
| **BibTeX** | Reference managers | Zotero, Mendeley import |

---

## 🔧 Search Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keywords` | str or List[str] | ✅ Yes | - | Search keywords (multiple = AND logic) |
| `year_min` | int | ❌ No | None | Minimum publication year |
| `year_max` | int | ❌ No | None | Maximum publication year |
| `category` | str | ❌ No | None | arXiv category (e.g., `cs.AI`, `cs.LG`) |
| `authors` | str | ❌ No | None | Filter by author name |
| `max_results` | int | ❌ No | 50 | Maximum number of papers to return |
| `sources` | List[str] | ❌ No | None | APIs to query: `["arxiv", "semantic", "cnki", ...]` |
| `output_format` | str | ❌ No | `"markdown"` | Output format: `markdown`/`json`/`csv`/`bibtex` |
| `save_to_file` | bool | ❌ No | True | Automatically save results to file |

---

## 📚 API Rate Limits

| API | Rate Limit | API Key | Delay |
|-----|------------|---------|-------|
| arXiv | ~2 requests/second | Not required | 3 seconds |
| Semantic Scholar | 100 requests/5 minutes (free) | Optional | 1 second |
| SerpApi | 100 searches/month (free) | Required | Built-in |
| Core API | 500 requests/day | Required | Built-in |
| CNKI | JWT expires in 24 hours | Username + Password | Built-in |
| Baidu Scholar | QPS limit (application required) | Required | Built-in |
| OpenAlex | Rate limited (free) | Optional | Built-in |

**Strategy**: Use multiple API sources simultaneously for comprehensive coverage. Built-in caching mechanism reduces repeated queries.

---

## 🗂️ File Structure

```
literature-search/
├── SPEC.md                          # Technical documentation for Agents ⭐
├── README.md                        # This file (user guide)
├── SKILL.md                         # Skill metadata
├── scripts/                         # Core search modules
│   ├── combined_search.py           # Main orchestrator
│   ├── arxiv_searcher.py            # arXiv client
│   ├── semantic_searcher.py         # Semantic Scholar client
│   ├── serpapi_searcher.py          # Google Scholar proxy
│   ├── cnki_searcher.py             # CNKI client
│   ├── baidu_scholar_searcher.py    # Baidu Scholar client
│   ├── core_searcher.py             # Core API client
│   ├── openalex_searcher.py         # OpenAlex client
│   └── result_formatter.py          # Output formatter
├── references/                      # Reference documentation
│   ├── arxiv_categories.md          # arXiv category reference
│   ├── query_examples.md            # Query examples
│   └── api_limits.md                # API limit details
└── outputs/                         # Automatically saved search results
```

---

## 💡 Best Practices

### Improve Search Efficiency
1. **Use specific keywords** - Avoid overly broad terms like "machine learning"
2. **Narrow year range** - e.g., `year_min=2020` to search only the last 5 years
3. **Use category filtering** - e.g., `cs.AI` to search only artificial intelligence field
4. **Set reasonable max_results** - e.g., 50 papers is sufficient for preliminary research

### Reduce API Calls
1. **Leverage built-in caching** - Avoid repeated searches on the same topic
2. **Batch searches** - Execute multiple related queries at once
3. **Reuse historical results** - Check the `outputs/` directory to avoid duplicate searches

### Result Management
1. **Enable file saving** - Automatically save to the `outputs/` directory
2. **Use Markdown format** - Directly usable for thesis writing
3. **Clean cache regularly** - Avoid occupying too much disk space

---

## ❓ Frequently Asked Questions

### "No results found"
- Try broader keywords
- Check spelling
- Remove year restrictions
- Try different API sources

### "API timeout"
- Automatic retry mechanism is implemented
- Wait a few seconds and retry
- Consider configuring an API key for Semantic Scholar

### "Missing citation data"
- Some papers may not have citation counts
- Use Semantic Scholar source for complete metrics
- Check if the paper is indexed by Semantic Scholar

---

## 🔗 Reference Documentation

- **SPEC.md** - Complete technical documentation for Agents (recommended for AI Agents)
- **references/arxiv_categories.md** - arXiv classification system
- **references/query_examples.md** - Advanced query pattern examples
- **references/api_limits.md** - API limits and configuration details

---

## 🔗 External Links

- [arXiv API Documentation](https://arxiv.org/help/api/)
- [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- [feedparser Documentation](https://pythonhosted.org/feedparser/)

---

## 📄 License

- Uses open APIs: arXiv, Semantic Scholar, SerpApi, Core, CNKI, Baidu, OpenAlex
- Complies with all API terms of service and rate limits
- Suitable for academic research purposes