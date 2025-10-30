# Project Context

## Purpose
Market Analysis Bot is an agentic AI assistant designed for energy traders during the market analysis phase. The bot helps traders:
- Analyze real-time commodity market data (WTI, Brent crude, Natural Gas)
- Parse and summarize OPEC Monthly Oil Market Reports (MOMR)
- Run data simulations and visualizations using Python
- Understand trading vernacular and domain-specific terminology
- Provide actionable insights for hedging and trading positions

The goal is to reduce manual report skimming and accelerate decision-making for energy trading workflows, particularly for oil and gas futures positions.

## Tech Stack
- **Framework**: Next.js 14 (React Server Components)
- **Language**: TypeScript
- **Database**: Supabase
- **Styling**: TailwindCSS
- **AI Integration**: Agentic framework (Cohere North or similar)
- **Data Analysis**: Python (NumPy, Pandas, Matplotlib)
- **External APIs**: 
  - Web search for real-time prices
  - OPEC report database API
  - Google Drive (for RAG over documents)

## Project Conventions

### Code Style
- **Component Naming**: Always use kebab-case for component files (e.g., `market-analysis.tsx`, `price-chart.tsx`)
- **TypeScript**: Strict mode enabled, explicit types preferred
- **Formatting**: Prettier with default config
- **Semantic HTML**: Use semantic HTML elements where possible
- **Comments**: Minimal inline comments; prefer self-documenting code
- **Error Handling**: Always implement error handling and error logging

### Architecture Patterns
- **Server-First**: Favour React Server Components and Next.js SSR features where possible
- **Client Components**: Minimize usage of 'use client' to small, isolated components
- **Data Fetching**: Always add loading and error states to data fetching components
- **Simplicity First**: Default to <100 lines of new code per component
- **Single Responsibility**: Components should have a single, clear purpose
- **No Premature Abstraction**: Avoid frameworks and abstractions without clear justification
- **File Organization**: Group by feature/domain, not by type

### Testing Strategy
- Test for existing behavior during implementation
- Bug fixes should restore intended behavior per specifications
- Manual testing required for key user flows before deployment
- Run `pnpm run build` locally to check for build errors before PR

### Git Workflow
- **Branching**: Sprint-based branches (e.g., `sprint-1`, `sprint-2`)
- **Commits**: Conventional commits format:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `refactor:` for code refactoring
  - `docs:` for documentation
  - `test:` for tests
- **Pull Requests**: Create PR at sprint completion, verify checks pass
- **Tagging**: Tag merge commits as `sprint-x` after merging
- **Archive**: Move sprint directories to `sprints/archive/` after completion

## Domain Context

### Energy Trading Terminology
- **ORB**: OPEC Reference Basket - weighted average price of OPEC crude oils
- **mb/d**: Million barrels per day - standard unit for oil production/demand
- **CLZ25**: December 2025 WTI crude oil futures contract on NYMEX
- **NGZ25**: December 2025 Natural Gas futures contract on NYMEX
- **MOMR**: Monthly Oil Market Report published by OPEC
- **Secondary Sources**: Independent production estimates (vs OPEC direct communications)
- **Henry Hub**: Natural gas pricing point and benchmark

### Market Analysis Workflow
1. Review latest OPEC MOMR for demand/supply forecasts
2. Compare current vs previous month's data for trend analysis
3. Check spot prices and futures contracts
4. Run simulations for price ranges and volatility
5. Consider cross-commodity impacts (oil-to-gas substitution)
6. Make hedging and position decisions

### Data Sources
- OPEC Monthly Oil Market Reports (primary source for supply/demand)
- Real-time price feeds (Bloomberg, Reuters, Trading Economics)
- Futures market data (NYMEX codes: CL for WTI, NG for Natural Gas)
- Analyst opinions from major financial institutions

## Important Constraints
- **Real-time Data**: Must access current market prices, not stale data
- **Accuracy**: Trading decisions rely on accurate data interpretation
- **Vernacular**: Must understand energy trading terminology without explicit definitions
- **Performance**: Responses should be fast enough for active trading workflows
- **Transparency**: AI should clearly explain reasoning and data sources
- **Regulatory**: No financial advice; present data and analysis objectively
- **Data Privacy**: Handle proprietary trading strategies confidentially

## External Dependencies
- **OPEC API/Database**: Custom tool for accessing Monthly Oil Market Reports
- **Web Search**: For real-time commodity prices and analyst opinions
- **Google Drive**: For RAG over historical reports and documents
- **Python Runtime**: For NumPy, Pandas, Matplotlib-based analysis
- **Supabase**: Database for storing user preferences and analysis history
- **Market Data APIs**: Bloomberg/Reuters feeds (specific implementation TBD)
