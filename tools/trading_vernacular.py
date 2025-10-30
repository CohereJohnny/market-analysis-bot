"""
Trading Vernacular - Explanations of energy trading terminology.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from north_mcp_python_sdk import NorthMCPServer

logger = logging.getLogger(__name__)

# Energy trading glossary
GLOSSARY = {
    "wti": {
        "full_name": "West Texas Intermediate",
        "definition": "Light, sweet crude oil benchmark priced at Cushing, Oklahoma. Primary US oil price reference.",
        "context": "Trading: 'WTI futures' refers to NYMEX contracts. 'WTI spot' is physical oil at Cushing."
    },
    "brent": {
        "full_name": "Brent Crude",
        "definition": "Global oil price benchmark from North Sea production. Priced at ICE exchange.",
        "context": "Trading: Brent is the international standard. Typically trades at premium to WTI."
    },
    "crack spread": {
        "full_name": "Crack Spread",
        "definition": "Difference between crude oil price and refined product prices (gasoline, diesel).",
        "context": "Trading: Refiners monitor crack spreads to assess profitability. '3-2-1 crack' = 3 barrels crude to 2 gasoline, 1 diesel."
    },
    "contango": {
        "full_name": "Contango",
        "definition": "Market condition where future prices are higher than spot prices.",
        "context": "Trading: Indicates excess supply or storage costs. Traders can profit by buying spot, selling futures, and storing."
    },
    "backwardation": {
        "full_name": "Backwardation",
        "definition": "Market condition where future prices are lower than spot prices.",
        "context": "Trading: Indicates tight supply. No incentive to store. Immediate demand exceeds future expectations."
    },
    "eia": {
        "full_name": "U.S. Energy Information Administration",
        "definition": "Federal agency providing energy data, forecasts, and analysis.",
        "context": "Trading: EIA weekly petroleum reports (Wed 10:30 AM ET) are market-moving events. Track inventory levels closely."
    },
    "opec": {
        "full_name": "Organization of Petroleum Exporting Countries",
        "definition": "Cartel of oil-producing nations coordinating production policy.",
        "context": "Trading: OPEC+ meetings drive market volatility. Production cuts/increases directly impact prices."
    },
    "cushing": {
        "full_name": "Cushing, Oklahoma",
        "definition": "Major oil storage hub and delivery point for NYMEX WTI futures contracts.",
        "context": "Trading: Cushing inventory levels signal US supply tightness. Low storage = bullish. High storage = bearish."
    },
    "nymex": {
        "full_name": "New York Mercantile Exchange",
        "definition": "Primary commodity futures exchange for WTI crude and natural gas.",
        "context": "Trading: WTI futures (CL contract) trade on NYMEX. Contract size: 1,000 barrels. Tick: $0.01/barrel = $10."
    },
    "henry hub": {
        "full_name": "Henry Hub",
        "definition": "Natural gas pipeline hub in Louisiana. Pricing point for NYMEX gas futures.",
        "context": "Trading: NG contract settled at Henry Hub. Regional basis differentials affect local gas pricing."
    },
    "mcf": {
        "full_name": "Thousand Cubic Feet",
        "definition": "Unit of natural gas volume measurement. 1 MCF ≈ 1 MMBtu.",
        "context": "Trading: Natural gas priced in $/MMBtu. Production reported in MCF or BCF (billion cubic feet)."
    },
    "mmbtu": {
        "full_name": "Million British Thermal Units",
        "definition": "Energy content measurement for natural gas. Standard trading unit.",
        "context": "Trading: Henry Hub futures quoted in $/MMBtu. 1 MMBtu ≈ 1 MCF for pipeline-quality gas."
    },
    "strip": {
        "full_name": "Calendar Strip",
        "definition": "Series of futures contracts spanning a time period (month, quarter, year).",
        "context": "Trading: 'Buying the 2026 strip' = buying all 12 monthly contracts for 2026. Provides price certainty."
    },
    "basis": {
        "full_name": "Basis Differential",
        "definition": "Price difference between local market and benchmark (e.g., WTI minus Houston crude).",
        "context": "Trading: Basis risk affects hedging. Narrow basis = strong local market. Wide basis = weak local demand."
    },
    "arb": {
        "full_name": "Arbitrage",
        "definition": "Exploiting price differences between related markets or contracts.",
        "context": "Trading: 'Brent-WTI arb' = spread between benchmarks. 'Time arb' = contango/backwardation play."
    },
    "prompt": {
        "full_name": "Prompt Month",
        "definition": "Nearest futures contract month. Most liquid and actively traded.",
        "context": "Trading: Prompt WTI = front-month contract. Price most sensitive to immediate supply/demand."
    },
    "long": {
        "full_name": "Long Position",
        "definition": "Owning an asset or futures contract. Profits when price rises.",
        "context": "Trading: 'Long 100 WTI' = own 100 contracts (100,000 barrels). Bullish position."
    },
    "short": {
        "full_name": "Short Position",
        "definition": "Selling an asset you don't own or selling futures. Profits when price falls.",
        "context": "Trading: 'Short 50 NG' = sold 50 contracts without owning. Bearish position. Must buy back to close."
    }
}


def register_vernacular_tool(mcp: "NorthMCPServer") -> None:
    """
    Register trading vernacular tool with the MCP server.
    
    Args:
        mcp: The NorthMCPServer instance
    """
    
    @mcp.tool()
    def explain_trading_term(term: str) -> str:
        """
        Explain energy trading terminology and jargon.
        
        Provides definitions, full names, and context for common terms
        used in oil and natural gas trading.
        
        Args:
            term: Trading term to explain (e.g., "wti", "contango", "crack spread")
        
        Returns:
            Formatted explanation with definition and trading context
        
        Example:
            term="contango" -> Explains market structure and trading implications
        """
        logger.info(f"Vernacular lookup: {term}")
        
        # Normalize term
        term_key = term.lower().strip()
        
        if term_key in GLOSSARY:
            entry = GLOSSARY[term_key]
            
            response = f"## {entry['full_name']}\n\n"
            response += f"**Term**: `{term}`\n\n"
            response += f"### Definition\n{entry['definition']}\n\n"
            response += f"### Trading Context\n{entry['context']}\n"
            
            return response
        else:
            # Provide helpful response with available terms
            available = list(GLOSSARY.keys())[:10]  # First 10 terms
            
            response = f"❓ **Term not found**: `{term}`\n\n"
            response += f"### Available Terms\n"
            response += f"Try these common trading terms:\n"
            for t in available:
                response += f"- `{t}`\n"
            response += f"\n*Total terms in glossary: {len(GLOSSARY)}*"
            
            return response
    
    @mcp.tool()
    def list_trading_terms(category: str = "all") -> str:
        """
        List available trading terms in the glossary.
        
        Args:
            category: Filter by category - "all", "benchmarks", "concepts", or "measurements"
        
        Returns:
            Organized list of available terms
        
        Example:
            category="benchmarks" -> Lists WTI, Brent, Henry Hub, etc.
        """
        logger.info(f"Listing terms: category={category}")
        
        # Categorize terms
        benchmarks = ["wti", "brent", "henry hub", "cushing", "nymex"]
        concepts = ["contango", "backwardation", "crack spread", "basis", "arb", "strip", "prompt"]
        measurements = ["mcf", "mmbtu"]
        organizations = ["eia", "opec"]
        positions = ["long", "short"]
        
        response = "## Energy Trading Glossary\n\n"
        
        if category == "all" or category == "benchmarks":
            response += "### 📊 Benchmarks & Markets\n"
            for term in benchmarks:
                if term in GLOSSARY:
                    response += f"- **{term}**: {GLOSSARY[term]['full_name']}\n"
            response += "\n"
        
        if category == "all" or category == "concepts":
            response += "### 💡 Trading Concepts\n"
            for term in concepts:
                if term in GLOSSARY:
                    response += f"- **{term}**: {GLOSSARY[term]['definition'][:60]}...\n"
            response += "\n"
        
        if category == "all" or category == "measurements":
            response += "### 📏 Measurements\n"
            for term in measurements:
                if term in GLOSSARY:
                    response += f"- **{term}**: {GLOSSARY[term]['full_name']}\n"
            response += "\n"
        
        if category == "all":
            response += "### 🏢 Organizations\n"
            for term in organizations:
                if term in GLOSSARY:
                    response += f"- **{term}**: {GLOSSARY[term]['full_name']}\n"
            response += "\n"
            
            response += "### 📈 Positions\n"
            for term in positions:
                if term in GLOSSARY:
                    response += f"- **{term}**: {GLOSSARY[term]['full_name']}\n"
            response += "\n"
        
        response += f"*Use `explain_trading_term` to get detailed explanations.*"
        
        return response
    
    logger.debug("Trading vernacular tool registered")

