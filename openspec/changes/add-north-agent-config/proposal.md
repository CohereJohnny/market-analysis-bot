# Change Proposal: Add North Agent Configuration

## Why
Once the MCP server is implemented, we need to configure the custom agent on the Cohere North platform to showcase the energy trading market analysis capabilities. The agent requires carefully crafted custom instructions that define its role, behavior, and tool usage patterns. Additionally, we need comprehensive demo documentation and sample prompts to effectively demonstrate the agent's capabilities to stakeholders.

Without these materials, the demo lacks:
- Proper agent configuration for consistent, domain-aware responses
- Clear guidance for demo presenters
- Structured sample prompts that showcase key features
- Documentation of the agent's purpose and capabilities

## What Changes
- Create custom agent instructions following North best practices
- Define agent role, mission, and core behaviors
- Document tool usage guidelines (EIA data, OPEC reports, analysis)
- Specify trading vernacular handling and domain knowledge
- Create comprehensive demo guide with setup and presentation flow
- Generate sample prompts aligned with demo conversation scenarios
- Document expected agent responses and capabilities
- Add troubleshooting guide for common demo issues

## Impact
- **Affected specs**: `north-agent` (new capability)
- **Affected code/files**: 
  - `specs/agent-instructions.md` - Custom instructions for North agent
  - `guides/demo-guide.md` - Comprehensive demo presentation guide
  - `guides/sample-prompts.md` - Sample queries for demonstration
  - `README.md` - Add agent configuration section
- **Dependencies**: Completed MCP server implementation (add-mcp-server)
- **Testing**: Manual testing with actual North agent deployment
- **Documentation**: Complete demo package for stakeholders

