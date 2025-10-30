# Change Proposal: Add EIA Data Tool

## Why
The Market Analysis Bot needs access to authoritative U.S. energy data to complement the global OPEC data. The U.S. Energy Information Administration (EIA) provides the most reliable source for:
- WTI (West Texas Intermediate) and Brent crude oil spot prices
- Henry Hub natural gas prices
- U.S. petroleum production and inventory data
- Short-Term Energy Outlook (STEO) forecasts

Without this tool, traders cannot access critical U.S. market data needed for analyzing NYMEX futures (CLZ25 for WTI, NGZ25 for Natural Gas) and making informed trading decisions.

## What Changes
- Create `eia_data_extractor` MCP tool wrapper for EIA Open Data API v2
- Implement HTTP client for EIA REST API endpoints
- Add support for key data series:
  - Petroleum spot prices (WTI, Brent)
  - Natural gas prices (Henry Hub)
  - Production volumes (crude oil, natural gas)
  - STEO forecasts
  - Import/export data
- Format responses as markdown tables using pandas
- Add comprehensive error handling for API failures
- Implement data caching to respect rate limits (5,000 req/hour)
- Create vernacular mapping for common trading terms
- Write unit tests for all data retrieval functions
- Document supported endpoints and series IDs

## Impact
- **Affected specs**: `eia-tool` (new capability)
- **Affected code**: 
  - `tools/eia_data_extractor.py` - Main tool implementation (~250 lines)
  - `tools/__init__.py` - Register new tool
  - `utils/eia_client.py` - EIA API client (~200 lines)
  - `tests/test_eia_tool.py` - Unit tests
  - `.env.example` - Add EIA_API_KEY variable
- **Dependencies**: None (uses existing requests, pandas)
- **Testing**: Unit tests + integration tests with MCP Inspector
- **Documentation**: 
  - README updates with EIA tool examples
  - Series ID reference guide
  - Common query patterns for traders

## Breaking Changes
None - This is a new capability that doesn't modify existing functionality.

## Migration Notes
N/A - New tool, no migration required.

