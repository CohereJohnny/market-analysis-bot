"""
EIA Data Extractor MCP Tool - Extract U.S. energy data from EIA Open Data API.
"""

import json
import logging
import os
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from north_mcp_python_sdk import NorthMCPServer

import pandas as pd

from utils.auth import get_authenticated_user
from utils.eia_client import EIAClient

logger = logging.getLogger(__name__)


def register_eia_data_extractor(mcp: "NorthMCPServer") -> None:
    """
    Register the EIA data extractor tool with the MCP server.
    
    Args:
        mcp: The NorthMCPServer instance
    """
    
    # Initialize EIA client
    api_key = os.getenv("EIA_API_KEY")
    if not api_key:
        logger.error("EIA_API_KEY not found in environment variables")
        logger.error("Register at: https://signups.eia.gov/api/signup/")
        # Still register tool but it will error when used
    
    @mcp.tool()
    def eia_data_extractor(
        path: str,
        facets: str = "",
        start: str = "",
        end: str = "",
        frequency: str = "monthly",
        limit: int = 100
    ) -> str:
        """
        Extract energy data from the U.S. Energy Information Administration (EIA) API.
        
        This tool provides access to authoritative U.S. energy data including petroleum
        prices, natural gas prices, production volumes, and forecasts. Essential for
        analyzing NYMEX futures (WTI, Brent, Natural Gas).
        
        Args:
            path: API endpoint path after /v2/ (required)
                Examples:
                - "petroleum/pri/spt" - Petroleum spot prices
                - "natural-gas/pri/sum" - Natural gas prices
                - "petroleum/prod/sum" - Production data
                - "steo" - Short-Term Energy Outlook forecasts
            
            facets: Optional JSON string for filtering by series ID
                Format: '{"series": ["SERIES_ID"]}'
                Examples:
                - '{"series": ["RWTC"]}' - WTI Cushing spot price
                - '{"series": ["RBRTE"]}' - Brent crude spot price
                - '{"series": ["MCRFPUS1"]}' - U.S. crude production
            
            start: Optional start date (YYYY-MM-DD or YYYY-MM)
                Example: "2025-01-01"
            
            end: Optional end date (YYYY-MM-DD or YYYY-MM)
                Example: "2025-10-30"
            
            frequency: Data frequency - daily, weekly, monthly, annual
                Default: "monthly"
            
            limit: Maximum rows to return (default: 100, max: 5000)
        
        Returns:
            Formatted markdown table with energy data and metadata
        
        Common Query Patterns:
            
            WTI Spot Prices (weekly):
                path="petroleum/pri/spt"
                facets='{"series":["RWTC"]}'
                frequency="weekly"
            
            Brent Spot Prices:
                path="petroleum/pri/spt"
                facets='{"series":["RBRTE"]}'
                frequency="weekly"
            
            Henry Hub Natural Gas:
                path="natural-gas/pri/sum"
                frequency="monthly"
            
            U.S. Crude Production:
                path="petroleum/prod/sum"
                facets='{"series":["MCRFPUS1"]}'
                frequency="monthly"
            
            STEO WTI Forecast:
                path="steo"
                facets='{"series":["WTIPUUS"]}'
                frequency="monthly"
        
        Series ID Reference:
            - RWTC: WTI Cushing Spot Price ($/barrel)
            - RBRTE: Brent Europe Spot Price ($/barrel)
            - MCRFPUS1: U.S. Field Production of Crude Oil (Thousand Barrels per Day)
            - WTIPUUS: STEO WTI Price Forecast ($/barrel)
        
        Browse all series: https://www.eia.gov/opendata/browser/
        """
        logger.info(f"EIA data extractor called with path='{path}', frequency='{frequency}'")
        
        # Log authenticated user if present
        user = get_authenticated_user()
        if user:
            logger.info(f"EIA query by authenticated user: {user.email}")
        
        # Check for API key
        if not api_key:
            return (
                "❌ **EIA API Key Not Configured**\n\n"
                "The EIA_API_KEY environment variable is not set.\n\n"
                "**To get an API key:**\n"
                "1. Visit: https://signups.eia.gov/api/signup/\n"
                "2. Register for a free API key\n"
                "3. Add to .env file: EIA_API_KEY=your-key-here\n"
                "4. Restart the server"
            )
        
        try:
            # Initialize client
            client = EIAClient(api_key)
            
            # Parse facets if provided
            facets_dict = None
            if facets:
                try:
                    facets_dict = json.loads(facets)
                except json.JSONDecodeError as e:
                    return (
                        f"❌ **Invalid Facets JSON**\n\n"
                        f"Error: {str(e)}\n\n"
                        f"**Example facets format:**\n"
                        f'```json\n{{"series": ["RWTC"]}}\n```\n\n'
                        f"Your input: `{facets}`"
                    )
            
            # Make API query
            data = client.query(
                path=path,
                facets=facets_dict,
                start=start or None,
                end=end or None,
                frequency=frequency,
                limit=limit
            )
            
            # Extract data from response
            response_data = data.get("response", {})
            records = response_data.get("data", [])
            
            if not records:
                return (
                    "ℹ️ **No Data Found**\n\n"
                    f"The query returned no results.\n\n"
                    f"**Query Details:**\n"
                    f"- Path: `{path}`\n"
                    f"- Frequency: `{frequency}`\n"
                    f"- Date Range: {start or 'not specified'} to {end or 'not specified'}\n"
                    f"- Facets: {facets or 'none'}\n\n"
                    f"**Suggestions:**\n"
                    f"- Try a broader date range\n"
                    f"- Check the series ID in facets\n"
                    f"- Verify the path is correct\n"
                    f"- Browse available data: https://www.eia.gov/opendata/browser/"
                )
            
            # Convert to DataFrame for formatting
            df = pd.DataFrame(records)
            
            # Format the response
            return _format_response(df, path, frequency, facets, len(records))
            
        except ValueError as e:
            # Parameter validation errors
            return f"❌ **Invalid Parameters**\n\n{str(e)}"
        
        except Exception as e:
            # API or other errors
            logger.error(f"EIA data extractor error: {e}", exc_info=True)
            return (
                f"❌ **Error Querying EIA API**\n\n"
                f"{str(e)}\n\n"
                f"**Troubleshooting:**\n"
                f"- Check your API key is valid\n"
                f"- Verify the path exists: https://www.eia.gov/opendata/browser/\n"
                f"- Check series ID in facets\n"
                f"- Ensure date format is YYYY-MM-DD or YYYY-MM"
            )
    
    logger.debug("eia_data_extractor tool handler registered")


def _format_response(
    df: pd.DataFrame,
    path: str,
    frequency: str,
    facets: str,
    record_count: int
) -> str:
    """
    Format EIA data as markdown with table and metadata.
    
    Args:
        df: DataFrame with EIA data
        path: API path used
        frequency: Data frequency
        facets: Facets filter used
        record_count: Number of records
    
    Returns:
        Formatted markdown string
    """
    # Determine what kind of data this is
    if "petroleum" in path and "pri" in path:
        data_type = "Petroleum Prices"
    elif "natural-gas" in path and "pri" in path:
        data_type = "Natural Gas Prices"
    elif "prod" in path:
        data_type = "Production Data"
    elif "steo" in path:
        data_type = "STEO Forecast"
    else:
        data_type = "Energy Data"
    
    # Build response
    response = f"## {data_type}\n\n"
    
    # Format table based on available columns
    if "value" in df.columns and "period" in df.columns:
        # Most common case: period and value
        table_df = df[["period", "value"]].copy()
        
        # Format value based on data type
        if "price" in data_type.lower() or "steo" in path.lower():
            table_df["value"] = table_df["value"].apply(lambda x: f"${x:.2f}")
            table_df.columns = ["Period", "Price"]
        else:
            table_df["value"] = table_df["value"].apply(lambda x: f"{x:,.2f}")
            table_df.columns = ["Period", "Value"]
        
        # Convert to markdown
        response += table_df.to_markdown(index=False)
    else:
        # Fallback: show all columns
        response += df.to_markdown(index=False)
    
    # Add summary statistics
    if "value" in df.columns and len(df) > 1:
        latest = df.iloc[0]["value"]
        oldest = df.iloc[-1]["value"]
        avg = df["value"].mean()
        
        response += f"\n\n### Summary\n"
        response += f"- **Latest**: {latest:.2f}\n"
        response += f"- **Average**: {avg:.2f}\n"
        
        if len(df) > 2:
            change = ((latest - oldest) / oldest) * 100
            response += f"- **Change**: {change:+.1f}% over period\n"
    
    # Add metadata
    response += f"\n\n### Metadata\n"
    response += f"- **Source**: EIA Open Data API\n"
    response += f"- **Path**: `{path}`\n"
    response += f"- **Frequency**: {frequency.capitalize()}\n"
    response += f"- **Records**: {record_count}\n"
    
    if facets:
        try:
            facets_dict = json.loads(facets)
            if "series" in facets_dict:
                response += f"- **Series**: {', '.join(facets_dict['series'])}\n"
        except:
            pass
    
    response += f"\n*Data updated regularly by U.S. Energy Information Administration*"
    
    return response

