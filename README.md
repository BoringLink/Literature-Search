<p align="center">
  <img src="literature_search_logo.png" width="120" alt="Literature Search Logo">
</p>

<h1 align="center" style="font-size: 2.5em; margin: 0.2em 0;">Literature Search Agent</h1>

<p align="center" style="font-size: 1.1em; color: #666; margin-bottom: 1.5em;">
Multi-source academic literature search tool for AI agents
</p>
<p align="center" style="font-size: 1.1em; color: #666; margin-bottom: 1.5em;">
Integrates **7 academic APIs**: arXiv, Semantic Scholar, SerpApi (Google Scholar), Core API, CNKI, Baidu Qianfan Academic, and OpenAlex.
</p>

<p align="center">
  <span style="display:inline-block; padding:3px 10px; font-size:12px; font-weight:600; border-radius:12px; background:#28a745; color:#fff;">arXiv · Free</span>
  <span style="display:inline-block; padding:3px 10px; font-size:12px; font-weight:600; border-radius:12px; background:#0366d6; color:#fff;">Semantic Scholar</span>
  <span style="display:inline-block; padding:3px 10px; font-size:12px; font-weight:600; border-radius:12px; background:#0366d6; color:#fff;">Google Scholar</span>
  <span style="display:inline-block; padding:3px 10px; font-size:12px; font-weight:600; border-radius:12px; background:#fd7e14; color:#fff;">CNKI 知网</span>
  <span style="display:inline-block; padding:3px 10px; font-size:12px; font-weight:600; border-radius:12px; background:#0366d6; color:#fff;">Baidu Scholar</span>
  <span style="display:inline-block; padding:3px 10px; font-size:12px; font-weight:600; border-radius:12px; background:#0366d6; color:#fff;">OpenAlex</span>
  <span style="display:inline-block; padding:3px 10px; font-size:12px; font-weight:600; border-radius:12px; background:#0366d6; color:#fff;">Core</span>
</p>

<p align="center">
<a href="./README.md">English</a> | <a href="./README.zh.md">中文</a>
</p>
---

## 🚀 QuickStart

> 💡 **Hint**: If you're using an AI agent (such as Claude Code, Cursor, OpenCode, etc.), you can simply tell the agent:
>
> **Install Literature-Search Skill according to the following spec: https://github.com/BoringLink/Literature-Search/SPEC.md**
>

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
