#!/usr/bin/env python3
"""
知网研学开放平台 API (CNKI) integration module.
Provides access to Chinese academic literature including journals, conference papers, theses.

API Documentation: http://openx--cnki--net--https.cnki.mdjsf.utuvpn.utuedu.com:9000/docs/guide/file_api.html
"""

import requests
from typing import List, Dict, Any, Optional
import time
import os


class CNKISearcher:
    """
    Client for 知网研学开放平台 API.
    Provides access to Chinese academic literature database.
    
    Authentication: JWT token via username + password
    Base URL: http://gateway--cnki--net--https.cnki.mdjsf.utuvpn.utuedu.com:9000/openx/
    """

    BASE_URL = "http://gateway--cnki--net--https.cnki.mdjsf.utuvpn.utuedu.com:9000/openx"

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None, delay: float = 3.0):
        """
        Initialize CNKI searcher.

        Args:
            username: CNKI platform username (or set CNKI_USERNAME env var)
            password: CNKI platform password (or set CNKI_PASSWORD env var)
            delay: Delay (seconds) between API requests
        """
        self.delay = delay
        self.last_request_time = 0
        self.access_token = None
        
        # Get credentials from parameters or environment variables
        self.username = username or os.environ.get("CNKI_USERNAME")
        self.password = password or os.environ.get("CNKI_PASSWORD")
        
        # Authenticate if credentials are available
        if self.username and self.password:
            self._authenticate()
        else:
            print("Warning: CNKI credentials not provided. Set CNKI_USERNAME and CNKI_PASSWORD environment variables.")

    def _authenticate(self):
        """Authenticate with CNKI platform to obtain JWT access token."""
        try:
            auth_url = f"{self.BASE_URL}/auth/login"
            
            response = requests.post(
                auth_url,
                json={"username": self.username, "password": self.password},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get("success"):
                self.access_token = data.get("content", {}).get("token")
                print("CNKI authentication successful")
            else:
                print(f"CNKI authentication failed: {data.get('message')}")
                self.access_token = None
                
        except Exception as e:
            print(f"CNKI authentication error: {e}")
            self.access_token = None

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with Authorization."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "LiteratureSearchSkill/1.0"
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def _rate_limit(self):
        """Enforce rate limiting between API requests."""
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
        """
        Search CNKI for academic literature.

        Args:
            keywords: List of search terms (Chinese or English)
            authors: Author name(s) to filter by
            year_min: Minimum publication year
            year_max: Maximum publication year
            max_results: Maximum number of results

        Returns:
            List of paper dictionaries with metadata
        """
        if not self.access_token:
            print("Warning: CNKI search requires authentication. Skipping search.")
            return []

        query = " ".join(keywords)
        search_url = f"{self.BASE_URL}/literature/search"
        
        params = {
            "query": query,
            "pageSize": min(max_results, 100),
            "pageNum": 0,
        }
        
        # Add year filter if specified
        if year_min or year_max:
            year_filter = []
            if year_min:
                year_filter.append(f"publishYear:>={year_min}")
            if year_max:
                year_filter.append(f"publishYear:<={year_max}")
            params["filters"] = " AND ".join(year_filter)
        
        # Add author filter
        if authors:
            if isinstance(authors, list):
                params["author"] = authors[0]  # CNKI may only support single author
            else:
                params["author"] = authors

        self._rate_limit()

        try:
            print(f"Querying CNKI: {query}")
            response = requests.get(
                search_url,
                params=params,
                headers=self._get_headers(),
                timeout=15
            )
            response.raise_for_status()
            
            data = response.json()
            if not data.get("success"):
                print(f"CNKI search failed: {data.get('message')}")
                return []
            
            results = data.get("content", {}).get("data", [])
            papers = []
            
            for item in results[:max_results]:
                paper = self._parse_result(item)
                if paper:
                    papers.append(paper)
            
            return papers
            
        except Exception as e:
            print(f"CNKI search error: {e}")
            return []

    def _parse_result(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse CNKI API response item into standard paper format."""
        try:
            return {
                "title": item.get("title", ""),
                "authors": item.get("authors", []),
                "year": item.get("publishYear"),
                "source": item.get("sourceName", ""),  # Journal/conference name
                "abstract": item.get("abstract", ""),
                "doi": item.get("doi", ""),
                "url": item.get("url", ""),
                "cnki_id": item.get("literatureId", ""),
                "type": item.get("literatureType", ""),  # journal, conference, dissertation, etc.
            }
        except Exception as e:
            print(f"Error parsing CNKI result: {e}")
            return None