#!/usr/bin/env python3
"""OpenAlex API integration module."""

import requests
from typing import List, Dict, Any, Optional
import time
import os


class OpenAlexSearcher:
    BASE_URL = "https://api.openalex.org"

    def __init__(self, api_key: Optional[str] = None, delay: float = 1.0):
        self.api_key = api_key or os.environ.get("OPENALEX_API_KEY")
        self.delay = delay
        self.last_request_time = 0
        
        if not self.api_key:
            print("Warning: OPENALEX_API_KEY not set. Using anonymous access (limited).")

    def _get_headers(self) -> Dict[str, str]:
        headers = {"User-Agent": "LiteratureSearchSkill/1.0"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()

    def search(
        self,
        keywords: List[str],
        authors: Optional[str | List[str]] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        if not keywords:
            return []

        query = " ".join(keywords)
        
        filters = []
        if year_min:
            filters.append(f"publication_year:>={year_min}")
        if year_max:
            filters.append(f"publication_year:<={year_max}")
        if authors:
            if isinstance(authors, list):
                author_query = " OR ".join([f"author.display_name.search:{a}" for a in authors])
                filters.append(f"({author_query})")
            else:
                filters.append(f"author.display_name.search:{authors}")

        papers = []
        cursor = "*"
        
        while len(papers) < max_results:
            self._rate_limit()
            
            url = f"{self.BASE_URL}/works"
            params = {
                "filter": ",".join(filters) if filters else None,
                "search": query,
                "per_page": min(200, max_results - len(papers)),
                "cursor": cursor,
                "select": "id,title,author,publication_year,abstract_inverted_index,doi,host_venue,citations_count,references_count,is_open_access,open_access,url",
            }
            
            params = {k: v for k, v in params.items() if v is not None}

            try:
                print(f"Querying OpenAlex: {query}")
                response = requests.get(
                    url,
                    params=params,
                    headers=self._get_headers(),
                    timeout=15
                )
                response.raise_for_status()
                
                data = response.json()
                results = data.get("results", [])
                
                for item in results:
                    paper = self._parse_result(item)
                    if paper:
                        papers.append(paper)
                
                cursor = data.get("meta", {}).get("next_cursor")
                if not cursor:
                    break
                    
            except Exception as e:
                print(f"OpenAlex search error: {e}")
                break

        return papers[:max_results]

    def _parse_result(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            authors_list = []
            for author in item.get("author", []):
                if "display_name" in author:
                    authors_list.append(author["display_name"])
            
            abstract = None
            if item.get("abstract_inverted_index"):
                index = item["abstract_inverted_index"]
                words = sorted(
                    [(word, pos) for word, positions in index.items() for pos in positions],
                    key=lambda x: x[1]
                )
                abstract = " ".join([word for word, _ in words])
            
            return {
                "title": item.get("title", ""),
                "authors": authors_list,
                "year": item.get("publication_year"),
                "source": item.get("host_venue", {}).get("display_name", ""),
                "abstract": abstract,
                "doi": item.get("doi", ""),
                "url": item.get("open_access", {}).get("oa_url") or item.get("url", ""),
                "citations": item.get("citations_count", 0),
                "references": item.get("references_count", 0),
                "is_open_access": item.get("is_open_access", False),
            }
        except Exception as e:
            print(f"Error parsing OpenAlex result: {e}")
            return None