# Implementation Tasks: Add MCP Server

## 1. Project Setup
- [ ] 1.1 Install North MCP Python SDK via uv
- [ ] 1.2 Add python-dotenv to dependencies
- [ ] 1.3 Create .env.example file with required variables
- [ ] 1.4 Update pyproject.toml with North SDK dependency
- [ ] 1.5 Create project directory structure (tools/, utils/, examples/)

## 2. Core Server Implementation
- [ ] 2.1 Create server.py with NorthMCPServer initialization
- [ ] 2.2 Implement CLI argument parsing (--transport, --port, --debug)
- [ ] 2.3 Add server secret authentication
- [ ] 2.4 Configure streamable HTTP transport
- [ ] 2.5 Implement graceful shutdown handling
- [ ] 2.6 Add environment variable loading

## 3. Authentication System
- [ ] 3.1 Create utils/auth.py module
- [ ] 3.2 Implement get_authenticated_user() helper
- [ ] 3.3 Add user context retrieval (email, OAuth tokens)
- [ ] 3.4 Add authentication error handling
- [ ] 3.5 Document authentication patterns

## 4. Tool Registration System
- [ ] 4.1 Create tools/__init__.py with tool discovery
- [ ] 4.2 Implement dynamic tool registration
- [ ] 4.3 Add tool decorator pattern (if needed)
- [ ] 4.4 Create hello_world example tool for testing

## 5. Logging Infrastructure
- [ ] 5.1 Create utils/logging.py module
- [ ] 5.2 Configure structured logging
- [ ] 5.3 Add debug mode support
- [ ] 5.4 Implement request/response logging
- [ ] 5.5 Add authentication event logging

## 6. Testing Utilities
- [ ] 6.1 Create examples/create_bearer_token.py
- [ ] 6.2 Implement JWT generation for user_id_token
- [ ] 6.3 Add bearer token encoding/formatting
- [ ] 6.4 Document token generation process

## 7. Documentation
- [ ] 7.1 Update README with server startup instructions
- [ ] 7.2 Add authentication configuration guide
- [ ] 7.3 Document MCP Inspector setup
- [ ] 7.4 Add troubleshooting section
- [ ] 7.5 Create example .env file

## 8. Testing & Validation
- [ ] 8.1 Test server startup with streamable HTTP
- [ ] 8.2 Test authentication with bearer token
- [ ] 8.3 Verify MCP Inspector connectivity
- [ ] 8.4 Test debug mode logging
- [ ] 8.5 Test graceful shutdown
- [ ] 8.6 Test hello_world tool invocation

## 9. Integration
- [ ] 9.1 Validate OpenSpec requirements
- [ ] 9.2 Run openspec validate --strict
- [ ] 9.3 Update sprint documentation
- [ ] 9.4 Commit implementation to sprint-1 branch

