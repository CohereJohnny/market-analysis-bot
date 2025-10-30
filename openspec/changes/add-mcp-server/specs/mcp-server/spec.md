# MCP Server Capability Specification

## ADDED Requirements

### Requirement: MCP Server Initialization
The system SHALL provide an MCP server that initializes with the North MCP Python SDK and supports streamable HTTP transport.

#### Scenario: Server starts successfully
- **WHEN** the server is started with valid configuration
- **THEN** the server binds to the specified port
- **AND** the server accepts MCP protocol connections
- **AND** the server logs startup information

#### Scenario: Server fails with invalid configuration
- **WHEN** the server is started with missing SERVER_SECRET
- **THEN** the server SHALL fail with a clear error message
- **AND** the error SHALL indicate the missing configuration

### Requirement: Authentication Support
The system SHALL authenticate incoming requests using server secret and optional user identity tokens.

#### Scenario: Authenticated request succeeds
- **WHEN** a request includes valid server secret in bearer token
- **THEN** the server SHALL process the request
- **AND** the server SHALL make user identity available to tools (if provided)

#### Scenario: Unauthenticated request rejected
- **WHEN** a request includes invalid or missing server secret
- **THEN** the server SHALL reject the request
- **AND** the server SHALL return an authentication error
- **AND** the server SHALL log the authentication failure

#### Scenario: User identity extraction
- **WHEN** a request includes user_id_token in bearer token
- **THEN** the server SHALL decode the JWT token
- **AND** the server SHALL make user email available via get_authenticated_user()
- **AND** the server SHALL make OAuth tokens available if present

### Requirement: Tool Registration System
The system SHALL provide a mechanism for registering and discovering MCP tools dynamically.

#### Scenario: Tool registration via decorator
- **WHEN** a tool is decorated with @mcp.tool()
- **THEN** the server SHALL register the tool
- **AND** the tool SHALL be discoverable via MCP list tools command
- **AND** the tool SHALL be invocable via MCP call tool command

#### Scenario: Tool invocation with arguments
- **WHEN** a registered tool is called with valid arguments
- **THEN** the server SHALL execute the tool function
- **AND** the server SHALL return the tool result
- **AND** the server SHALL log the tool invocation

### Requirement: Transport Configuration
The system SHALL support streamable HTTP transport for North MCP compatibility.

#### Scenario: Streamable HTTP transport configuration
- **WHEN** the server is started with --transport streamable-http
- **THEN** the server SHALL use streamable HTTP protocol
- **AND** the server SHALL expose MCP endpoint at /mcp path
- **AND** the server SHALL accept POST requests with MCP payloads

#### Scenario: Stdio transport for testing
- **WHEN** the server is started with --transport stdio
- **THEN** the server SHALL use stdio transport
- **AND** the server SHALL communicate via standard input/output
- **AND** authentication SHALL be optional

### Requirement: Debug Mode
The system SHALL provide a debug mode that logs detailed authentication and request information for troubleshooting.

#### Scenario: Debug mode enabled
- **WHEN** the server is started with DEBUG=true or --debug flag
- **THEN** the server SHALL log detailed authentication steps
- **AND** the server SHALL log request headers and payloads
- **AND** the server SHALL log token parsing and validation steps

#### Scenario: Debug mode disabled
- **WHEN** debug mode is not enabled
- **THEN** the server SHALL log only INFO level and above
- **AND** the server SHALL NOT log sensitive authentication details

### Requirement: Configuration Management
The system SHALL load configuration from environment variables and CLI arguments.

#### Scenario: Environment variable loading
- **WHEN** the server starts
- **THEN** the server SHALL load SERVER_SECRET from environment
- **AND** the server SHALL load optional DEBUG flag from environment
- **AND** the server SHALL load other API keys as needed

#### Scenario: CLI argument override
- **WHEN** CLI arguments are provided
- **THEN** CLI arguments SHALL override environment variables
- **AND** the server SHALL use CLI-provided port, transport, and debug settings

### Requirement: Graceful Shutdown
The system SHALL handle shutdown signals gracefully and clean up resources.

#### Scenario: SIGINT received
- **WHEN** the server receives SIGINT (Ctrl+C)
- **THEN** the server SHALL log shutdown message
- **AND** the server SHALL close open connections
- **AND** the server SHALL exit with status code 0

### Requirement: Bearer Token Testing Support
The system SHALL provide utilities for generating bearer tokens for local testing with MCP Inspector.

#### Scenario: Bearer token generation
- **WHEN** create_bearer_token.py is executed
- **THEN** the script SHALL generate a JWT for user_id_token
- **AND** the script SHALL encode server_secret, user_id_token, and optional connector tokens
- **AND** the script SHALL output a valid Base64-encoded bearer token
- **AND** the token SHALL be usable with MCP Inspector

#### Scenario: Token validation
- **WHEN** a generated bearer token is used in a request
- **THEN** the server SHALL successfully decode and validate it
- **AND** user identity SHALL be accessible in tools

