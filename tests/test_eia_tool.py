"""
Tests for EIA data extractor tool.
"""

import pytest


def test_eia_tool_import():
    """Test that EIA tool module can be imported."""
    from tools import eia_data_extractor
    assert hasattr(eia_data_extractor, 'register_eia_data_extractor')


def test_eia_client_import():
    """Test that EIA client can be imported."""
    from utils import eia_client
    assert hasattr(eia_client, 'EIAClient')


# Integration tests with real API would go here
# These require EIA_API_KEY to be set and are best done manually
# during validation phase

def test_format_response():
    """Test response formatting function."""
    import pandas as pd
    from tools.eia_data_extractor import _format_response
    
    # Create sample data
    df = pd.DataFrame({
        'period': ['2025-10', '2025-09', '2025-08'],
        'value': [71.50, 70.25, 72.10]
    })
    
    result = _format_response(
        df=df,
        path="petroleum/pri/spt",
        frequency="monthly",
        facets='{"series":["RWTC"]}',
        record_count=3
    )
    
    # Check response contains expected elements
    assert "Petroleum Prices" in result
    assert "Period" in result
    assert "$71.50" in result or "71.50" in result
    assert "Summary" in result
    assert "Metadata" in result
    assert "Source" in result
    assert "petroleum/pri/spt" in result


def test_format_response_empty():
    """Test formatting with empty DataFrame."""
    import pandas as pd
    from tools.eia_data_extractor import _format_response
    
    df = pd.DataFrame()
    
    result = _format_response(
        df=df,
        path="test/path",
        frequency="monthly",
        facets="",
        record_count=0
    )
    
    # Should still return valid markdown
    assert isinstance(result, str)
    assert len(result) > 0

