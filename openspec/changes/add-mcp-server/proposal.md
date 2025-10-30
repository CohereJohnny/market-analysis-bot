# Change Proposal: Add MCP Server

## Why
This demo requires a functional Model Context Protocol (MCP) server built with Cohere's North platform to showcase agentic capabilities for energy trading market analysis. Without the MCP server, we cannot demonstrate North's features including custom tools, authentication, user context, and multi-turn conversations.

## What Changes
- Create base MCP server using North MCP Python SDK
- Implement authentication with server secret and user identity support
- Add transport layer configuration (streamable HTTP)
- Create server startup script with CLI arguments
- Implement basic health check and tool registration system
- Add debug mode for troubleshooting authentication
- Create helper utilities for bearer token generation (testing)
- Set up logging infrastructure
- Configure development and production modes

## Impact
- **Affected specs**: `mcp-server` (new capability)
- **Affected code**: 
  - `server.py` - Main MCP server entry point
  - `tools/__init__.py` - Tool registration system
  - `utils/auth.py` - Authentication helpers
  - `utils/logging.py` - Logging configuration
  - `examples/create_bearer_token.py` - Testing utility
- **Dependencies**: North MCP Python SDK, python-dotenv
- **Testing**: Requires MCP Inspector for local testing
- **Documentation**: README updates for server setup and usage

