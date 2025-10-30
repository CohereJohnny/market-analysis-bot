"""
Tests for trading_vernacular module.
"""

import pytest


def test_explain_term_wti():
    """Test explaining WTI term."""
    from tools.trading_vernacular import register_vernacular_tool
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_vernacular_tool(mcp)
    
    # Test explain_trading_term
    assert "explain_trading_term" in tool_functions
    result = tool_functions["explain_trading_term"](term="wti")
    
    assert "West Texas Intermediate" in result
    assert "Definition" in result
    assert "Trading Context" in result


def test_explain_term_contango():
    """Test explaining contango."""
    from tools.trading_vernacular import register_vernacular_tool
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_vernacular_tool(mcp)
    
    result = tool_functions["explain_trading_term"](term="contango")
    
    assert "Contango" in result
    assert "future prices" in result.lower()
    assert "spot prices" in result.lower()


def test_explain_term_case_insensitive():
    """Test that term lookup is case-insensitive."""
    from tools.trading_vernacular import register_vernacular_tool
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_vernacular_tool(mcp)
    
    # Test uppercase
    result_upper = tool_functions["explain_trading_term"](term="WTI")
    result_lower = tool_functions["explain_trading_term"](term="wti")
    
    assert "West Texas Intermediate" in result_upper
    assert "West Texas Intermediate" in result_lower


def test_explain_term_not_found():
    """Test explaining a term that doesn't exist."""
    from tools.trading_vernacular import register_vernacular_tool
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_vernacular_tool(mcp)
    
    result = tool_functions["explain_trading_term"](term="nonexistent_term")
    
    assert "not found" in result.lower()
    assert "Available Terms" in result


def test_list_terms_all():
    """Test listing all trading terms."""
    from tools.trading_vernacular import register_vernacular_tool
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_vernacular_tool(mcp)
    
    # Test list_trading_terms
    assert "list_trading_terms" in tool_functions
    result = tool_functions["list_trading_terms"](category="all")
    
    assert "Energy Trading Glossary" in result
    assert "Benchmarks" in result
    assert "Trading Concepts" in result
    assert "wti" in result.lower()
    assert "contango" in result.lower()


def test_list_terms_benchmarks():
    """Test listing only benchmark terms."""
    from tools.trading_vernacular import register_vernacular_tool
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_vernacular_tool(mcp)
    
    result = tool_functions["list_trading_terms"](category="benchmarks")
    
    assert "Benchmarks" in result
    assert "wti" in result.lower() or "brent" in result.lower()


def test_list_terms_concepts():
    """Test listing only concept terms."""
    from tools.trading_vernacular import register_vernacular_tool
    from unittest.mock import MagicMock
    
    mcp = MagicMock()
    tool_functions = {}
    
    def mock_tool():
        def decorator(func):
            tool_functions[func.__name__] = func
            return func
        return decorator
    
    mcp.tool = mock_tool
    register_vernacular_tool(mcp)
    
    result = tool_functions["list_trading_terms"](category="concepts")
    
    assert "Trading Concepts" in result
    assert "contango" in result.lower() or "backwardation" in result.lower()


def test_glossary_coverage():
    """Test that glossary has essential trading terms."""
    from tools.trading_vernacular import GLOSSARY
    
    # Check for key terms
    essential_terms = [
        "wti", "brent", "contango", "backwardation",
        "eia", "opec", "henry hub", "nymex"
    ]
    
    for term in essential_terms:
        assert term in GLOSSARY, f"Missing essential term: {term}"
        assert "definition" in GLOSSARY[term]
        assert "full_name" in GLOSSARY[term]
        assert "context" in GLOSSARY[term]

