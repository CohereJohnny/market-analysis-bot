# Market Analysis Bot - Cohere North MCP Demo

A demonstration project showcasing the **Cohere North agentic foundry platform** through an energy trading market analysis assistant. This MCP (Model Context Protocol) server provides AI-powered tools for analyzing commodity markets, accessing real-time energy data, and supporting trader decision-making workflows.

## Purpose

This demo showcases North's capabilities for:
- **Multi-turn agentic conversations** with domain expertise
- **Custom MCP tools** for specialized data access (EIA, OPEC)
- **Authentication & user context** via North's security features
- **Real-time data integration** from external APIs
- **Complex analysis** with Python-based simulations

**Note**: This is a proof-of-concept demo, not a production application.

## Features

### Custom MCP Tools
- **EIA Data Extractor**: Access U.S. Energy Information Administration data
  - WTI and Brent crude oil prices
  - Natural gas (Henry Hub) prices
  - Production volumes and forecasts
  - Short-Term Energy Outlook (STEO) data
- **OPEC Report Analyzer**: Parse Monthly Oil Market Reports (MOMR)
- **Market Analysis**: Run simulations and trend analysis
- **Trading Vernacular**: Understand domain-specific terminology

### Domain Knowledge
- Energy trading terminology (ORB, mb/d, CLZ25, NGZ25, etc.)
- Commodity price analysis workflows
- Cross-commodity impact analysis (oil-to-gas substitution)

## Tech Stack

- **Platform**: [Cohere North MCP](https://github.com/cohere-ai/north-mcp-python-sdk)
- **Language**: Python 3.11+
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Key Dependencies**:
  - `north-mcp-python-sdk` - MCP server framework with North extensions
  - `requests` - HTTP client for API calls
  - `pandas` - Data manipulation
  - `numpy` - Numerical analysis

## Prerequisites

1. **Python 3.11+** installed
2. **uv** package manager (v0.8.13+):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **EIA API Key** (free):
   - Register at https://signups.eia.gov/api/signup/
   - Save key as environment variable: `export EIA_API_KEY="your-key-here"`
4. **Node.js** (for MCP Inspector testing)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd market-analysis-bot
   ```

2. Install North MCP SDK:
   ```bash
   uv pip install git+https://github.com/cohere-ai/north-mcp-python-sdk.git
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Configure environment:
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env and set required variables:
   # - SERVER_SECRET (required for streamable-http)
   # - EIA_API_KEY (for EIA data tool)
   # - DEBUG (optional, set to true for verbose logging)
   ```

## Usage

### Running the MCP Server

#### Quick Start

Start the server with streamable HTTP transport (required for North):

```bash
# Basic startup
uv run server.py

# With custom port
uv run server.py --port 8080

# With debug mode for detailed logging
uv run server.py --debug

# With stdio transport (for simple testing)
uv run server.py --transport stdio
```

The server will start on `http://localhost:5222/mcp` by default.

#### Command Line Options

```
--transport     Transport protocol: streamable-http or stdio (default: streamable-http)
--port          Server port for HTTP transport (default: 5222)
--debug         Enable debug mode for verbose logging
--server-secret Server secret for authentication (or use SERVER_SECRET env var)
```

#### Server Startup Example

```bash
$ uv run server.py --debug
============================================================
Market Analysis Bot - MCP Server
============================================================
Transport: streamable-http
Port: 5222
Debug Mode: True
============================================================
INFO - MCP server instance created successfully
INFO - ✓ hello_world tool registered
INFO - Tool registration complete: 1 tool(s) registered
INFO - Starting MCP server...
INFO - Server available at: http://localhost:5222/mcp
INFO - Waiting for connections from North platform...
```

### Local Testing with MCP Inspector

For local testing without North:

1. **Generate a bearer token** for authentication:
   ```bash
   # Basic token (server secret only)
   uv run examples/create_bearer_token.py --server-secret demo-secret-key
   
   # With user identity
   uv run examples/create_bearer_token.py --server-secret demo-secret-key --email trader@company.com
   
   # With connector tokens
   uv run examples/create_bearer_token.py --server-secret demo-secret-key --email trader@company.com --with-connectors
   
   # Save to file
   uv run examples/create_bearer_token.py --output-file bearer_token.txt
   ```

2. **Start your MCP server**:
   ```bash
   # In one terminal
   SERVER_SECRET=demo-secret-key uv run server.py --debug
   ```

3. **Start the MCP Inspector**:
   ```bash
   # In another terminal
   npx @modelcontextprotocol/inspector
   ```

4. **Configure Inspector connection**:
   - **Transport Type**: Streamable HTTP
   - **URL**: `http://localhost:5222/mcp`
   - **Authentication → Bearer token**: [paste generated token]
   - Click **"Connect"**

5. **Test tools**:
   - Select **"Tools"** tab at the top
   - Click **"List Tools"** to see available tools
   - Select a tool (e.g., `hello_world`)
   - Provide parameters (e.g., `name: "Trader"`)
   - Click **"Run"**
   - View the response in the output panel

#### Expected Output for hello_world Tool

```
Hello, Trader! Welcome to the Market Analysis Bot.

Authenticated as: trader@company.com
Available connectors: google, slack

Server Status: ✓ Running
This is a demonstration MCP server for energy trading market analysis.
```

### Using the EIA Data Tool

The `eia_data_extractor` tool provides access to U.S. energy data including petroleum prices, natural gas prices, and production volumes.

#### Quick Start

1. **Get an EIA API key** (free):
   ```bash
   # Visit https://signups.eia.gov/api/signup/
   # Add to .env file
   echo "EIA_API_KEY=your-key-here" >> .env
   ```

2. **Query WTI spot prices** (via MCP Inspector):
   ```json
   {
     "path": "petroleum/pri/spt",
     "facets": "{\"series\":[\"RWTC\"]}",
     "frequency": "weekly",
     "start": "2025-01-01",
     "limit": 10
   }
   ```

#### Common Query Examples

**WTI Crude Oil Spot Prices** (Weekly):
```json
{
  "path": "petroleum/pri/spt",
  "facets": "{\"series\":[\"RWTC\"]}",
  "frequency": "weekly",
  "start": "2025-01-01",
  "end": "2025-10-30"
}
```

**Brent Crude Oil Spot Prices**:
```json
{
  "path": "petroleum/pri/spt",
  "facets": "{\"series\":[\"RBRTE\"]}",
  "frequency": "weekly",
  "limit": 20
}
```

**Henry Hub Natural Gas Prices** (Monthly):
```json
{
  "path": "natural-gas/pri/sum",
  "frequency": "monthly",
  "start": "2025-01",
  "limit": 12
}
```

**U.S. Crude Oil Production**:
```json
{
  "path": "petroleum/prod/sum",
  "facets": "{\"series\":[\"MCRFPUS1\"]}",
  "frequency": "monthly",
  "limit": 12
}
```

**STEO WTI Price Forecast**:
```json
{
  "path": "steo",
  "facets": "{\"series\":[\"WTIPUUS\"]}",
  "frequency": "monthly"
}
```

#### Common Series IDs

| Trading Term | Series ID | Path | Description |
|--------------|-----------|------|-------------|
| WTI Spot | RWTC | petroleum/pri/spt | WTI Cushing spot price ($/barrel) |
| Brent Spot | RBRTE | petroleum/pri/spt | Brent Europe spot price ($/barrel) |
| U.S. Production | MCRFPUS1 | petroleum/prod/sum | U.S. crude production (thousand bbl/day) |
| STEO WTI Forecast | WTIPUUS | steo | Short-term WTI price forecast |

Browse all series: https://www.eia.gov/opendata/browser/

## Project Structure

```
market-analysis-bot/
├── server.py                 # Main MCP server
├── tools/                    # MCP tool implementations
│   ├── eia_data_extractor.py
│   ├── opec_report_extractor.py
│   └── analysis_tools.py
├── examples/                 # Demo scripts and examples
│   ├── demo_conversation.md
│   ├── create_bearer_token.py
│   └── sample_queries.py
├── tests/                    # Unit tests
├── sprints/                  # Sprint planning and logs
│   ├── sprintplan.md
│   ├── tech_debt.md
│   ├── backlog.md
│   └── bug_swatting.md
├── openspec/                 # Project specifications
│   ├── project.md
│   └── AGENTS.md
├── specs/                    # Domain specifications
│   ├── demo-context.md
│   └── eia-data.md
├── pyproject.toml           # Python dependencies
└── README.md
```

## Development

### Sprint-Based Workflow

This project uses a sprint-based development approach. See `sprints/sprintplan.md` for the overall plan.

### Code Style

- Follow PEP 8 conventions
- Use type hints for function signatures
- Format code with `uv format`
- Add docstrings to functions and classes

### Testing

Run tests with pytest:
```bash
uv run pytest
```

### Contributing

1. Create a sprint branch: `git checkout -b sprint-X`
2. Implement tasks from `sprints/sprint_X/sprint_X_tasks.md`
3. Commit frequently with conventional commits:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `refactor:` for code improvements
4. Create PR at sprint completion

## Authentication

North MCP supports several authentication strategies:

### Server Secret Only
```python
mcp = NorthMCPServer(name="Demo", port=5222, server_secret="secret")
```

### With User Identity
```python
user = get_authenticated_user()
print(user.email)
```

### With OAuth Tokens
```python
user = get_authenticated_user()
print(user.connector_access_tokens)
```

### Debug Mode
Enable detailed authentication logging:
```bash
export DEBUG=true
# or
NorthMCPServer(debug=True)
```

## Resources

- [North MCP Python SDK](https://github.com/cohere-ai/north-mcp-python-sdk)
- [EIA Open Data API](https://www.eia.gov/opendata/documentation.php)
- [OPEC Monthly Reports](https://www.opec.org/opec_web/en/publications/338.htm)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)

## License

MIT

## Contact

For questions about this demo, please refer to the project documentation in `openspec/` and `specs/`.

