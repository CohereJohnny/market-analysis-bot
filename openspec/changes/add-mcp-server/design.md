# Design Document: MCP Server Implementation

## Context
This document outlines technical decisions for implementing the MCP (Model Context Protocol) server using Cohere's North platform. The server is the foundation for a demo showcasing agentic AI capabilities for energy trading market analysis. It must support custom tools, authentication, and multi-turn conversations.

**Background**: 
- North MCP extends the standard MCP protocol with authentication and OAuth support
- Uses streamable HTTP transport (not SSE)
- Requires bearer token authentication for security
- Demo environment (not production)

**Constraints**:
- Must work with MCP Inspector for local testing
- Python 3.11+ required
- Authentication required for North compatibility
- Simplicity prioritized over scalability (demo scope)

## Goals / Non-Goals

### Goals
- Create functional MCP server with North SDK
- Support authentication (server secret + user identity)
- Enable dynamic tool registration
- Provide debug mode for troubleshooting
- Support both development (MCP Inspector) and North integration
- Simple, readable codebase (<100 lines per module)

### Non-Goals
- Production-grade scalability or performance
- Database persistence (stateless tools)
- Complex middleware or plugin systems
- Multiple transport protocols (streamable HTTP only)
- Frontend UI (server-only demo)

## Decisions

### Decision 1: Server Architecture Pattern
**Choice**: Single-file server entry point (server.py) with modular tool system

**Rationale**:
- Follows North SDK examples pattern
- Easy to understand and demo
- Tools in separate modules for organization
- Minimal abstraction overhead

**Alternatives Considered**:
- FastAPI-based approach: Rejected - North SDK handles HTTP layer
- Plugin framework: Rejected - over-engineering for demo scope

**Implementation**:
```python
# server.py
from north_mcp_python_sdk import NorthMCPServer
from tools import register_all_tools

mcp = NorthMCPServer(name="Market Analysis", port=5222, server_secret=SECRET)
register_all_tools(mcp)
mcp.start()
```

### Decision 2: Authentication Strategy
**Choice**: Server secret + optional user identity (get_authenticated_user)

**Rationale**:
- Server secret protects against unauthorized access
- User identity enables personalization (future)
- OAuth tokens available for third-party APIs (future)
- Matches North SDK patterns

**Security Model**:
- Server secret validates North → Server communication
- User ID token (JWT) provides user identity
- Bearer token format: Base64(JSON{server_secret, user_id_token, connector_tokens})

**Implementation**:
```python
# In tools
from north_mcp_python_sdk import get_authenticated_user

def my_tool():
    user = get_authenticated_user()
    print(f"Tool called by: {user.email}")
```

### Decision 3: Tool Registration System
**Choice**: Decorator-based registration with automatic discovery

**Rationale**:
- Clean, Pythonic API
- Easy to add new tools
- Follows North SDK conventions
- Self-documenting code

**Pattern**:
```python
# tools/example.py
@mcp.tool()
def hello_world(name: str) -> str:
    """Say hello to someone"""
    return f"Hello, {name}!"
```

### Decision 4: Configuration Management
**Choice**: Environment variables + CLI arguments

**Rationale**:
- Standard practice for 12-factor apps
- Secrets stay out of code
- CLI args for development convenience
- python-dotenv for .env support

**Variables**:
- `SERVER_SECRET` - Required for authentication
- `EIA_API_KEY` - For EIA data tool
- `DEBUG` - Enable debug logging
- CLI: `--transport`, `--port`, `--debug` override env vars

### Decision 5: Logging Strategy
**Choice**: Python logging module with structured debug mode

**Rationale**:
- Standard library (no deps)
- Debug mode for North auth troubleshooting
- Structured logs for request tracing

**Levels**:
- DEBUG: Auth details, token parsing, request/response
- INFO: Server start, tool invocations
- ERROR: Auth failures, API errors

## Risks / Trade-offs

### Risk 1: North SDK API Changes
**Mitigation**: Pin SDK version in pyproject.toml, document version used

### Risk 2: Authentication Complexity
**Mitigation**: Debug mode for detailed logging, clear error messages, create_bearer_token.py helper

### Risk 3: Tool State Management
**Trade-off**: Stateless tools simplify design but limit capabilities
**Mitigation**: Document state limitations, use external APIs for data persistence if needed

### Risk 4: MCP Inspector Compatibility
**Mitigation**: Test with both stdio (simple) and streamable-http (realistic) transports

## Migration Plan
N/A - This is initial implementation, no migration needed

## Testing Strategy

### Unit Tests
- Tool registration and discovery
- Authentication helpers
- Bearer token generation

### Integration Tests
- Server startup/shutdown
- MCP Inspector connectivity
- Tool invocation with auth
- Debug mode logging

### Manual Testing
- Start server with various CLI args
- Connect via MCP Inspector
- Test hello_world tool
- Verify auth logging in debug mode

## File Organization

```
market-analysis-bot/
├── server.py                    # Main entry point (50-80 lines)
├── tools/
│   ├── __init__.py             # Tool registration (30-50 lines)
│   └── hello_world.py          # Example tool (20-30 lines)
├── utils/
│   ├── auth.py                 # Auth helpers (40-60 lines)
│   └── logging.py              # Logging config (30-50 lines)
├── examples/
│   └── create_bearer_token.py  # Testing utility (50-70 lines)
└── .env.example                # Config template
```

## Open Questions
- ~~Should we support stdio transport?~~ **Decision**: Yes, for simple testing
- ~~How verbose should debug logging be?~~ **Decision**: Very verbose for auth, normal for tools
- ~~Need custom error types?~~ **Decision**: No, use standard exceptions with clear messages

## References
- [North MCP Python SDK](https://github.com/cohere-ai/north-mcp-python-sdk)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- Project conventions: `openspec/project.md`

