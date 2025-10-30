# North Agent Configuration Specification

## ADDED Requirements

### Requirement: Custom Agent Instructions
The system SHALL provide comprehensive custom instructions that define the agent's role, behavior, and capabilities for energy trading market analysis.

#### Scenario: Agent role definition
- **WHEN** the agent is deployed to North platform
- **THEN** the agent SHALL identify as an energy trading market analyst
- **AND** the agent SHALL specialize in oil and gas commodity analysis
- **AND** the agent SHALL communicate in a professional, data-driven style

#### Scenario: Core behavior adherence
- **WHEN** the agent receives a query
- **THEN** the agent SHALL follow defined behavior rules
- **AND** the agent SHALL cite sources for all data
- **AND** the agent SHALL format responses according to guidelines

### Requirement: Trading Terminology Handling
The system SHALL interpret and use energy trading terminology correctly without requiring user clarification.

#### Scenario: Vernacular interpretation
- **WHEN** user mentions "ORB"
- **THEN** the agent SHALL interpret as OPEC Reference Basket
- **AND** the agent SHALL use the term naturally in responses

#### Scenario: Futures contract codes
- **WHEN** user mentions "CLZ25"
- **THEN** the agent SHALL interpret as December 2025 WTI crude futures
- **AND** the agent SHALL provide relevant context about the contract

#### Scenario: Production units
- **WHEN** user mentions "mb/d"
- **THEN** the agent SHALL interpret as million barrels per day
- **AND** the agent SHALL use the unit correctly in analysis

### Requirement: Tool Selection Logic
The system SHALL select appropriate tools based on query content using conditional logic and priority ordering.

#### Scenario: EIA data query
- **WHEN** user asks about US petroleum prices or production
- **THEN** the agent SHALL use EIA data tool first
- **AND** the agent SHALL format results as tables when appropriate

#### Scenario: OPEC report query
- **WHEN** user asks about OPEC MOMR or global demand forecasts
- **THEN** the agent SHALL use OPEC report tool
- **AND** the agent SHALL cite the specific report edition

#### Scenario: Real-time price query
- **WHEN** user asks for "current" or "today's" prices
- **THEN** the agent SHALL use web search tool
- **AND** the agent SHALL provide spot price with timestamp

#### Scenario: Multi-tool analysis
- **WHEN** query requires comprehensive analysis
- **THEN** the agent SHALL chain multiple tools appropriately
- **AND** the agent SHALL synthesize results from all sources
- **AND** the agent SHALL note any data conflicts or discrepancies

### Requirement: Response Format Standards
The system SHALL structure responses with clear sections, data tables, citations, and actionable insights.

#### Scenario: Data-heavy response
- **WHEN** response includes numerical data
- **THEN** the agent SHALL format data as markdown tables
- **AND** the agent SHALL include summary interpretation
- **AND** the agent SHALL cite data source and date

#### Scenario: Analysis response
- **WHEN** response includes analysis
- **THEN** the agent SHALL use bullet points for key insights
- **AND** the agent SHALL provide evidence for conclusions
- **AND** the agent SHALL suggest relevant follow-up analyses

#### Scenario: Source attribution
- **WHEN** any data is presented
- **THEN** the agent SHALL cite the source explicitly
- **AND** the citation SHALL include publication date or data timestamp

### Requirement: Scope Boundaries
The system SHALL define clear boundaries for what the agent can and cannot do, with appropriate handling for out-of-scope queries.

#### Scenario: In-scope market analysis query
- **WHEN** user asks about commodity prices, forecasts, or market data
- **THEN** the agent SHALL provide comprehensive analysis
- **AND** the agent SHALL use appropriate tools

#### Scenario: Out-of-scope query
- **WHEN** user asks about non-trading topics
- **THEN** the agent SHALL politely redirect to market analysis scope
- **AND** the agent SHALL offer to help with trading-related questions

#### Scenario: Prediction request
- **WHEN** user asks for price predictions
- **THEN** the agent SHALL decline to predict
- **AND** the agent SHALL offer data-driven analysis with ranges instead
- **AND** the agent SHALL explain uncertainty and factors

### Requirement: Demo Guide Documentation
The system SHALL provide comprehensive demo guide with setup instructions, presentation flow, and troubleshooting.

#### Scenario: Demo setup instructions
- **WHEN** presenter accesses demo guide
- **THEN** guide SHALL include prerequisites and setup steps
- **AND** guide SHALL document agent deployment process
- **AND** guide SHALL provide MCP server connection configuration

#### Scenario: Presentation flow guidance
- **WHEN** presenter follows demo guide
- **THEN** guide SHALL provide progressive complexity structure
- **AND** guide SHALL include timing for each section
- **AND** guide SHALL suggest talking points for each feature

#### Scenario: Troubleshooting scenarios
- **WHEN** presenter encounters issues
- **THEN** guide SHALL provide common problem solutions
- **AND** guide SHALL include fallback strategies
- **AND** guide SHALL document error recovery procedures

### Requirement: Sample Prompts Collection
The system SHALL provide categorized sample prompts with expected responses for demonstration and testing.

#### Scenario: Basic level prompts
- **WHEN** presenter needs simple demonstration
- **THEN** sample prompts SHALL include basic data retrieval queries
- **AND** prompts SHALL demonstrate single tool usage
- **AND** expected responses SHALL be documented

#### Scenario: Intermediate level prompts
- **WHEN** presenter shows analysis capabilities
- **THEN** sample prompts SHALL include multi-turn conversations
- **AND** prompts SHALL demonstrate tool chaining
- **AND** prompts SHALL show data comparison and analysis

#### Scenario: Advanced level prompts
- **WHEN** presenter shows sophisticated features
- **THEN** sample prompts SHALL include simulation requests
- **AND** prompts SHALL demonstrate cross-commodity analysis
- **AND** prompts SHALL show complex reasoning scenarios

#### Scenario: Edge case prompts
- **WHEN** testing agent robustness
- **THEN** sample prompts SHALL include ambiguous queries
- **AND** prompts SHALL test error handling
- **AND** prompts SHALL verify scope boundary enforcement

### Requirement: Agent Configuration Documentation
The system SHALL document North platform agent configuration including tool connections and settings.

#### Scenario: Agent deployment configuration
- **WHEN** deploying agent to North
- **THEN** documentation SHALL specify agent name and description
- **AND** documentation SHALL include MCP server connection URL
- **AND** documentation SHALL document authentication requirements

#### Scenario: Tool connection setup
- **WHEN** connecting MCP tools to agent
- **THEN** documentation SHALL list all required tools
- **AND** documentation SHALL provide connection parameters
- **AND** documentation SHALL include verification steps

#### Scenario: Environment configuration
- **WHEN** configuring agent environment
- **THEN** documentation SHALL list required environment variables
- **AND** documentation SHALL specify model selection recommendations
- **AND** documentation SHALL document response settings (temperature, tokens)

### Requirement: Quality Assurance Procedures
The system SHALL define validation procedures for agent instructions, prompts, and demo materials.

#### Scenario: Instruction validation
- **WHEN** custom instructions are created
- **THEN** instructions SHALL be reviewed against North best practices
- **AND** all behavior rules SHALL be testable
- **AND** conditional logic SHALL be unambiguous

#### Scenario: Prompt testing
- **WHEN** sample prompts are finalized
- **THEN** each prompt SHALL be tested with deployed agent
- **AND** responses SHALL match expected behavior
- **AND** edge cases SHALL be verified

#### Scenario: Demo rehearsal
- **WHEN** preparing for demo
- **THEN** full demo flow SHALL be rehearsed 3+ times
- **AND** timing SHALL be validated
- **AND** failure points SHALL be identified and mitigated

