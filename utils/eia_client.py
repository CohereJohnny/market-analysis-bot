"""
EIA API Client for Market Analysis Bot.
Provides HTTP client for querying U.S. Energy Information Administration Open Data API v2.
"""

import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

import requests


logger = logging.getLogger(__name__)


class EIAClient:
    """
    Client for EIA Open Data API v2.
    
    The EIA (U.S. Energy Information Administration) provides authoritative data on:
    - Petroleum prices (WTI, Brent crude oil spot prices)
    - Natural gas prices (Henry Hub)
    - Production volumes (crude oil, natural gas)
    - Imports/exports
    - Short-Term Energy Outlook (STEO) forecasts
    
    API Documentation: https://www.eia.gov/opendata/documentation.php
    Rate Limit: 5,000 requests per hour
    """
    
    BASE_URL = "https://api.eia.gov/v2"
    RATE_LIMIT = 5000  # requests per hour
    RATE_LIMIT_WARNING = 4000  # warn at 80%
    
    def __init__(self, api_key: str):
        """
        Initialize EIA API client.
        
        Args:
            api_key: EIA API key (register at https://signups.eia.gov/api/signup/)
        
        Raises:
            ValueError: If API key is missing or empty
        """
        if not api_key:
            raise ValueError(
                "EIA API key required. Register at: "
                "https://signups.eia.gov/api/signup/"
            )
        
        self.api_key = api_key
        self.request_count = 0
        self.last_reset = datetime.now()
        
        logger.info("EIA API client initialized")
    
    def query(
        self,
        path: str,
        facets: Optional[Dict[str, Any]] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        frequency: str = "monthly",
        data_fields: List[str] = None,
        sort: Optional[List[Dict[str, str]]] = None,
        limit: int = 5000
    ) -> Dict[str, Any]:
        """
        Query EIA API for energy data.
        
        Args:
            path: API endpoint path after /v2/ (e.g., "petroleum/pri/spt")
            facets: Optional dict for filtering (e.g., {"series": ["RWTC"]})
            start: Start date (YYYY-MM-DD or YYYY-MM)
            end: End date (YYYY-MM-DD or YYYY-MM)
            frequency: Data frequency (daily, weekly, monthly, annual)
            data_fields: Fields to return (default: ["value"])
            sort: Sort configuration (e.g., [{"column": "period", "direction": "desc"}])
            limit: Maximum rows to return (max 5000)
        
        Returns:
            Dict containing response data
        
        Raises:
            requests.HTTPError: For API errors (4xx, 5xx)
            requests.Timeout: For timeout errors
            ValueError: For invalid parameters
        
        Example:
            >>> client = EIAClient(api_key="YOUR_KEY")
            >>> data = client.query(
            ...     path="petroleum/pri/spt",
            ...     facets={"series": ["RWTC"]},
            ...     frequency="weekly",
            ...     start="2025-01-01"
            ... )
        """
        # Check rate limit
        self._check_rate_limit()
        
        # Validate parameters
        self._validate_params(path, frequency, limit)
        
        # Build request parameters
        params = self._build_params(
            facets=facets,
            start=start,
            end=end,
            frequency=frequency,
            data_fields=data_fields or ["value"],
            sort=sort,
            limit=limit
        )
        
        # Make API request
        url = f"{self.BASE_URL}/{path}/data/"
        
        try:
            logger.debug(f"EIA API request: {path} with params: {params}")
            
            response = requests.get(
                url,
                params=params,
                timeout=30
            )
            
            self.request_count += 1
            
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"EIA API response: {len(data.get('response', {}).get('data', []))} records")
            
            return data
            
        except requests.Timeout:
            logger.error(f"EIA API timeout for path: {path}")
            raise requests.Timeout(
                "EIA API request timed out. Please try again or check your network connection."
            )
        
        except requests.HTTPError as e:
            logger.error(f"EIA API error: {e.response.status_code} - {e.response.text}")
            
            if e.response.status_code == 401:
                raise requests.HTTPError(
                    "Invalid EIA API key. Please check your API key or register at: "
                    "https://signups.eia.gov/api/signup/",
                    response=e.response
                )
            
            elif e.response.status_code == 429:
                raise requests.HTTPError(
                    "EIA API rate limit exceeded (5,000 requests/hour). "
                    "Please wait before making more requests.",
                    response=e.response
                )
            
            elif e.response.status_code == 404:
                raise requests.HTTPError(
                    f"Invalid EIA API path: '{path}'. "
                    f"Check available paths at: https://www.eia.gov/opendata/browser/",
                    response=e.response
                )
            
            else:
                raise
    
    def _validate_params(self, path: str, frequency: str, limit: int) -> None:
        """Validate query parameters."""
        if not path:
            raise ValueError("Path parameter is required")
        
        valid_frequencies = ["daily", "weekly", "monthly", "annual"]
        if frequency not in valid_frequencies:
            raise ValueError(
                f"Invalid frequency: '{frequency}'. "
                f"Valid options: {', '.join(valid_frequencies)}"
            )
        
        if limit > 5000:
            logger.warning(f"Limit {limit} exceeds maximum 5000, capping at 5000")
            limit = 5000
    
    def _build_params(
        self,
        facets: Optional[Dict[str, Any]],
        start: Optional[str],
        end: Optional[str],
        frequency: str,
        data_fields: List[str],
        sort: Optional[List[Dict[str, str]]],
        limit: int
    ) -> Dict[str, Any]:
        """Build API request parameters."""
        params = {
            "api_key": self.api_key,
            "frequency": frequency,
            "data[0]": ",".join(data_fields),
            "limit": min(limit, 5000)
        }
        
        if start:
            params["start"] = start
        
        if end:
            params["end"] = end
        
        if facets:
            # EIA API expects facets as URL parameters
            # Format: facets[key][]=value
            for key, values in facets.items():
                if isinstance(values, list):
                    for value in values:
                        params[f"facets[{key}][]"] = value
                else:
                    params[f"facets[{key}][]"] = values
        
        if sort:
            params["sort"] = json.dumps(sort)
        
        return params
    
    def _check_rate_limit(self) -> None:
        """Check and warn about rate limit usage."""
        # Reset counter if hour has passed
        now = datetime.now()
        hours_passed = (now - self.last_reset).total_seconds() / 3600
        
        if hours_passed >= 1.0:
            logger.debug(f"Resetting rate limit counter (was {self.request_count})")
            self.request_count = 0
            self.last_reset = now
        
        # Warn if approaching limit
        if self.request_count >= self.RATE_LIMIT_WARNING:
            remaining = self.RATE_LIMIT - self.request_count
            logger.warning(
                f"Approaching EIA API rate limit: {self.request_count}/{self.RATE_LIMIT} requests used. "
                f"{remaining} requests remaining this hour."
            )

