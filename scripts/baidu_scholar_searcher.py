#!/usr/bin/env python3
"""
Baidu Qianfan Academic Search API integration module.
Provides access to academic literature search with AI-generated abstracts.

API Documentation: https://cloud.baidu.com/doc/qianfan/s/Amkw9qpzd
"""

import requests
from typing import List, Dict, Any, Optional
import time
import os


class BaiduScholarSearcher:
    """Client for Baidu Qianfan Academic Search API."""

    BASE_URL = "https://qianfan.baidubce.com/v2/tools/baidu_scholar/search"

    def __init__(self, api_key: Optional[str] = None, delay: float = 1.0):
        self.delay = delay
        self.last_request_time = 0
        
        if not self.api_key:
            print("Warning: BAIDU_API_KEY not set. Baidu Scholar search disabled.")

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Appbuilder-From": "openclaw",
            "User-Agent": "LiteratureSearchSkill/1.0"
        }
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
        enable_abstract: bool = True,
    ) -> List[Dict[str, Any]]:
        if not self.api_key:
            return []

        query = " ".join(keywords)
        page_num = 0
        papers = []

        while len(papers) < max_results:
            self._rate_limit()
            
            params = {
                "wd": query,
                "pageNum": page_num,
                "enable_abstract": str(enable_abstract).lower(),
            }

            try:
                print(f"Querying Baidu Scholar: {query} (page {page_num})")
                response = requests.get(
                    self.BASE_URL,
                    params=params,
                    headers=self._get_headers(),
                    timeout=15
                )
                response.raise_for_status()
                
                data = response.json()
                if data.get("code") != 0:
                    print(f"Baidu Scholar error: {data.get('message')}")
                    break
                
                results = data.get("data", [])
                if not results:
                    break
                
                for item in results:
                    paper = self._parse_result(item)
                    if paper:
                        papers.append(paper)
                
                if not data.get("hasMore"):
                    break
                
                page_num += 1
                
            except Exception as e:
                print(f"Baidu Scholar search error: {e}")
                break

        return papers[:max_results]

    def _parse_result(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            return {
                "title": item.get("title", ""),
                "authors": item.get("authors", []),
                "year": item.get("publishYear"),
                "source": item.get("publishInfo", {}).get("journalName", ""),
                "abstract": item.get("aiAbstract") or item.get("abstract", ""),
                "doi": item.get("doi", ""),
                "url": item.get("url", ""),
                "paper_id": item.get("paperId", ""),
            }
        except Exception as e:
            print(f"Error parsing Baidu Scholar result: {e}")
            return None