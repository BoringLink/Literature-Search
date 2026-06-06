# Literature Search Agent

Multi-source academic literature search tool for AI agents. Integrates arXiv, Semantic Scholar, Google Scholar, CNKI, and more.

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

## Usage

```bash
# Basic search
python -m literature_search "deep learning" --year-min 2020

# Multi-keyword search
python -m literature_search "federated learning" "privacy" --authors "Yann LeCun"

# Specify sources
python -m literature_search "transformer" --sources semantic --max-results 100

# Output format
python -m literature_search "neural networks" --format json
```

## API Sources

- arXiv (free, no key required)
- Semantic Scholar (requires API key)
- Google Scholar via SerpApi (requires API key)
- CNKI 知网 (requires username/password)
- Baidu Scholar (requires API key)
- OpenAlex (requires API key)
- Core (requires API key)

## Configuration

Create a `.env` file or set environment variables:

```bash
SEMANTIC_SCHOLAR_KEY=xxx
SERPAPI_KEY=xxx
CORE_API_KEY=xxx
CNKI_USERNAME=xxx
CNKI_PASSWORD=xxx
BAIDU_API_KEY=xxx
OPENALEX_API_KEY=xxx
```

## Output

Results are saved to `outputs/` directory in Markdown, JSON, CSV, or BibTeX format.

## License

MIT
