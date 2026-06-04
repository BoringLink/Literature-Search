---
name: literature-search
description: |
  Multi-source academic literature search tool integrating arXiv, Semantic Scholar, SerpApi (Google Scholar), Core API, and 知网API (CNKI). Optimized for thesis background research, literature reviews, and discovering papers by keyword, author, year range, or academic discipline (CS, ML, AI, NLP, education).
  
  Triggered by queries like:
  - "Find papers on [topic]" for thesis writing
  - "Search literature on [keywords]" for background research
  - "Find papers by [author name]" for author tracking
  - "Literature review on [subject]" with year constraints
  - "Papers in [category like AI/ML/education]" from specific years
  
  Returns structured results (title, authors, year, citations, abstract, links) in Markdown (thesis-friendly) or JSON (programmatic) format with local file persistence.
  
  Best for: thesis lit reviews, related work sections, author publication discovery, domain-specific paper collection, academic background research with output saved to workspace.
compatibility: "Python 3.8+, requests library, feedparser"
---

# Literature Search Skill

This skill enables comprehensive academic paper discovery across multiple sources, optimized for thesis writing and research.

## Overview

The skill integrates **seven** major academic search APIs:
- **arXiv**: Direct access to preprints across CS, physics, and other domains
- **Semantic Scholar**: Enriched metadata, citation graphs, and influence metrics
- **SerpApi (Google Scholar)**: Access to Google Scholar search results with rich metadata
- **Core API**: Access to millions of open access research papers from repositories worldwide
- **知网 API (CNKI)**: Access to Chinese academic literature database
- **百度千帆学术**: Access to Baidu's academic search engine
- **OpenAlex**: Access to the open catalog of the world's research papers
- **百度千帆学术 (Baidu Scholar)**: Chinese academic search with Bearer token authentication
- **OpenAlex**: Comprehensive open academic catalog with global coverage

Results are structured and saved locally for seamless thesis integration.

## Capabilities

### Multi-Source Search
- Query arXiv for preprints (especially strong in CS and physics)
- Query Semantic Scholar for published papers with citation metrics
- Query SerpApi for Google Scholar search results
- Query Core API for open access research papers
- Query 知网研学开放平台 for Chinese academic literature (JWT auth)
- Query 百度千帆学术 for Chinese academic search (API key)
- Query OpenAlex for comprehensive open academic catalog
- Combine results with deduplication

### Flexible Filtering
- **Keywords**: Multi-keyword boolean search
- **Authors**: Search by author name
- **Year Range**: Specify publication date constraints
- **Category/Domain**: Focus on CS (AI/ML/education) or other fields
- **Source**: arXiv, Semantic Scholar, SerpApi, Core API, 知网API, or any combination

### Output Formats
- **Markdown**: Human-readable, thesis-friendly format with links
- **JSON**: Structured data for programmatic use
- **Results Storage**: Auto-save to workspace directory with timestamp

### Agent-Friendly Design
- Clear parameter schema for easy delegation
- Comprehensive error handling and fallbacks
- Progress reporting and result summaries
- Designed for autonomous Agent execution

## Usage

### Basic Search
```
Search for papers on "transformer architecture" from 2020-2024
Sources: arXiv, Semantic Scholar, SerpApi, and Core API
Output format: Markdown
```

### Advanced Search
```
Search for papers by "Yoshua Bengio" on deep learning
Filter: 2018-2024
Category: Computer Science > AI/ML
Sources: Semantic Scholar (for citation metrics) and Core API
Output: JSON with citation counts
Save to: ./outputs/bengio_papers_2024.json
```

### For Thesis Writing
```
Literature review search: "federated learning" + "privacy"
Years: 2019-2024
Focus: arXiv (preprints) + Semantic Scholar (published) + Core API (OA papers)
Output: Markdown (easy to integrate into thesis)
Include: Title, authors, year, abstract, link
```

### For Chinese Literature Search
```
Search for papers on "深度学习" from 2020-2024
Sources: 知网研学开放平台，百度千帆学术
Output: Markdown with Chinese metadata
Include: Title, authors, year, abstract, DOI (if available)
```

### Comprehensive Search
```
Search for papers on "neural networks" from 2020-2024
Sources: arXiv, Semantic Scholar, SerpApi, Core API, CNKI Xuetang, Baidu Scholar, OpenAlex
Output: JSON with full metadata
Save to: ./outputs/comprehensive_neural_networks_2024.json
```

## Parameters

The skill accepts the following parameters (typically passed by Agent):

| Parameter | Type | Example | Notes |
|-----------|------|---------|-------|
| `keywords` | string or list | `"transformer"` or `["深度学习", "NLP"]` | Main search terms |
| `authors` | string or list | `"Yann LeCun"` or `"姚期智"` | Optional author filter |
| `year_min` | int | `2020` | Earliest publication year |
| `year_max` | int | `2024` | Latest publication year |
| `category` | string | `"cs.AI"` or `"education"` | arXiv category or domain |
| `sources` | list | `["arxiv", "semantic", "serpapi", "core", "cnki", "cnki_xuetang", "baidu_scholar", "openalex"]` | Which APIs to query |
| `output_format` | string | `"markdown"` or `"json"` | Result format |
| `max_results` | int | `50` | Number of results per source |
| `save_to_file` | bool | `true` | Save results locally |
| `output_dir` | string | `"./outputs"` | Directory for saved results |
| `serpapi_key` | string | `"your-serpapi-key"` | API key for SerpApi (Google Scholar) |
| `semantic_scholar_key` | string | `"your-semantic-scholar-key"` | API key for Semantic Scholar (optional) |
| `core_api_key` | string | `"your-core-api-key"` | API key for Core API |
| `cnki_username` | string | `"your-cnki-username"` | Username for 知网API authentication |
| `cnki_password` | string | `"your-cnki-password"` | Password for 知网API authentication |

## Implementation Details

### Scripts
- `combined_search.py`: Main entry point, orchestrates searches across all sources
- `arxiv_searcher.py`: arXiv API client with caching
- `semantic_searcher.py`: Semantic Scholar API integration
- `serpapi_searcher.py`: SerpApi (Google Scholar) API integration
- `core_searcher.py`: Core API integration for open access papers
- `cnki_searcher.py`: 知网 API (CNKI) integration for Chinese academic literature
- `cnki_xuetang_searcher.py`: 知网研学开放平台 integration with JWT authentication
- `baidu_scholar_searcher.py`: 百度千帆学术 integration with Bearer token auth
- `openalex_searcher.py`: OpenAlex API integration for comprehensive academic catalog
- `result_formatter.py`: Convert results to Markdown/JSON

### References
- `arxiv_categories.md`: Category taxonomy
- `query_examples.md`: Query construction guide
- `api_limits.md`: Rate limiting and quotas

## Output Example

### Markdown Format
```markdown
# Literature Search Results
**Query**: transformer architecture  
**Date**: 2024-04-21  
**Sources**: arXiv, Semantic Scholar  

## Results (15 papers found)

### 1. Attention Is All You Need
- **Authors**: Vaswani et al.
- **Year**: 2017
- **Source**: arXiv (1706.03762)
- **Abstract**: We propose a new simple network architecture based on an attention mechanism...
- **Link**: https://arxiv.org/abs/1706.03762

### 2. ...
```

### JSON Format
```json
{
  "query": "transformer architecture",
  "search_params": {
    "keywords": ["transformer"],
    "year_min": 2020,
    "year_max": 2024
  },
  "results": [
    {
      "title": "...",
      "authors": [...],
      "year": 2023,
      "arxiv_id": "2301.xxxxx",
      "abstract": "...",
      "citations": 45,
      "url": "..."
    }
  ],
  "total_found": 15,
  "search_duration_seconds": 4.2
}
```

## Best Practices

### For Thesis Literature Reviews
1. Search multiple related keywords separately (combine results later)
2. Use year constraints to focus on recent work
3. Save results as Markdown for easy integration into thesis
4. Cross-reference citations using Semantic Scholar data

### For Agent Execution
1. Provide clear keyword combinations
2. Specify year ranges to reduce noise
3. Use `max_results` to balance coverage vs. speed
4. Enable file saving for result persistence

### API Considerations
- arXiv: ~2 requests/second limit (handled by caching)
- Semantic Scholar: Free tier with reasonable rate limits
- Results cached locally to minimize API calls
- Fallback to Markdown if JSON parsing fails

## Error Handling

The skill handles:
- Network timeouts (with retries)
- Invalid API keys (graceful degradation)
- Empty result sets (alternative searches suggested)
- Malformed responses (logged and skipped)

For Semantic Scholar queries without API key, results are limited but available.

## Future Enhancements

- Google Scholar integration (if permitted)
- Cross-reference resolution (citation graph exploration)
- PDF metadata extraction
- Local database for caching large result sets
