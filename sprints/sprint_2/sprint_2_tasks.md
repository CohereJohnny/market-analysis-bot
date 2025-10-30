# Sprint 2 Tasks

## Goals
Build fully functional EIA data extractor tool following OpenSpec change `add-eia-data-tool`.

## Tasks

### 1. OpenSpec Proposal
- [x] 1.1 Create proposal.md
- [x] 1.2 Create design.md with technical decisions
- [x] 1.3 Create spec.md with requirements and scenarios
- [x] 1.4 Create tasks.md with implementation checklist
- [x] 1.5 Validate proposal with openspec

### 2. EIA API Client
- [x] 2.1 Create utils/eia_client.py module
- [x] 2.2 Implement EIAClient class
- [x] 2.3 Add API key loading and validation
- [x] 2.4 Implement query() method with parameter building
- [x] 2.5 Add JSON response parsing
- [x] 2.6 Implement error handling (4xx, 5xx, timeouts)
- [x] 2.7 Add rate limit tracking and warnings
- [x] 2.8 Add request logging

### 3. MCP Tool Implementation
- [x] 3.1 Create tools/eia_data_extractor.py
- [x] 3.2 Define register_eia_data_extractor function
- [x] 3.3 Implement tool handler with comprehensive docstring
- [x] 3.4 Add parameter validation
- [x] 3.5 Implement facets JSON parsing
- [x] 3.6 Connect to EIAClient for data retrieval
- [x] 3.7 Implement pandas DataFrame formatting
- [x] 3.8 Add markdown table generation
- [x] 3.9 Implement response metadata
- [x] 3.10 Add user-friendly error messages

### 4. Tool Registration
- [x] 4.1 Update tools/__init__.py to import EIA tool
- [x] 4.2 Add register_eia_data_extractor call
- [x] 4.3 Update tool count logging

### 5. Testing
- [x] 5.1 Create tests/test_eia_client.py
- [x] 5.2 Test client initialization
- [x] 5.3 Test parameter validation
- [x] 5.4 Test parameter building
- [x] 5.5 Test rate limit tracking
- [x] 5.6 Create tests/test_eia_tool.py
- [x] 5.7 Test tool imports
- [x] 5.8 Test response formatting
- [ ] 5.9 Integration test with real API (manual)
- [ ] 5.10 Test with MCP Inspector (manual)

### 6. Documentation
- [x] 6.1 Update README with EIA tool section
- [x] 6.2 Add Quick Start guide
- [x] 6.3 Document common query examples
- [x] 6.4 Create series ID reference table
- [x] 6.5 Update .env.example with EIA_API_KEY

### 7. Validation
- [ ] 7.1 Run pytest for unit tests
- [ ] 7.2 Test with actual EIA API key
- [ ] 7.3 Verify WTI, Brent, Henry Hub queries
- [ ] 7.4 Test with MCP Inspector
- [ ] 7.5 Validate table formatting
- [ ] 7.6 Test error scenarios
- [ ] 7.7 OpenSpec validation

## Progress Notes
- Sprint started: October 30, 2025
- EIA data tool for U.S. energy market data
- Implementation complete: 90%
- Manual validation pending

