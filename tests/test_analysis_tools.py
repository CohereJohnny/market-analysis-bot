"""
Tests for analysis_tools module.
"""

import pytest
import numpy as np


def test_monte_carlo_basic():
    """Test basic Monte Carlo simulation."""
    from tools.analysis_tools import register_analysis_tools
    from unittest.mock import MagicMock
    
    # Mock MCP server
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    
    # Register tools
    register_analysis_tools(mcp)
    
    # Test monte_carlo_simulation
    assert "monte_carlo_simulation" in tool_functions
    result = tool_functions["monte_carlo_simulation"](
        current_price=70.0,
        volatility=0.25,
        days=30,
        simulations=100
    )
    
    assert "Monte Carlo Price Simulation" in result
    assert "$70.00" in result
    assert "25.0% annual" in result
    assert "Confidence Intervals" in result


def test_monte_carlo_price_movement():
    """Test that Monte Carlo produces reasonable price distributions."""
    from tools.analysis_tools import register_analysis_tools
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_analysis_tools(mcp)
    
    # Run simulation
    result = tool_functions["monte_carlo_simulation"](
        current_price=100.0,
        volatility=0.20,
        days=10,
        simulations=500
    )
    
    # Check that results include key metrics
    assert "Mean" in result
    assert "Median" in result
    assert "Std Dev" in result
    assert "95%" in result


def test_calculate_statistics_basic():
    """Test basic statistical calculations."""
    from tools.analysis_tools import register_analysis_tools
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_analysis_tools(mcp)
    
    # Test calculate_statistics
    assert "calculate_statistics" in tool_functions
    result = tool_functions["calculate_statistics"](
        values="10,20,30,40,50",
        label="Test Data"
    )
    
    assert "Statistical Analysis: Test Data" in result
    assert "Sample Size" in result
    assert "5 values" in result
    assert "Mean" in result
    assert "30.00" in result  # Mean of 10,20,30,40,50


def test_calculate_statistics_single_value():
    """Test statistics with single value."""
    from tools.analysis_tools import register_analysis_tools
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_analysis_tools(mcp)
    
    result = tool_functions["calculate_statistics"](
        values="42.5",
        label="Single Value"
    )
    
    assert "42.50" in result
    assert "1 values" in result


def test_calculate_statistics_invalid_input():
    """Test statistics with invalid input."""
    from tools.analysis_tools import register_analysis_tools
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_analysis_tools(mcp)
    
    # Test with non-numeric values
    result = tool_functions["calculate_statistics"](
        values="abc,def",
        label="Invalid"
    )
    
    assert "Error" in result


def test_calculate_statistics_empty():
    """Test statistics with empty input."""
    from tools.analysis_tools import register_analysis_tools
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_analysis_tools(mcp)
    
    # Test with empty string (after split, will have one empty value)
    result = tool_functions["calculate_statistics"](
        values="",
        label="Empty"
    )
    
    # Should handle gracefully
    assert "Error" in result or "0 values" in result

