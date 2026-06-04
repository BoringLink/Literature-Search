#!/usr/bin/env python3
"""
Core API integration module.
Provides access to millions of open access research papers.
"""

import requests
from typing import List, Dict, Any, Optional
import time
import os


class CoreSearcher:
    """
    Client for Core API.
    Provides access to open access research papers from repositories worldwide.
    Requires an API key from core.ac.uk.
    """

    BASE_URL = "https://api.core.ac.uk/v3"

    def __init__(self, api_key: Optional[str] = None, delay: float = 1.0):
        """
        Initialize Core API searcher.

        Args:
            api_key: Core API API key (required for most endpoints)
            delay: Delay (seconds) between API requests
        """
        self.api_key = api_key
        self.delay = delay
        self.last_request_time = 0
        self.headers = {}

        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
        # Try to get from environment variable if not provided
        elif os.environ.get("CORE_API_KEY"):
            self.headers["Authorization"] = f"Bearer {os.environ.get('CORE_API_KEY')}"
   
