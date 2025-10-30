# Sprint 1 Validation Guide

## Manual Testing Checklist

### Prerequisites
- [ ] uv installed and working
- [ ] North MCP SDK installed
- [ ] Node.js installed (for MCP Inspector)
- [ ] .env file created with SERVER_SECRET

### 1. Install Dependencies
```bash
cd /Users/jkb/Demos/market-analysis-bot
uv pip install git+https://github.com/cohere-ai/north-mcp-python-sdk.git
uv sync
```

### 2. Generate Bearer Token
```bash
uv run examples/create_bearer_token.py \
  --server-secret demo-secret-key \
  --email trader@test.com \
  --with-connectors \
  --output-file bearer_token.txt
```

Expected output:
- JWT token generated successfully
- Bearer token Base64 encoded
- Token saved to bearer_token.txt

### 3. Test Server Startup - Streamable HTTP

```bash
# Terminal 1: Start server with debug mode
SERVER_SECRET=demo-secret-key uv run server.py --debug
```

Expected output:
```
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

Validation:
- [ ] Server starts without errors
- [ ] hello_world tool registered
- [ ] Server listens on port 5222
- [ ] Debug logging appears

### 4. Test Server Startup - Stdio

```bash
SERVER_SECRET=demo-secret-key uv run server.py --transport stdio
```

Validation:
- [ ] Server starts in stdio mode
- [ ] No port binding (stdio uses stdin/stdout)

### 5. Test with MCP Inspector

```bash
# Terminal 2: Start MCP Inspector
npx @modelcontextprotocol/inspector
```

MCP Inspector Configuration:
1. Transport Type: **Streamable HTTP**
2. URL: `http://localhost:5222/mcp`
3. Authentication → Bearer token: [paste from bearer_token.txt]
4. Click **"Connect"**

Validation:
- [ ] Inspector connects successfully
- [ ] No connection errors in server logs
- [ ] Authentication debug logs appear (if debug mode on)

### 6. Test hello_world Tool

In MCP Inspector:
1. Select **"Tools"** tab
2. Click **"List Tools"**
3. Verify `hello_world` appears in list
4. Select `hello_world` tool
5. Set parameter: `name: "Trader"`
6. Click **"Run"**

Expected Response:
```
Hello, Trader! Welcome to the Market Analysis Bot.

Authenticated as: trader@test.com
Available connectors: google, slack

Server Status: ✓ Running
This is a demonstration MCP server for energy trading market analysis.
```

Validation:
- [ ] Tool executes successfully
- [ ] Authenticated user email shown
- [ ] Connector tokens displayed
- [ ] Server logs show tool invocation

### 7. Test Authentication

Test 1: Valid Bearer Token
- [ ] Connection succeeds with valid token
- [ ] User identity extracted correctly

Test 2: Invalid Bearer Token
```bash
# Try connecting with wrong token in Inspector
```
- [ ] Connection rejected or auth error logged

Test 3: Missing SERVER_SECRET
```bash
# Start server without SERVER_SECRET
uv run server.py
```
- [ ] Server fails to start with clear error message

### 8. Test Debug Mode

With debug mode ON (`--debug`):
- [ ] Detailed authentication logs appear
- [ ] Request/response logging visible
- [ ] Token parsing steps logged

With debug mode OFF (default):
- [ ] Only INFO level logs
- [ ] No sensitive auth details in logs

### 9. Test Graceful Shutdown

```bash
# In server terminal, press Ctrl+C
```

Expected:
- [ ] "Shutdown requested" message appears
- [ ] Server stops cleanly
- [ ] Exit code 0

### 10. Run Basic Tests

```bash
uv run pytest tests/test_hello_world.py -v
```

Validation:
- [ ] All import tests pass
- [ ] No import errors

## OpenSpec Validation

```bash
openspec validate add-mcp-server --strict
```

Validation:
- [ ] Change validates successfully
- [ ] All requirements have scenarios
- [ ] No validation errors

## Sprint 1 Completion Criteria

All items must be checked:
- [x] Project structure created
- [x] Dependencies configured
- [x] Server implementation complete
- [x] Authentication system working
- [x] Tool registration functional
- [x] Logging infrastructure in place
- [x] Bearer token generator working
- [x] Documentation updated
- [ ] Manual testing completed successfully
- [ ] MCP Inspector connectivity verified
- [ ] hello_world tool tested and working

## Next Steps

After successful validation:
1. Update sprint_1_tasks.md (mark all items complete)
2. Update sprint_1_updates.md with final notes
3. Commit all changes to sprint-1 branch
4. Create pull request (or continue to Sprint 2)
5. Prepare to archive OpenSpec change `add-mcp-server`

## Troubleshooting

### Issue: North MCP SDK Not Found
```
Error: North MCP Python SDK not found.
```
**Solution**: `uv pip install git+https://github.com/cohere-ai/north-mcp-python-sdk.git`

### Issue: SERVER_SECRET Required
```
ERROR - SERVER_SECRET is required for streamable-http transport.
```
**Solution**: Set environment variable or use `--server-secret` flag

### Issue: MCP Inspector Won't Connect
- Verify server is running on correct port
- Check bearer token is valid
- Ensure SERVER_SECRET matches token
- Check server logs for authentication errors

### Issue: Tool Not Appearing
- Check server logs for tool registration errors
- Verify `register_all_tools()` is called
- Check import errors in tools module

## Notes

- This is Sprint 1 foundation - tools will be added in Sprint 2-3
- North SDK API may require adjustments if SDK changes
- Some authentication features depend on actual North platform behavior
- Test with actual North platform for production validation

