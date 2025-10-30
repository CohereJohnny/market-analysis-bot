"""
Analysis Tools - Statistical analysis and simulations for energy trading.
"""

import logging
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from north_mcp_python_sdk import NorthMCPServer

import numpy as np
import pandas as pd

from utils.auth import get_authenticated_user

logger = logging.getLogger(__name__)


def register_analysis_tools(mcp: "NorthMCPServer") -> None:
    """
    Register analysis tools with the MCP server.
    
    Args:
        mcp: The NorthMCPServer instance
    """
    
    @mcp.tool()
    def monte_carlo_simulation(
        current_price: float,
        volatility: float,
        days: int = 30,
        simulations: int = 1000,
        drift: float = 0.0
    ) -> str:
        """
        Run Monte Carlo simulation for price forecasting.
        
        Simulates potential future price paths using geometric Brownian motion.
        Useful for risk analysis and scenario planning.
        
        Args:
            current_price: Starting price (e.g., 71.50 for WTI at $71.50/barrel)
            volatility: Annual volatility as decimal (e.g., 0.25 for 25%)
            days: Number of days to simulate (default: 30)
            simulations: Number of simulation paths (default: 1000)
            drift: Expected daily return as decimal (default: 0.0)
        
        Returns:
            Formatted results with price distribution and confidence intervals
        
        Example:
            current_price=71.50, volatility=0.25, days=30
            Simulates WTI price over next 30 days with 25% annual volatility
        """
        logger.info(f"Monte Carlo simulation: price={current_price}, vol={volatility}, days={days}")
        
        user = get_authenticated_user()
        if user:
            logger.info(f"Simulation requested by: {user.email}")
        
        try:
            # Convert annual volatility to daily
            daily_vol = volatility / np.sqrt(252)  # 252 trading days/year
            
            # Run simulations
            np.random.seed(42)  # For reproducibility in demo
            results = []
            
            for _ in range(simulations):
                price = current_price
                for _ in range(days):
                    # Geometric Brownian motion
                    change = np.random.normal(drift, daily_vol)
                    price = price * (1 + change)
                results.append(price)
            
            results = np.array(results)
            
            # Calculate statistics
            mean_price = np.mean(results)
            median_price = np.median(results)
            std_dev = np.std(results)
            
            # Confidence intervals
            ci_95_lower = np.percentile(results, 2.5)
            ci_95_upper = np.percentile(results, 97.5)
            ci_68_lower = np.percentile(results, 16)
            ci_68_upper = np.percentile(results, 84)
            
            # Build response
            response = f"## Monte Carlo Price Simulation\n\n"
            response += f"**Starting Price**: ${current_price:.2f}\n"
            response += f"**Volatility**: {volatility*100:.1f}% annual\n"
            response += f"**Time Horizon**: {days} days\n"
            response += f"**Simulations**: {simulations:,}\n\n"
            
            response += f"### Price Distribution (Day {days})\n\n"
            response += f"| Statistic | Price |\n"
            response += f"|-----------|-------|\n"
            response += f"| Mean | ${mean_price:.2f} |\n"
            response += f"| Median | ${median_price:.2f} |\n"
            response += f"| Std Dev | ${std_dev:.2f} |\n\n"
            
            response += f"### Confidence Intervals\n\n"
            response += f"| Confidence | Lower Bound | Upper Bound | Range |\n"
            response += f"|------------|-------------|-------------|-------|\n"
            response += f"| 95% | ${ci_95_lower:.2f} | ${ci_95_upper:.2f} | ${ci_95_upper - ci_95_lower:.2f} |\n"
            response += f"| 68% | ${ci_68_lower:.2f} | ${ci_68_upper:.2f} | ${ci_68_upper - ci_68_lower:.2f} |\n\n"
            
            # Interpretation
            upside = ((ci_95_upper - current_price) / current_price) * 100
            downside = ((current_price - ci_95_lower) / current_price) * 100
            
            response += f"### Interpretation\n\n"
            response += f"- **Upside Potential (95% CI)**: +{upside:.1f}%\n"
            response += f"- **Downside Risk (95% CI)**: -{downside:.1f}%\n"
            response += f"- **Expected Change**: {((mean_price - current_price) / current_price) * 100:+.1f}%\n\n"
            
            response += f"*Simulation uses geometric Brownian motion. Past volatility may not predict future movement.*"
            
            return response
            
        except Exception as e:
            logger.error(f"Monte Carlo simulation error: {e}", exc_info=True)
            return f"❌ **Simulation Error**: {str(e)}"
    
    @mcp.tool()
    def calculate_statistics(
        values: str,
        label: str = "Data"
    ) -> str:
        """
        Calculate statistical measures for a dataset.
        
        Args:
            values: Comma-separated numbers (e.g., "71.5,70.2,72.1,69.8")
            label: Label for the dataset (e.g., "WTI Prices")
        
        Returns:
            Statistical summary with mean, median, std dev, min, max, range
        
        Example:
            values="71.5,70.2,72.1,69.8,71.0", label="WTI Weekly Prices"
        """
        logger.info(f"Statistics calculation for: {label}")
        
        try:
            # Parse values
            data = [float(v.strip()) for v in values.split(",")]
            
            if len(data) == 0:
                return "❌ **Error**: No values provided"
            
            arr = np.array(data)
            
            # Calculate statistics
            mean = np.mean(arr)
            median = np.median(arr)
            std_dev = np.std(arr)
            min_val = np.min(arr)
            max_val = np.max(arr)
            range_val = max_val - min_val
            
            # Build response
            response = f"## Statistical Analysis: {label}\n\n"
            response += f"**Sample Size**: {len(data)} values\n\n"
            
            response += f"| Measure | Value |\n"
            response += f"|---------|-------|\n"
            response += f"| Mean | {mean:.2f} |\n"
            response += f"| Median | {median:.2f} |\n"
            response += f"| Std Deviation | {std_dev:.2f} |\n"
            response += f"| Minimum | {min_val:.2f} |\n"
            response += f"| Maximum | {max_val:.2f} |\n"
            response += f"| Range | {range_val:.2f} |\n\n"
            
            # Coefficient of variation
            cv = (std_dev / mean) * 100
            response += f"### Variability\n\n"
            response += f"- **Coefficient of Variation**: {cv:.1f}%\n"
            response += f"- **Volatility**: {'High' if cv > 10 else 'Moderate' if cv > 5 else 'Low'}\n"
            
            return response
            
        except ValueError as e:
            return f"❌ **Error**: Invalid number format. Use comma-separated values like: 71.5,70.2,72.1"
        except Exception as e:
            logger.error(f"Statistics calculation error: {e}", exc_info=True)
            return f"❌ **Calculation Error**: {str(e)}"
    
    logger.debug("Analysis tools registered")

