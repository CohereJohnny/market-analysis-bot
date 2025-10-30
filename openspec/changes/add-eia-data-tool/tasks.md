# Implementation Tasks: Add EIA Data Tool

## 1. EIA API Client Development
- [ ] 1.1 Create utils/eia_client.py module
- [ ] 1.2 Implement EIAClient class with initialization
- [ ] 1.3 Add API key loading from environment
- [ ] 1.4 Implement base HTTP request method
- [ ] 1.5 Add query parameter building (path, facets, dates, frequency)
- [ ] 1.6 Implement JSON response parsing
- [ ] 1.7 Add error handling for API failures (4xx, 5xx)
- [ ] 1.8 Implement rate limit handling
- [ ] 1.9 Add request logging for debugging

## 2. Core Tool Implementation
- [ ] 2.1 Create tools/eia_data_extractor.py
- [ ] 2.2 Define tool registration function
- [ ] 2.3 Implement eia_data_extractor tool handler
- [ ] 2.4 Add comprehensive docstring with examples
- [ ] 2.5 Implement parameter validation
- [ ] 2.6 Add facets JSON parsing and validation
- [ ] 2.7 Implement date format validation
- [ ] 2.8 Add frequency validation
- [ ] 2.9 Connect to EIAClient for data retrieval

## 3. Data Formatting & Response
- [ ] 3.1 Implement pandas DataFrame conversion
- [ ] 3.2 Add markdown table formatting
- [ ] 3.3 Implement data summarization (count, latest value, trends)
- [ ] 3.4 Add period/date formatting for readability
- [ ] 3.5 Implement price formatting ($/barrel, $/MMBtu)
- [ ] 3.6 Add metadata to responses (source, date range, series ID)
- [ ] 3.7 Handle empty result sets gracefully

## 4. Common Query Patterns
- [ ] 4.1 Implement WTI spot price query helper
- [ ] 4.2 Implement Brent spot price query helper
- [ ] 4.3 Implement Henry Hub natural gas query helper
- [ ] 4.4 Implement U.S. crude production query helper
- [ ] 4.5 Implement STEO forecast query helper
- [ ] 4.6 Add query pattern documentation
- [ ] 4.7 Create series ID reference guide

## 5. Vernacular Mapping
- [ ] 5.1 Create trading term to series ID mapping
- [ ] 5.2 Map WTI → RWTC series
- [ ] 5.3 Map Brent → RBRTE series
- [ ] 5.4 Map Henry Hub → natural gas series
- [ ] 5.5 Map production terms → production series
- [ ] 5.6 Document vernacular mappings in tool

## 6. Error Handling
- [ ] 6.1 Handle missing API key gracefully
- [ ] 6.2 Handle invalid path errors
- [ ] 6.3 Handle invalid series ID in facets
- [ ] 6.4 Handle date format errors
- [ ] 6.5 Handle API rate limit exceeded (429)
- [ ] 6.6 Handle API timeout errors
- [ ] 6.7 Handle empty data responses
- [ ] 6.8 Add user-friendly error messages

## 7. Tool Registration
- [ ] 7.1 Update tools/__init__.py to import EIA tool
- [ ] 7.2 Add register_eia_data_extractor call
- [ ] 7.3 Update tool count logging
- [ ] 7.4 Test tool appears in MCP list

## 8. Testing
- [ ] 8.1 Create tests/test_eia_client.py
- [ ] 8.2 Test EIAClient initialization
- [ ] 8.3 Test query parameter building
- [ ] 8.4 Test successful API responses (mocked)
- [ ] 8.5 Test error handling (mocked failures)
- [ ] 8.6 Create tests/test_eia_tool.py
- [ ] 8.7 Test tool with valid parameters
- [ ] 8.8 Test tool with invalid parameters
- [ ] 8.9 Test table formatting
- [ ] 8.10 Integration test with MCP Inspector

## 9. Documentation
- [ ] 9.1 Update README with EIA tool section
- [ ] 9.2 Add EIA_API_KEY to .env.example
- [ ] 9.3 Document common query examples
- [ ] 9.4 Create series ID reference guide
- [ ] 9.5 Add troubleshooting section
- [ ] 9.6 Document API rate limits
- [ ] 9.7 Add example tool responses

## 10. Validation
- [ ] 10.1 Test with actual EIA API key
- [ ] 10.2 Verify WTI spot price queries
- [ ] 10.3 Verify Brent price queries
- [ ] 10.4 Verify Henry Hub queries
- [ ] 10.5 Verify production data queries
- [ ] 10.6 Verify STEO forecast queries
- [ ] 10.7 Test with MCP Inspector
- [ ] 10.8 Validate table formatting in responses
- [ ] 10.9 Run unit tests (pytest)
- [ ] 10.10 OpenSpec validation (openspec validate --strict)

