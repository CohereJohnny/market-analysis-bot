# Project Context

## Purpose
Market Analysis Bot is a **demonstration project** showcasing the **Cohere North agentic foundry platform**. This is an agentic AI assistant designed for energy traders during the market analysis phase. The bot helps traders:
- Analyze real-time commodity market data (WTI, Brent crude, Natural Gas)
- Access U.S. Energy Information Administration (EIA) data via custom MCP tool
- Parse and summarize OPEC Monthly Oil Market Reports (MOMR)
- Run data simulations and visualizations using Python
- Understand trading vernacular and domain-specific terminology
- Provide actionable insights for hedging and trading positions

**Demo Focus**: This is a proof-of-concept to demonstrate North's capabilities for multi-turn agentic conversations with custom tools, authentication, and real-time data integration. No production deployment is planned.

## Tech Stack
- **Platform**: Cohere North MCP (Model Context Protocol)
- **Language**: Python 3.11+
- **MCP SDK**: [North MCP Python SDK](https://github.com/cohere-ai/north-mcp-python-sdk)
- **Transport**: Streamable HTTP (North's custom extension)
- **Data Analysis**: Python (NumPy, Pandas, Matplotlib)
- **Package Manager**: uv (for dependency management)
- **Custom MCP Tools**: 
  - EIA Data Extractor (U.S. energy data)
  - OPEC Report Extractor (global oil market reports)
  - Web search for real-time prices
  - Python code execution for analysis

## Project Conventions

### Code Style
- **File Naming**: Use snake_case for Python files (e.g., `eia_data_extractor.py`, `market_analysis_server.py`)
- **Python Style**: Follow PEP 8 conventions
- **Type Hints**: Use Python type hints for function signatures
- **Formatting**: Use `uv format` for consistent code formatting
- **Docstrings**: Use docstrings for functions and classes
- **Comments**: Minimal inline comments; prefer self-documenting code
- **Error Handling**: Always implement error handling with proper logging

### Architecture Patterns
- **MCP Server Architecture**: Build as standalone MCP server using North SDK
- **Tool-Based**: Implement functionality as MCP tools (functions callable by North)
- **Stateless**: Keep tools stateless; use context for user authentication
- **Simplicity First**: Default to <100 lines of new code per module
- **Single Responsibility**: Each MCP tool should have a single, clear purpose
- **No Premature Abstraction**: Avoid complex frameworks without clear justification
- **File Organization**: 
  - `/tools/` - MCP tool implementations (e.g., `eia_data_extractor.py`)
  - `/server.py` - Main MCP server setup
  - `/examples/` - Demo conversation examples
  - `/tests/` - Unit tests for tools

### Testing Strategy
- **Local Testing**: Use MCP Inspector (`npx @modelcontextprotocol/inspector`) for testing tools
- **Unit Tests**: Use pytest for testing individual tool functions
- **Integration Tests**: Test full conversation flows using demo scripts
- **Authentication Testing**: Use `create_bearer_token.py` for local auth testing
- **Debug Mode**: Enable debug logging for troubleshooting authentication issues
- Manual testing required for key trader conversation flows before demo

### Git Workflow
- **Branching**: Sprint-based branches (e.g., `sprint-1`, `sprint-2`)
- **Commits**: Conventional commits format:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `refactor:` for code refactoring
  - `docs:` for documentation
  - `test:` for tests
- **Pull Requests**: Create PR at sprint completion, verify checks pass
- **Tagging**: Tag merge commits as `sprint-x` after merging
- **Archive**: Move sprint directories to `sprints/archive/` after completion

## North MCP Platform Details

### Authentication & Security
- **Server Secret**: Protects all requests to the MCP server
  - Set via `NorthMCPServer(server_secret="your-secret")`
  - Required for North to communicate with server
- **User Identity**: Access authenticated user information
  - Use `get_authenticated_user()` to retrieve user email and context
  - User ID token validated via JWT
- **OAuth Tokens**: Access third-party services on behalf of users
  - Available via `user.connector_access_tokens` dict
  - Supports connectors like Google, Slack, etc.
- **Debug Mode**: Enable detailed auth logging for troubleshooting
  - Set via environment variable: `export DEBUG=true`
  - Or constructor: `NorthMCPServer(debug=True)`

### Transport Layer
- **Streamable HTTP**: North's custom MCP transport (required)
  - Replaces SSE transport from standard MCP
  - Supports bearer token authentication
  - Base URL pattern: `http://localhost:PORT/mcp`
- **Bearer Token Format**: Base64-encoded JSON with:
  - `server_secret`: Server authentication
  - `user_id_token`: JWT for user identity
  - `connector_access_tokens`: OAuth tokens dict

### Development Workflow
- **Local Testing**: Use MCP Inspector with streamable-http transport
- **Authentication Testing**: Generate tokens with `create_bearer_token.py`
- **Server Startup**: `uv run server.py --transport streamable-http`
- **Stdio Mode**: For testing without authentication

## Domain Context

### Energy Trading Terminology
- **ORB**: OPEC Reference Basket - weighted average price of OPEC crude oils
- **mb/d**: Million barrels per day - standard unit for oil production/demand
- **CLZ25**: December 2025 WTI crude oil futures contract on NYMEX
- **NGZ25**: December 2025 Natural Gas futures contract on NYMEX
- **MOMR**: Monthly Oil Market Report published by OPEC
- **Secondary Sources**: Independent production estimates (vs OPEC direct communications)
- **Henry Hub**: Natural gas pricing point and benchmark

### Market Analysis Workflow
1. Review latest OPEC MOMR for demand/supply forecasts
2. Compare current vs previous month's data for trend analysis
3. Check spot prices and futures contracts
4. Run simulations for price ranges and volatility
5. Consider cross-commodity impacts (oil-to-gas substitution)
6. Make hedging and position decisions

### Data Sources
- OPEC Monthly Oil Market Reports (primary source for supply/demand)
- Real-time price feeds (Bloomberg, Reuters, Trading Economics)
- Futures market data (NYMEX codes: CL for WTI, NG for Natural Gas)
- Analyst opinions from major financial institutions

## Important Constraints
- **Real-time Data**: Must access current market prices, not stale data
- **Accuracy**: Trading decisions rely on accurate data interpretation
- **Vernacular**: Must understand energy trading terminology without explicit definitions
- **Performance**: Responses should be fast enough for active trading workflows
- **Transparency**: AI should clearly explain reasoning and data sources
- **Regulatory**: No financial advice; present data and analysis objectively
- **Data Privacy**: Handle proprietary trading strategies confidentially

## External Dependencies
- **EIA Open Data API v2**: U.S. Energy Information Administration API for petroleum/natural gas data
  - Requires free API key from https://signups.eia.gov/api/signup/
  - Rate limit: 5,000 requests/hour
  - Primary endpoints: petroleum prices, natural gas prices, production data, STEO forecasts
- **OPEC Data Source**: Custom tool for accessing Monthly Oil Market Reports (MOMR)
  - Implementation: Web scraping or PDF parsing from https://www.opec.org/
- **Web Search**: For real-time commodity prices and analyst opinions
- **Python Packages**:
  - `requests` - HTTP client for API calls
  - `pandas` - Data manipulation and table formatting
  - `numpy` - Numerical computations and simulations
  - `matplotlib` - Data visualization (optional for advanced demos)
- **North MCP SDK**: `north-mcp-python-sdk` from Cohere
  - Install: `uv pip install git+ssh://git@github.com/cohere-ai/north-mcp-python-sdk.git`
  - Provides authentication, user context, and OAuth token access
