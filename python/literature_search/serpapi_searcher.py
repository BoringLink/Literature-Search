#!/usr/bin/env python3
"""
SerpApi (Google Scholar) integration module.
Provides access to Google Scholar search results.
"""

import requests
from typing import List, Dict, Any, Optional
import time
import os


class SerpApiSearcher:
    """
    Client for SerpApi Google Scholar API.
    Provides access to Google Scholar search results with rich metadata.
    Requires an API key from serpapi.com.
    """

    BASE_URL = "https://serpapi.com/search"

    def __init__(self, api_key: Optional[str] = None, delay: float = 2.0):
        """
        Initialize SerpApi searcher.

        Args:
            api_key: SerpApi API key (required)
            delay: Delay (seconds) between API requests
        """
        self.api_key = api_key
        self.delay = delay
        self.last_request_time = 0

        if not api_key:
            # Try to get from environment variable
            self.api_key = os.environ.get("SERPAPI_KEY")

    def search(
        self,
        keywords: List[str],
        authors: Optional[str | List[str]] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Search Google Scholar via SerpApi.

        Args:
            keywords: List of search terms
            authors: Author name(s) to filter by (can use author: prefix in query)
            year_min: Minimum publication year (using as_ylo parameter)
            year_max: Maximum publication year (using as_yhi parameter)
            max_results: Maximum number of results (max 100 per request)

        Returns:
            List of paper dictionaries with metadata
        """
        if not self.api_key:
            raise ValueError("SerpApi API key is required. Set SERPAPI_KEY environment variable or pass api_key parameter.")

        # Combine keywords into search query
        query = " ".join(keywords)
        
        # Add author filter if specified
        if authors:
            if isinstance(authors, list):
                authors_str = " OR ".join([f'author:"{author}"' for author in authors])
            else:
                authors_str = f'author:"{authors}"'
            query = f"{query} {authors_str}"

        # Construct request
        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": self.api_key,
            "num": min(max_results, 20),  # SerpApi limits to 20 results per page
        }

        # Add year filters
        if year_min:
            params["as_ylo"] = year_min
        if year_max:
            params["as_yhi"] = year_max

        # Rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        try:
            print(f"Querying SerpApi (Google Scholar): {query}")
            response = requests.get(
                self.BASE_URL, params=params, timeout=10
            )
            response.raise_for_status()
            self.last_request_time = time.time()
            
            data = response.json()
            
            # Extract organic results
            organic_results = data.get("organic_results", [])
            
            results = []
            for item in organic_results:
                # Extract authors from the publication info
                authors_list = []
                publication_info = item.get("publication_info", {})
                authors_str = publication_info.get("authors", "")
                
                # Parse authors string (format: "Author1, Author2, Author3...")
                if authors_str:
                    # Simple parsing - split by comma and clean up
                    authors_list = [author.strip() for author in authors_str.split(",") if author.strip()]
                
                result = {
                    "title": item.get("title", ""),
                    "authors": authors_list,
                    "year": self._extract_year(publication_info),
                    "abstract": item.get("snippet", ""),
                    "venue": publication_info.get("summary", ""),
                    "citation_count": item.get("cited_by", {}).get("value", 0),
                    "url": item.get("link", ""),
                    "source": "serpapi",
                    "rank": item.get("position", 0)
                }
                results.append(result)
                
            # Handle pagination if we need more results
            if len(results) < max_results and "pagination" in data:
                # For simplicity, we're just getting the first page
                # In a full implementation, we would handle pagination
                pass
                
            return results[:max_results]
            
        except Exception as e:
            print(f"Error querying SerpApi: {e}")
            return []

    def _extract_year(self, publication_info: Dict[str, Any]) -> Optional[int]:
        """
        Extract year from publication info.
        """
        summary = publication_info.get("summary", "")
        # Look for 4-digit year in the summary
        import re
        year_match = re.search(r'\b(19|20)\d{2}\b', summary)
        if year_match:
            return int(year_match.group())
        return None