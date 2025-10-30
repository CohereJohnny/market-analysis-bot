# Market Analysis Bot - Sprint Plan

## Project Overview
This is a demonstration project showcasing the Cohere North agentic foundry platform. The goal is to build an MCP server that provides energy trading market analysis capabilities using custom tools for EIA data, OPEC reports, and real-time price analysis.

**Demo Focus**: Multi-turn agentic conversations with authentication, custom tools, and domain-specific knowledge.

## Success Criteria
- [ ] Functional MCP server running on North platform
- [ ] EIA data extractor tool retrieving petroleum/gas data
- [ ] OPEC report tool for market analysis
- [ ] Demo conversation script showing realistic trader workflow
- [ ] Authentication working with North's bearer token system
- [ ] Clean code following project conventions

## OpenSpec Integration

This project uses OpenSpec for spec-driven development. Major features are tracked as changes in `openspec/changes/`:

- **Active Changes**: Run `openspec list` to see current proposals
- **Specifications**: Run `openspec list --specs` to see implemented capabilities
- **Change Details**: Run `openspec show [change-id]` to view proposal details
- **Validation**: Run `openspec validate [change-id] --strict` before implementation

### Workflow
1. Create change proposal for new capabilities (proposal.md, tasks.md, design.md, spec deltas)
2. Get approval on proposal before implementing
3. Implement following tasks.md checklist
4. After deployment, archive the change: `openspec archive [change-id]`

## Sprint Breakdown

### Sprint 1: Foundation & Setup (Estimated: 2-3 days)
**Goal**: Set up project infrastructure and basic MCP server

**OpenSpec Change**: `add-mcp-server` (See `openspec/changes/add-mcp-server/`)

**Tasks**:
- Initialize Python project with uv
- Install North MCP SDK and dependencies
- Create basic MCP server with authentication (per OpenSpec change proposal)
- Set up project structure (tools/, tests/, examples/)
- Register for EIA API key
- Create README with setup instructions
- Test basic server connectivity with MCP Inspector
- Follow implementation tasks in `openspec/changes/add-mcp-server/tasks.md`

**Deliverables**:
- Working MCP server with "hello world" tool
- pyproject.toml with all dependencies
- Authentication configured and tested
- Documentation for running locally
- OpenSpec change validated and ready for archival

### Sprint 2: EIA Data Tool Implementation (Estimated: 3-4 days)
**Goal**: Build fully functional EIA data extractor tool

**Tasks**:
- Implement EIA API wrapper with requests
- Create eia_data_extractor MCP tool
- Support key endpoints: petroleum prices, natural gas prices, production
- Handle common series IDs (WTI, Brent, Henry Hub)
- Add error handling and user-friendly messages
- Format responses as tables using pandas
- Write unit tests for EIA tool
- Test with MCP Inspector

**Deliverables**:
- tools/eia_data_extractor.py
- Support for at least 5 common query patterns
- Unit tests with pytest
- Documentation of supported series IDs

### Sprint 3: OPEC & Enhanced Features (Estimated: 2-3 days)
**Goal**: Add OPEC data and analysis capabilities

**Tasks**:
- Implement OPEC report extractor (web scraping or PDF parsing)
- Add data analysis tool for simulations (Monte Carlo, etc.)
- Create helper tool for trading vernacular explanations
- Implement comparison tools (OPEC vs EIA forecasts)
- Add logging and debug mode
- Integration testing with multiple tools

**Deliverables**:
- tools/opec_report_extractor.py
- tools/analysis_tools.py
- Glossary/vernacular mapping
- Integration tests

### Sprint 4: Agent Configuration & Demo (Estimated: 3-4 days)
**Goal**: Configure North agent and create compelling demo materials

**OpenSpec Change**: `add-north-agent-config` (See `openspec/changes/add-north-agent-config/`)

**Tasks**:
- Create custom agent instructions following North best practices
- Define agent role, mission, and behavior rules
- Document tool usage patterns and conditional logic
- Develop comprehensive demo guide with setup and presentation flow
- Generate sample prompts aligned with demo-context.md
- Configure agent on North platform
- Test full conversation flows with deployed agent
- Create presentation materials and talking points
- Polish error messages and responses
- Performance testing and demo rehearsal
- Final documentation review
- Follow implementation tasks in `openspec/changes/add-north-agent-config/tasks.md`

**Deliverables**:
- specs/agent-instructions.md (Custom North agent instructions)
- guides/demo-guide.md (Comprehensive demo presentation guide)
- guides/sample-prompts.md (Sample queries by complexity level)
- Deployed and tested North agent
- Polished README with agent configuration section
- Demo rehearsal checklist and presenter notes
- OpenSpec change validated and ready for archival

## Technical Debt Log
(Items to address post-demo if this becomes a real project)

## Backlog
(Future enhancements beyond demo scope)

## Bug Swatting Log
(Critical bugs discovered during sprints)

