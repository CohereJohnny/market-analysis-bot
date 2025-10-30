# EIA Data Tool Specification

## ADDED Requirements

### Requirement: EIA API Client
The system SHALL provide an HTTP client for querying the EIA Open Data API v2.

#### Scenario: Successful API query
- **WHEN** client is initialized with valid API key
- **AND** query is made with valid path and parameters
- **THEN** client SHALL return parsed JSON data
- **AND** response SHALL include data records

#### Scenario: Missing API key
- **WHEN** client is initialized without API key
- **THEN** client SHALL raise clear error
- **AND** error SHALL include registration link

#### Scenario: Invalid API path
- **WHEN** query is made with non-existent path
- **THEN** client SHALL return error from API
- **AND** error SHALL be wrapped with helpful message

#### Scenario: Rate limit exceeded
- **WHEN** more than 5000 requests made in one hour
- **THEN** API SHALL return 429 error
- **AND** client SHALL provide retry guidance

### Requirement: Data Extraction Tool
The system SHALL provide an MCP tool for extracting EIA energy data with flexible query parameters.

#### Scenario: WTI spot price query
- **WHEN** tool is called with path="petroleum/pri/spt" and facets for RWTC
- **THEN** tool SHALL return WTI spot prices
- **AND** prices SHALL be formatted as markdown table
- **AND** table SHALL include period and price columns

#### Scenario: Henry Hub natural gas query
- **WHEN** tool is called with path="natural-gas/pri/sum"
- **THEN** tool SHALL return natural gas price data
- **AND** data SHALL be formatted with appropriate units ($/MMBtu)

#### Scenario: Date range query
- **WHEN** tool is called with start and end dates
- **THEN** tool SHALL return data only within specified range
- **AND** dates SHALL be formatted for readability

#### Scenario: Frequency specification
- **WHEN** tool is called with frequency parameter
- **THEN** tool SHALL request data at specified interval
- **AND** valid frequencies SHALL be: daily, weekly, monthly, annual

#### Scenario: Empty result set
- **WHEN** query returns no data
- **THEN** tool SHALL return message indicating no data found
- **AND** message SHALL suggest adjusting query parameters

### Requirement: Response Formatting
The system SHALL format EIA data responses as readable markdown tables with metadata.

#### Scenario: Table with price data
- **WHEN** price data is returned
- **THEN** response SHALL include markdown table
- **AND** table SHALL have period and price columns
- **AND** prices SHALL be formatted with currency symbol and units

#### Scenario: Metadata inclusion
- **WHEN** data is returned
- **THEN** response SHALL include source attribution
- **AND** response SHALL include series ID
- **AND** response SHALL include frequency
- **AND** response SHALL include record count

#### Scenario: Large result sets
- **WHEN** query returns >100 records
- **THEN** response SHALL show summary statistics
- **AND** full table SHALL be included
- **AND** latest values SHALL be highlighted

### Requirement: Series ID Support
The system SHALL support EIA series IDs for filtering specific data series.

#### Scenario: Common series documentation
- **WHEN** tool documentation is accessed
- **THEN** docs SHALL list common series IDs
- **AND** docs SHALL include: WTI (RWTC), Brent (RBRTE), production series

#### Scenario: Facets JSON parsing
- **WHEN** facets parameter includes JSON string
- **THEN** tool SHALL parse JSON correctly
- **AND** tool SHALL pass facets to API
- **AND** invalid JSON SHALL return clear error

#### Scenario: Multiple series in facets
- **WHEN** facets includes array of series IDs
- **THEN** tool SHALL request all specified series
- **AND** response SHALL include data for each series

### Requirement: Parameter Validation
The system SHALL validate tool parameters before making API requests.

#### Scenario: Required path parameter
- **WHEN** tool is called without path parameter
- **THEN** tool SHALL return error
- **AND** error SHALL list common paths

#### Scenario: Date format validation
- **WHEN** start or end date is provided
- **THEN** tool SHALL validate date format (YYYY-MM-DD or YYYY-MM)
- **AND** invalid format SHALL return clear error with example

#### Scenario: Frequency validation
- **WHEN** frequency parameter is provided
- **THEN** tool SHALL validate against allowed values
- **AND** invalid frequency SHALL return error with valid options

#### Scenario: Limit validation
- **WHEN** limit parameter exceeds 5000
- **THEN** tool SHALL cap limit at 5000
- **AND** tool SHALL log warning about limit

### Requirement: Error Handling
The system SHALL provide user-friendly error messages for all failure scenarios.

#### Scenario: Network timeout
- **WHEN** API request times out
- **THEN** tool SHALL return timeout error
- **AND** error SHALL suggest checking network connection

#### Scenario: Invalid series ID
- **WHEN** facets includes non-existent series ID
- **THEN** API SHALL return error
- **AND** tool SHALL suggest checking series browser

#### Scenario: Malformed facets JSON
- **WHEN** facets parameter is invalid JSON
- **THEN** tool SHALL return JSON parsing error
- **AND** error SHALL show example facets format

#### Scenario: API authentication error
- **WHEN** API key is invalid or expired
- **THEN** tool SHALL return authentication error
- **AND** error SHALL include re-registration link

### Requirement: Tool Registration
The system SHALL register the EIA data extractor tool with the MCP server.

#### Scenario: Tool appears in list
- **WHEN** server starts
- **THEN** eia_data_extractor SHALL appear in tool list
- **AND** tool description SHALL be clear
- **AND** parameters SHALL be documented

#### Scenario: Tool invocation logging
- **WHEN** tool is called
- **THEN** server SHALL log tool invocation
- **AND** log SHALL include parameters (excluding API key)
- **AND** log SHALL include authenticated user if present

### Requirement: Common Query Patterns
The system SHALL document and support common energy trading query patterns.

#### Scenario: WTI spot price pattern
- **WHEN** docs are accessed
- **THEN** docs SHALL show WTI query example
- **AND** example SHALL include path, facets, and frequency

#### Scenario: Brent price pattern
- **WHEN** docs are accessed
- **THEN** docs SHALL show Brent query example
- **AND** example SHALL work with current API

#### Scenario: Production data pattern
- **WHEN** docs are accessed
- **THEN** docs SHALL show U.S. production query
- **AND** example SHALL include appropriate series ID

#### Scenario: STEO forecast pattern
- **WHEN** docs are accessed
- **THEN** docs SHALL show forecast query example
- **AND** example SHALL retrieve Short-Term Energy Outlook data

### Requirement: Integration with Authentication
The system SHALL optionally log authenticated user information for EIA queries.

#### Scenario: Authenticated query
- **WHEN** tool is called by authenticated user
- **THEN** server SHALL log user email
- **AND** query SHALL execute normally

#### Scenario: Unauthenticated query
- **WHEN** tool is called without authentication
- **THEN** query SHALL execute normally
- **AND** no user info SHALL be logged

### Requirement: Rate Limit Awareness
The system SHALL track API usage and warn when approaching rate limits.

#### Scenario: Normal usage tracking
- **WHEN** API requests are made
- **THEN** client SHALL increment request counter
- **AND** counter SHALL reset hourly

#### Scenario: Approaching limit
- **WHEN** request count exceeds 4000 in current hour
- **THEN** client SHALL log warning
- **AND** warning SHALL indicate requests remaining

#### Scenario: Limit reached
- **WHEN** API returns 429 rate limit error
- **THEN** client SHALL return clear error
- **AND** error SHALL indicate wait time

