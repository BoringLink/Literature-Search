#!/usr/bin/env python3
"""
Combined literature search across arXiv and Semantic Scholar.
Main entry point for the literature-search skill.
"""

import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
import argparse
from pathlib import Path


class LiteratureSearcher:
    """Orchestrates searches across multiple academic sources."""

    def __init__(
        self, 
        output_dir: str = "./outputs", 
        semantic_api_key: Optional[str] = None,
        serpapi_key: Optional[str] = None,
        core_api_key: Optional[str] = None,
        cnki_username: Optional[str] = None,
        cnki_password: Optional[str] = None,
        baidu_api_key: Optional[str] = None,
        openalex_api_key: Optional[str] = None,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.semantic_api_key = semantic_api_key
        self.serpapi_key = serpapi_key
        self.core_api_key = core_api_key
        self.cnki_username = cnki_username
        self.cnki_password = cnki_password
        self.baidu_api_key = baidu_api_key
        self.openalex_api_key = openalex_api_key

        # Import API handlers
        try:
            from .arxiv_searcher import ArxivSearcher

            self.arxiv = ArxivSearcher()
        except ImportError:
            print("Warning: arxiv_searcher module not available")
            self.arxiv = None

        try:
            from .semantic_searcher import SemanticSearcher

            self.semantic = SemanticSearcher(api_key=semantic_api_key)
        except ImportError:
            print("Warning: semantic_searcher module not available")
            self.semantic = None
            
        try:
            from .serpapi_searcher import SerpApiSearcher

            self.serpapi = SerpApiSearcher(api_key=serpapi_key)
        except ImportError:
            print("Warning: serpapi_searcher module not available")
            self.serpapi = None
            
        try:
            from .core_searcher import CoreSearcher

            self.core = CoreSearcher(api_key=core_api_key)
        except ImportError:
            print("Warning: core_searcher module not available")
            self.core = None
            
        try:
            from .cnki_searcher import CNKISearcher

            self.cnki = CNKISearcher(username=cnki_username, password=cnki_password)
        except ImportError:
            print("Warning: cnki_searcher module not available")
            self.cnki = None
        
        try:
            from .cnki_xuetang_searcher import CNKIXuetangSearcher

            self.cnki_xuetang = CNKIXuetangSearcher(username=cnki_username, password=cnki_password)
        except ImportError:
            print("Warning: cnki_xuetang_searcher module not available")
            self.cnki_xuetang = None
            
        try:
            from .baidu_scholar_searcher import BaiduScholarSearcher

            self.baidu_scholar = BaiduScholarSearcher(api_key=baidu_api_key)
        except ImportError:
            print("Warning: baidu_scholar_searcher module not available")
            self.baidu_scholar = None
            
        try:
            from .openalex_searcher import OpenAlexSearcher

            self.openalex = OpenAlexSearcher(api_key=openalex_api_key)
        except ImportError:
            print("Warning: openalex_searcher module not available")
            self.openalex = None

    def search(
        self,
        keywords: Optional[str | List[str]] = None,
        authors: Optional[str | List[str]] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        category: Optional[str] = None,
        sources: Optional[List[str]] = None,
        output_format: str = "markdown",
        max_results: int = 50,
        save_to_file: bool = True,
    ) -> Dict[str, Any]:
        """
        Execute combined search across sources.

        Args:
            keywords: Search keywords (string or list)
            authors: Author names to search
            year_min: Earliest publication year
            year_max: Latest publication year
            category: arXiv category (e.g., 'cs.AI') or domain
            sources: List of sources to query ('arxiv', 'semantic', 'serpapi', 'core', 'cnki', 'cnki_xuetang', 'baidu_scholar', 'openalex', or any combination)
            output_format: 'markdown' or 'json'
            max_results: Maximum results per source
            save_to_file: Whether to save results to local file

        Returns:
            Dictionary with search results and metadata
        """

        if sources is None:
            sources = ["arxiv", "semantic"]

        # Normalize keywords
        if isinstance(keywords, str):
            keywords = [keywords]

        results = {
            "query": keywords,
            "search_params": {
                "keywords": keywords,
                "authors": authors,
                "year_min": year_min,
                "year_max": year_max,
                "category": category,
                "sources": sources,
            },
            "results": [],
            "by_source": {},
            "search_timestamp": datetime.now().isoformat(),
            "total_found": 0,
        }

        # Search arXiv
        if "arxiv" in sources and self.arxiv:
            print(f"Searching arXiv for: {keywords}")
            arxiv_results = self.arxiv.search(
                keywords=keywords,
                authors=authors,
                year_min=year_min,
                year_max=year_max,
                category=category,
                max_results=max_results,
            )
            results["by_source"]["arxiv"] = arxiv_results
            results["results"].extend(arxiv_results)
            print(f"  Found {len(arxiv_results)} papers on arXiv")

        # Search Semantic Scholar
        if "semantic" in sources and self.semantic:
            print(f"Searching Semantic Scholar for: {keywords}")
            semantic_results = self.semantic.search(
                keywords=keywords,
                authors=authors,
                year_min=year_min,
                year_max=year_max,
                max_results=max_results,
            )
            results["by_source"]["semantic"] = semantic_results

            # Merge with deduplication (simple title-based)
            existing_titles = {r.get("title", "").lower() for r in results["results"]}
            for paper in semantic_results:
                if paper.get("title", "").lower() not in existing_titles:
                    results["results"].append(paper)

            print(f"  Found {len(semantic_results)} papers on Semantic Scholar")

        # Search SerpApi (Google Scholar)
        if "serpapi" in sources and self.serpapi:
            print(f"Searching SerpApi (Google Scholar) for: {keywords}")
            serpapi_results = self.serpapi.search(
                keywords=keywords,
                authors=authors,
                year_min=year_min,
                year_max=year_max,
                max_results=max_results,
            )
            results["by_source"]["serpapi"] = serpapi_results

            # Merge with deduplication (simple title-based)
            existing_titles = {r.get("title", "").lower() for r in results["results"]}
            for paper in serpapi_results:
                if paper.get("title", "").lower() not in existing_titles:
                    results["results"].append(paper)

            print(f"  Found {len(serpapi_results)} papers on SerpApi")

        # Search Core API
        if "core" in sources and self.core:
            print(f"Searching Core API for: {keywords}")
            core_results = self.core.search(
                keywords=keywords,
                authors=authors,
                year_min=year_min,
                year_max=year_max,
                max_results=max_results,
            )
            results["by_source"]["core"] = core_results

            # Merge with deduplication (simple title-based)
            existing_titles = {r.get("title", "").lower() for r in results["results"]}
            for paper in core_results:
                if paper.get("title", "").lower() not in existing_titles:
                    results["results"].append(paper)

            print(f"  Found {len(core_results)} papers on Core API")

        # Search CNKI
        if "cnki" in sources and self.cnki:
            print(f"Searching CNKI for: {keywords}")
            cnki_results = self.cnki.search(
                keywords=keywords,
                authors=authors,
                year_min=year_min,
                year_max=year_max,
                max_results=max_results,
            )
            results["by_source"]["cnki"] = cnki_results

            # Merge with deduplication (simple title-based)
            existing_titles = {r.get("title", "").lower() for r in results["results"]}
            for paper in cnki_results:
                if paper.get("title", "").lower() not in existing_titles:
                    results["results"].append(paper)

            print(f"  Found {len(cnki_results)} papers on CNKI")

        if "cnki_xuetang" in sources and self.cnki_xuetang:
            print(f"Searching CNKI Xuetang for: {keywords}")
            cnki_xuetang_results = self.cnki_xuetang.search(
                keywords=keywords,
                authors=authors,
                year_min=year_min,
                year_max=year_max,
                max_results=max_results,
            )
            results["by_source"]["cnki_xuetang"] = cnki_xuetang_results

            existing_titles = {r.get("title", "").lower() for r in results["results"]}
            for paper in cnki_xuetang_results:
                if paper.get("title", "").lower() not in existing_titles:
                    results["results"].append(paper)

            print(f"  Found {len(cnki_xuetang_results)} papers on CNKI Xuetang")

        if "baidu_scholar" in sources and self.baidu_scholar:
            print(f"Searching Baidu Scholar for: {keywords}")
            baidu_results = self.baidu_scholar.search(
                keywords=keywords,
                authors=authors,
                year_min=year_min,
                year_max=year_max,
                max_results=max_results,
            )
            results["by_source"]["baidu_scholar"] = baidu_results

            existing_titles = {r.get("title", "").lower() for r in results["results"]}
            for paper in baidu_results:
                if paper.get("title", "").lower() not in existing_titles:
                    results["results"].append(paper)

            print(f"  Found {len(baidu_results)} papers on Baidu Scholar")

        if "openalex" in sources and self.openalex:
            print(f"Searching OpenAlex for: {keywords}")
            openalex_results = self.openalex.search(
                keywords=keywords,
                authors=authors,
                year_min=year_min,
                year_max=year_max,
                max_results=max_results,
            )
            results["by_source"]["openalex"] = openalex_results

            existing_titles = {r.get("title", "").lower() for r in results["results"]}
            for paper in openalex_results:
                if paper.get("title", "").lower() not in existing_titles:
                    results["results"].append(paper)

            print(f"  Found {len(openalex_results)} papers on OpenAlex")

        results["total_found"] = len(results["results"])

        # Format and save
        if output_format == "markdown":
            formatted = self._format_markdown(results)
        else:
            formatted = json.dumps(results, indent=2, ensure_ascii=False)

        if save_to_file:
            filename = self._generate_filename(keywords, output_format)
            filepath = self.output_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(formatted)
            print(f"Results saved to: {filepath}")
            results["saved_to"] = str(filepath)

        return results

    def _format_markdown(self, results: Dict[str, Any]) -> str:
        """Convert results to Markdown format."""
        lines = [
            "# Literature Search Results",
            "",
            f"**Query**: {', '.join(results['query'])}",
            f"**Search Date**: {results['search_timestamp']}",
            f"**Sources**: {', '.join(results['search_params']['sources'])}",
            f"**Total Papers Found**: {results['total_found']}",
            "",
            "## Search Parameters",
            "",
        ]

        params = results["search_params"]
        if params.get("authors"):
            lines.append(f"- **Authors**: {params['authors']}")
        if params.get("year_min") or params.get("year_max"):
            year_range = f"{params.get('year_min', '?')}-{params.get('year_max', '?')}"
            lines.append(f"- **Year Range**: {year_range}")
        if params.get("category"):
            lines.append(f"- **Category**: {params['category']}")

        lines.extend(["", "## Results", ""])

        for i, paper in enumerate(results["results"], 1):
            lines.append(f"### {i}. {paper.get('title', 'Untitled')}")
            lines.append("")

            if paper.get("authors"):
                authors = paper["authors"]
                if isinstance(authors, list):
                    authors = ", ".join(authors[:3])  # Show first 3
                    if len(paper["authors"]) > 3:
                        authors += f", et al. (+{len(paper['authors']) - 3})"
                lines.append(f"**Authors**: {authors}")

            if paper.get("year"):
                lines.append(f"**Year**: {paper['year']}")

            if paper.get("arxiv_id"):
                lines.append(
                    f"**arXiv ID**: [{paper['arxiv_id']}](https://arxiv.org/abs/{paper['arxiv_id']})"
                )
            elif paper.get("source_id"):
                lines.append(f"**ID**: {paper['source_id']}")

            if paper.get("citations"):
                lines.append(f"**Citations**: {paper['citations']}")

            if paper.get("abstract"):
                abstract = paper["abstract"]
                if len(abstract) > 300:
                    abstract = abstract[:300] + "..."
                lines.append(f"\n**Abstract**: {abstract}\n")

            if paper.get("url"):
                lines.append(f"**Link**: {paper['url']}")

            lines.append("")

        return "\n".join(lines)

    def _generate_filename(self, keywords: List[str], format_type: str) -> str:
        """Generate a filename for results."""
        keyword_str = "_".join(keywords[:2]).replace(" ", "_").lower()[:20]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = "md" if format_type == "markdown" else "json"
        return f"papers_{keyword_str}_{timestamp}.{ext}"


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Search academic literature across arXiv and Semantic Scholar"
    )
    parser.add_argument("keywords", nargs="+", help="Search keywords")
    parser.add_argument("--authors", help="Author names to filter by")
    parser.add_argument("--year-min", type=int, help="Minimum publication year")
    parser.add_argument("--year-max", type=int, help="Maximum publication year")
    parser.add_argument("--category", help="arXiv category (e.g., cs.AI)")
    parser.add_argument(
        "--sources",
        nargs="+",
        choices=["arxiv", "semantic", "serpapi", "core", "cnki", "cnki_xuetang", "baidu_scholar", "openalex"],
        default=["arxiv", "semantic"],
        help="Sources to search",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--max-results", type=int, default=50, help="Maximum results per source"
    )
    parser.add_argument(
        "--output-dir", default="./outputs", help="Directory to save results"
    )
    parser.add_argument("--semantic-key", help="API key for Semantic Scholar")
    parser.add_argument("--serpapi-key", help="API key for SerpApi")
    parser.add_argument("--core-key", help="API key for Core API")
    parser.add_argument("--cnki-username", help="CNKI username")
    parser.add_argument("--cnki-password", help="CNKI password")
    parser.add_argument("--baidu-key", help="API key for Baidu Qianfan")
    parser.add_argument("--openalex-key", help="API key for OpenAlex")
    parser.add_argument(
        "--no-save", action="store_true", help="Don't save results to file"
    )

    args = parser.parse_args()

    sources = args.sources

    searcher = LiteratureSearcher(
        output_dir=args.output_dir,
        semantic_api_key=args.semantic_key,
        serpapi_key=args.serpapi_key,
        core_api_key=args.core_key,
        cnki_username=args.cnki_username,
        cnki_password=args.cnki_password,
        baidu_api_key=args.baidu_key,
        openalex_api_key=args.openalex_key,
    )

    results = searcher.search(
        keywords=args.keywords,
        authors=args.authors,
        year_min=args.year_min,
        year_max=args.year_max,
        category=args.category,
        sources=sources,
        output_format=args.format,
        max_results=args.max_results,
        save_to_file=not args.no_save,
    )

    # Print summary
    print(f"\n✓ Search complete. Found {results['total_found']} papers.")
    if results.get("saved_to"):
        print(f"✓ Results saved to: {results['saved_to']}")


if __name__ == "__main__":
    main()
