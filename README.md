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
- **Analysis Tools**: Statistical analysis and simulations
  - Monte Carlo price simulations (geometric Brownian motion)
  - Statistical calculations (mean, std dev, confidence intervals)
  - Risk assessment and scenario planning
- **Trading Vernacular**: Domain-specific terminology explanations
  - 18+ essential trading terms (contango, crack spread, basis, etc.)
  - Benchmark explanations (WTI, Brent, Henry Hub)
  - Trading context and practical usage

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

---

### Analysis Tools

Statistical analysis and simulation tools for market forecasting and risk assessment.

#### Monte Carlo Simulation

Run Monte Carlo price simulations using geometric Brownian motion:

**Tool**: `monte_carlo_simulation`

**Parameters**:
- `current_price` - Starting price (e.g., 71.50)
- `volatility` - Annual volatility as decimal (e.g., 0.25 for 25%)
- `days` - Number of days to simulate (default: 30)
- `simulations` - Number of simulation paths (default: 1000)
- `drift` - Expected daily return as decimal (default: 0.0)

**Example Request**:
```json
{
  "current_price": 71.50,
  "volatility": 0.25,
  "days": 30,
  "simulations": 1000
}
```

**Use Cases**:
- Risk assessment for trading positions
- Scenario planning for hedging strategies
- Confidence interval estimation
- Value-at-Risk (VaR) calculations

**Example Output**:
```
## Monte Carlo Price Simulation

**Starting Price**: $71.50
**Volatility**: 25.0% annual
**Time Horizon**: 30 days
**Simulations**: 1,000

### Price Distribution (Day 30)
| Statistic | Price |
|-----------|-------|
| Mean | $71.89 |
| Median | $71.45 |
| Std Dev | $5.24 |

### Confidence Intervals
| Confidence | Lower Bound | Upper Bound | Range |
|------------|-------------|-------------|-------|
| 95% | $63.12 | $82.55 | $19.43 |
| 68% | $67.23 | $76.89 | $9.66 |

### Interpretation
- **Upside Potential (95% CI)**: +15.5%
- **Downside Risk (95% CI)**: -11.7%
- **Expected Change**: +0.5%
```

#### Statistical Calculations

Calculate statistics for a dataset:

**Tool**: `calculate_statistics`

**Parameters**:
- `values` - Comma-separated numbers (e.g., "71.5,70.2,72.1")
- `label` - Label for the dataset (e.g., "WTI Weekly Prices")

**Example Request**:
```json
{
  "values": "71.5,70.2,72.1,69.8,71.0",
  "label": "WTI Weekly Prices"
}
```

**Returns**:
- Mean, median, standard deviation
- Min, max, range
- Coefficient of variation
- Volatility assessment

---

### Trading Vernacular

Domain-specific terminology explanations for energy trading.

#### Explain Term

Get detailed explanations of trading terms:

**Tool**: `explain_trading_term`

**Parameters**:
- `term` - Trading term to explain (e.g., "contango", "wti", "crack spread")

**Example Request**:
```json
{
  "term": "contango"
}
```

**Example Output**:
```
## Contango

**Term**: `contango`

### Definition
Market condition where future prices are higher than spot prices.

### Trading Context
Trading: Indicates excess supply or storage costs. Traders can profit by buying 
spot, selling futures, and storing.
```

**Available Terms**:
- Benchmarks: WTI, Brent, Henry Hub, Cushing, NYMEX
- Concepts: Contango, Backwardation, Crack Spread, Basis, Arb, Strip, Prompt
- Measurements: MCF, MMBtu
- Organizations: EIA, OPEC
- Positions: Long, Short

#### List Terms

List all available trading terms:

**Tool**: `list_trading_terms`

**Parameters**:
- `category` - Filter by category: "all", "benchmarks", "concepts", "measurements"

**Example Request**:
```json
{
  "category": "benchmarks"
}
```

---

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

