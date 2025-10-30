# Design Document: North Agent Configuration

## Context
This document outlines the design decisions for configuring a custom agent on the Cohere North platform for energy trading market analysis. The agent serves as the user-facing interface to the MCP server, providing an intelligent assistant that understands trading vernacular, accesses specialized tools, and delivers actionable insights.

**Background**:
- North agents are configured via custom instructions that define behavior
- Agents connect to MCP servers for tool access
- Demo must showcase multi-turn conversations with domain expertise
- Target audience: Energy traders analyzing commodity markets

**Constraints**:
- Custom instructions limited to what North platform supports
- Must work with implemented MCP tools (EIA, OPEC, etc.)
- Demo environment (not production)
- Need to balance sophistication with understandability

## Goals / Non-Goals

### Goals
- Create clear, effective custom agent instructions
- Enable natural conversations about energy trading
- Demonstrate proper tool usage and chaining
- Provide comprehensive demo guide for presenters
- Generate realistic sample prompts for testing
- Document agent configuration for reproducibility

### Non-Goals
- Production deployment procedures
- Multi-language support
- Advanced personalization features
- Integration with actual trading systems
- Real-time alerting or monitoring

## Decisions

### Decision 1: Agent Persona and Voice
**Choice**: Professional energy trading analyst with concise, data-driven communication style

**Rationale**:
- Matches target audience expectations (traders)
- Builds credibility through domain expertise
- Professional but not overly formal
- Data-focused aligns with trading decision-making

**Agent Definition**:
- **Name**: Market Analysis Assistant
- **Role**: Energy trading market analyst specializing in oil and gas commodities
- **Tone**: Professional, concise, analytical, helpful
- **Style**: Bullet points for data, paragraphs for analysis, always cite sources

**Voice Characteristics**:
- Uses trading vernacular naturally (ORB, mb/d, CLZ25)
- Quantitative and evidence-based
- Transparent about data sources and limitations
- Proactive in offering relevant analysis

### Decision 2: Custom Instructions Structure
**Choice**: Follow North best practices with clear sections (Role, Mission, Rules, Logic)

**Rationale**:
- Proven pattern from North documentation
- Easy for admins to understand and modify
- Clear separation of concerns
- Testable behavior rules

**Structure**:
```markdown
## Task And Context
[Agent purpose and capabilities]

### Role
[Who the agent is]

### Mission
[Primary goal]

### Core Behaviour Rules
[15-20 specific, testable rules]

### Conditional Logic
[Tool usage patterns]

## Style Guide
[Communication guidelines]

### Output Format
[Response structure]

### Quality Check
[Verification steps]
```

### Decision 3: Tool Usage Strategy
**Choice**: Explicit conditional logic with priority ordering (internal tools → web search)

**Rationale**:
- Prevents unnecessary API calls
- Ensures data source hierarchy
- Makes tool selection predictable
- Demonstrates agentic reasoning

**Tool Priority**:
1. **EIA Data Tool**: For US petroleum/gas data, prices, production
2. **OPEC Report Tool**: For global demand/supply forecasts, OPEC basket prices
3. **Web Search**: For real-time spot prices, analyst opinions, news
4. **Analysis Tool**: For calculations, simulations, trend analysis

**Conditional Logic Examples**:
- IF query mentions WTI/Brent prices → Use EIA tool first
- IF query mentions OPEC MOMR → Use OPEC report tool
- IF query asks for "current" or "today's" prices → Use web search
- IF query asks for simulation/calculation → Use analysis tool
- IF data incomplete or contradictory → Use multiple tools, cite all sources

### Decision 4: Domain Knowledge Handling
**Choice**: Embed trading terminology glossary in instructions with interpretation guidelines

**Rationale**:
- Reduces misinterpretation of abbreviations
- Maintains conversation flow (no need to ask for clarification)
- Demonstrates domain expertise
- Enables natural trader language

**Key Terms to Define**:
- ORB (OPEC Reference Basket)
- mb/d (million barrels per day)
- CLZ25 (December 2025 WTI futures)
- NGZ25 (December 2025 Natural Gas futures)
- MOMR (Monthly Oil Market Report)
- Secondary sources (independent production estimates)
- Henry Hub (natural gas pricing point)
- STEO (Short-Term Energy Outlook)

**Interpretation Rules**:
- Assume "latest" means most recent available data
- "Current" price means today's spot price (use web search)
- "Forecast" means STEO or MOMR projections
- "Trend" requires historical data (minimum 3 months)

### Decision 5: Response Format Standards
**Choice**: Structured responses with data tables, clear citations, and next-step suggestions

**Rationale**:
- Traders need scannable information
- Tables for numerical data improve readability
- Citations build trust
- Next steps enhance conversation flow

**Format Guidelines**:
- **Summary**: 1-2 sentences with key takeaway
- **Data**: Tables for numerical comparisons
- **Analysis**: Bullet points for insights
- **Sources**: Always cite (e.g., "per EIA STEO October 2025")
- **Next Steps**: Optional suggestions for deeper analysis

**Example Structure**:
```
Key Takeaway: WTI prices averaged $71.50/b in October, up 2% from September.

| Month | WTI Price | Change |
|-------|-----------|--------|
| Sept  | $70.20    | -      |
| Oct   | $71.50    | +1.9%  |

Analysis:
- Upward pressure from OPEC supply cuts
- Offset by demand softening in OECD regions
- Futures spreads suggest continued volatility

Source: EIA Petroleum Status Report, Oct 30, 2025

Would you like me to compare this to Brent pricing or run a volatility analysis?
```

### Decision 6: Demo Guide Structure
**Choice**: Progressive complexity structure (Setup → Basic → Intermediate → Advanced)

**Rationale**:
- Accommodates different presenter skill levels
- Builds audience understanding gradually
- Showcases increasing sophistication
- Allows flexible demo timing

**Demo Flow**:
1. **Setup** (5 min): Agent intro, MCP connection verification
2. **Basic Queries** (10 min): Simple data retrieval (WTI price, OPEC production)
3. **Analysis** (10 min): Multi-turn conversation, tool chaining
4. **Advanced** (10 min): Simulations, cross-commodity analysis
5. **Q&A** (5 min): Handle audience questions

### Decision 7: Sample Prompts Organization
**Choice**: Categorize by complexity level and tool usage

**Rationale**:
- Easy to select appropriate prompts for demo phase
- Tests different capabilities systematically
- Provides variety for different demo scenarios
- Documents expected agent behavior

**Categories**:
- **Level 1 - Basic**: Single tool, simple data retrieval
- **Level 2 - Analysis**: Multi-turn, calculations, comparisons
- **Level 3 - Complex**: Tool chaining, simulations, insights
- **Edge Cases**: Error handling, data conflicts, ambiguous queries

## Risks / Trade-offs

### Risk 1: Custom Instructions Too Prescriptive
**Trade-off**: Detailed rules may limit agent flexibility
**Mitigation**: Balance specific rules with general principles; test with varied prompts

### Risk 2: Tool Selection Logic Conflicts
**Trade-off**: Explicit priority may miss optimal tool combinations
**Mitigation**: Include "use multiple tools for comprehensive analysis" guideline

### Risk 3: Demo Complexity Overwhelming
**Trade-off**: Showing all features may confuse audience
**Mitigation**: Progressive structure allows stopping at appropriate level

### Risk 4: Sample Prompts Too Scripted
**Trade-off**: Pre-written prompts may seem inauthentic
**Mitigation**: Include variations and encourage ad-lib based on examples

## Migration Plan
N/A - Initial implementation, no migration needed

## File Organization

```
market-analysis-bot/
├── specs/
│   └── agent-instructions.md       # Custom instructions for North (~200-300 lines)
├── guides/
│   ├── demo-guide.md              # Demo presentation guide (~300-400 lines)
│   ├── sample-prompts.md          # Sample queries (~150-200 lines)
│   └── north-agent-best-practices.md  # Reference (existing)
└── README.md                       # Updated with agent config section
```

## Testing Strategy

### Agent Instruction Validation
- Deploy to North test environment
- Test each behavior rule individually
- Verify tool selection logic
- Check response format compliance

### Demo Rehearsal
- Run through full demo script 3+ times
- Test all sample prompts
- Time each section
- Identify potential failure points

### Edge Case Testing
- Invalid queries
- Tool failures
- Data conflicts
- Ambiguous terminology

## Open Questions
- ~~Should agent refuse non-trading queries?~~ **Decision**: Politely redirect to market analysis scope
- ~~How verbose should explanations be?~~ **Decision**: Concise by default, offer details if asked
- ~~Include price predictions?~~ **Decision**: No predictions, only data-driven analysis with ranges

## References
- North best practices: `guides/north-agent-best-practices.md`
- Sample structure: `guides/sample-agent-instructions.md`
- Demo context: `specs/demo-context.md`
- EIA tool spec: `specs/eia-data.md`
- Project conventions: `openspec/project.md`

