# Design Document: EIA Data Tool Implementation

## Context
This document outlines the design for implementing the EIA (U.S. Energy Information Administration) data extractor tool for the Market Analysis Bot. This tool provides access to authoritative U.S. energy data including petroleum prices, natural gas prices, production volumes, and forecasts - essential for energy traders analyzing NYMEX futures.

**Background**:
- EIA Open Data API v2 is the authoritative source for U.S. energy statistics
- API uses RESTful structure with JSON responses
- Data updated regularly (e.g., weekly petroleum reports every Wednesday)
- Rate limit: 5,000 requests/hour
- Free API key required (register at https://signups.eia.gov/api/signup/)

**Constraints**:
- Must respect API rate limits
- API key must be stored securely (environment variable)
- Demo environment (not production)
- Keep implementation simple (<250 lines per module)

## Goals / Non-Goals

### Goals
- Provide access to critical U.S. energy data (WTI, Brent, Henry Hub)
- Format responses as readable markdown tables
- Handle common trading queries naturally
- Support flexible date ranges and frequencies
- Implement robust error handling
- Respect API rate limits

### Non-Goals
- Real-time streaming data (API provides near-real-time)
- Complex caching beyond basic rate limit protection
- Multiple API versions (focus on v2 only)
- Data persistence (stateless tool)
- Advanced analytics (just data retrieval)

## Decisions

### Decision 1: Two-Layer Architecture
**Choice**: Separate EIA API client (utils/eia_client.py) from MCP tool (tools/eia_data_extractor.py)

**Rationale**:
- Separation of concerns: HTTP client logic vs. tool interface
- Client can be tested independently
- Client reusable for future tools (e.g., batch queries)
- Cleaner code organization

**Implementation**:
```
utils/eia_client.py (200 lines)
  ├─ EIAClient class
  ├─ query() method for API calls
  └─ Error handling and parsing

tools/eia_data_extractor.py (250 lines)
  ├─ register_eia_data_extractor()
  ├─ MCP tool handler
  ├─ Parameter validation
  └─ Response formatting
```

### Decision 2: Flexible Query Parameters
**Choice**: Support full EIA API flexibility through path + facets approach

**Rationale**:
- EIA API v2 uses path-based endpoints (e.g., petroleum/pri/spt)
- Facets allow filtering by series ID, product, region
- Enables advanced queries without hardcoding every endpoint
- Maintains compatibility with EIA documentation

**Parameters**:
- `path` (required): API endpoint path after /v2/
- `facets` (optional): JSON string for series filtering
- `start`, `end` (optional): Date range
- `frequency` (optional): daily, weekly, monthly, annual
- `limit` (optional): Max rows (default 5000)

**Common Query Examples**:
```python
# WTI spot prices
path="petroleum/pri/spt"
facets='{"series":["RWTC"]}'
frequency="weekly"

# Henry Hub natural gas
path="natural-gas/pri/sum"
frequency="monthly"

# STEO forecasts
path="steo"
facets='{"series":["WTIPUUS"]}'
```

### Decision 3: Markdown Table Formatting
**Choice**: Use pandas DataFrame → markdown for all responses

**Rationale**:
- Traders need scannable data
- Markdown tables render well in chat interfaces
- Pandas provides powerful formatting options
- Consistent with project conventions

**Format**:
```markdown
## WTI Crude Oil Spot Prices

| Period | Price ($/barrel) |
|--------|------------------|
| 2025-10-27 | $71.50 |
| 2025-10-20 | $70.25 |
| 2025-10-13 | $72.10 |

**Source**: EIA - Petroleum Spot Prices
**Series**: RWTC (WTI Cushing)
**Frequency**: Weekly
**Records**: 3
```

### Decision 4: Series ID Reference System
**Choice**: Provide common series IDs in docstring + separate reference guide

**Rationale**:
- EIA uses cryptic series IDs (e.g., "RWTC" for WTI)
- Traders need quick reference for common queries
- Can't hardcode all series (thousands exist)
- Balance between usability and flexibility

**Common Series IDs**:
| Trading Term | Series ID | Path |
|--------------|-----------|------|
| WTI Spot | RWTC | petroleum/pri/spt |
| Brent Spot | RBRTE | petroleum/pri/spt |
| Henry Hub | Various | natural-gas/pri/sum |
| U.S. Crude Production | MCRFPUS1 | petroleum/prod/sum |
| STEO WTI Forecast | WTIPUUS | steo |

### Decision 5: Error Handling Strategy
**Choice**: User-friendly error messages with actionable guidance

**Rationale**:
- API errors can be cryptic
- Traders need to know how to fix issues
- Debug mode can show raw errors

**Error Categories**:
1. **Missing API Key**: Clear message with registration link
2. **Invalid Path**: Suggest checking EIA documentation
3. **Invalid Series ID**: Show example facets format
4. **Rate Limit**: Suggest waiting or using broader queries
5. **Date Format**: Show expected format (YYYY-MM-DD)
6. **No Data**: Indicate empty result set vs. error

**Example Error**:
```
Error: Invalid EIA API path 'petroleum/invalid'

Common paths:
- petroleum/pri/spt (spot prices)
- natural-gas/pri/sum (gas prices)
- petroleum/prod/sum (production)

See: https://www.eia.gov/opendata/browser/
```

### Decision 6: Rate Limit Handling
**Choice**: Simple request counter + warning at 80% limit

**Rationale**:
- 5,000 req/hour is generous for demo
- Complex caching adds unnecessary complexity
- Warning at 4,000 requests prevents hitting limit
- Reset counter hourly

**Implementation**:
- Track request count in EIAClient instance
- Log warning when >4,000 requests in current hour
- Don't block requests (let API return 429 if needed)
- User can restart server to reset counter

### Decision 7: Authentication Integration
**Choice**: Optional user context logging (no auth required for tool)

**Rationale**:
- EIA data is public (only needs API key)
- Tool doesn't need user-specific behavior
- Can log which user made query for analytics
- Consistent with hello_world pattern

**Implementation**:
```python
@mcp.tool()
def eia_data_extractor(path: str, ...) -> str:
    user = get_authenticated_user()
    if user:
        logger.info(f"EIA query by {user.email}")
    # Execute query
```

## Risks / Trade-offs

### Risk 1: API Rate Limits
**Trade-off**: Simple counter vs. sophisticated caching
**Mitigation**: 5,000/hour is generous; warn at 80%

### Risk 2: Series ID Complexity
**Trade-off**: Easy-to-use presets vs. flexible facets
**Mitigation**: Provide common presets in documentation

### Risk 3: Data Freshness
**Trade-off**: Real-time accuracy vs. API update schedules
**Mitigation**: Document update frequencies (weekly reports)

### Risk 4: Large Result Sets
**Trade-off**: Complete data vs. response size
**Mitigation**: Default limit 5000, user can adjust

## Implementation Plan

### Phase 1: EIA Client (1-2 hours)
```python
# utils/eia_client.py
class EIAClient:
    def __init__(self, api_key: str)
    def query(self, path, facets, start, end, ...) -> dict
    def _build_params(...) -> dict
    def _parse_response(response) -> dict
```

### Phase 2: MCP Tool (1-2 hours)
```python
# tools/eia_data_extractor.py
def register_eia_data_extractor(mcp):
    @mcp.tool()
    def eia_data_extractor(...) -> str:
        # Validate params
        # Call EIAClient
        # Format as table
        # Return markdown
```

### Phase 3: Testing (1 hour)
- Unit tests for EIAClient
- Unit tests for tool parameters
- Integration test with real API
- MCP Inspector test

### Phase 4: Documentation (30 min)
- Update README
- Series ID reference
- Common query examples

## File Organization

```
market-analysis-bot/
├── utils/
│   └── eia_client.py          # EIA API client (~200 lines)
├── tools/
│   ├── __init__.py            # Update tool registration
│   └── eia_data_extractor.py  # MCP tool (~250 lines)
├── tests/
│   ├── test_eia_client.py     # Client unit tests
│   └── test_eia_tool.py       # Tool unit tests
└── docs/
    └── eia_series_reference.md # Series ID guide
```

## Testing Strategy

### Unit Tests
- EIAClient parameter building
- EIAClient response parsing
- Tool parameter validation
- Error handling for each error type

### Integration Tests
- Real API calls with test key
- WTI, Brent, Henry Hub queries
- Date range queries
- Empty result handling

### Manual Tests
- MCP Inspector tool invocation
- Multiple query patterns
- Error scenarios

## Open Questions
- ~~Should we cache responses?~~ **Decision**: No, keep simple
- ~~Support multiple series in one query?~~ **Decision**: Yes, via facets
- ~~Hardcode common queries?~~ **Decision**: No, use flexible params + docs

## References
- EIA Open Data API: https://www.eia.gov/opendata/documentation.php
- API Browser: https://www.eia.gov/opendata/browser/
- Series specification: `specs/eia-data.md`
- Project conventions: `openspec/project.md`

