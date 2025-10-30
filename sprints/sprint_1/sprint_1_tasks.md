# Sprint 1 Tasks

## Goals
Set up project infrastructure and basic MCP server following OpenSpec change `add-mcp-server`.

## Tasks

### 1. Project Setup
- [x] 1.1 Create sprint-1 branch
- [x] 1.2 Create project directory structure (tools/, utils/, examples/, tests/)
- [x] 1.3 Create .env.example file with required variables
- [x] 1.4 Update pyproject.toml with North SDK dependency
- [ ] 1.5 Install dependencies with uv (manual step)

### 2. Core Server Implementation
- [x] 2.1 Create server.py with NorthMCPServer initialization
- [x] 2.2 Implement CLI argument parsing (--transport, --port, --debug)
- [x] 2.3 Add server secret authentication
- [x] 2.4 Configure streamable HTTP transport
- [x] 2.5 Implement graceful shutdown handling
- [x] 2.6 Add environment variable loading

### 3. Authentication System
- [x] 3.1 Create utils/auth.py module
- [x] 3.2 Implement get_authenticated_user() helper
- [x] 3.3 Add user context retrieval (email, OAuth tokens)
- [x] 3.4 Add authentication error handling
- [x] 3.5 Document authentication patterns

### 4. Tool Registration System
- [x] 4.1 Create tools/__init__.py with tool discovery
- [x] 4.2 Implement dynamic tool registration
- [x] 4.3 Create hello_world example tool for testing
- [ ] 4.4 Test tool invocation (manual testing required)

### 5. Logging Infrastructure
- [x] 5.1 Create utils/logging.py module
- [x] 5.2 Configure structured logging
- [x] 5.3 Add debug mode support
- [x] 5.4 Implement request/response logging

### 6. Testing Utilities
- [x] 6.1 Create examples/create_bearer_token.py
- [x] 6.2 Implement JWT generation for user_id_token
- [x] 6.3 Add bearer token encoding/formatting
- [x] 6.4 Document token generation process

### 7. Documentation
- [x] 7.1 Update README with server startup instructions
- [x] 7.2 Add authentication configuration guide
- [x] 7.3 Document MCP Inspector setup
- [x] 7.4 Create .env.example with all variables

### 8. Testing & Validation
- [ ] 8.1 Test server startup with streamable HTTP
- [ ] 8.2 Test authentication with bearer token
- [ ] 8.3 Verify MCP Inspector connectivity
- [ ] 8.4 Test debug mode logging
- [ ] 8.5 Test graceful shutdown
- [ ] 8.6 Test hello_world tool invocation

## Progress Notes
- Sprint started: [Date]
- MCP server foundation for energy trading demo

