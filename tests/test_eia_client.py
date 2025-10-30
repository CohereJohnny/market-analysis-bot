"""
Tests for EIA API client.
"""

import pytest
from unittest.mock import Mock, patch
from utils.eia_client import EIAClient


def test_client_initialization_success():
    """Test EIA client initializes with valid API key."""
    client = EIAClient(api_key="test-key")
    assert client.api_key == "test-key"
    assert client.request_count == 0


def test_client_initialization_missing_key():
    """Test EIA client raises error without API key."""
    with pytest.raises(ValueError) as exc_info:
        EIAClient(api_key="")
    
    assert "API key required" in str(exc_info.value)
    assert "signups.eia.gov" in str(exc_info.value)


def test_validate_params_missing_path():
    """Test parameter validation fails with missing path."""
    client = EIAClient(api_key="test-key")
    
    with pytest.raises(ValueError) as exc_info:
        client._validate_params("", "monthly", 100)
    
    assert "Path parameter is required" in str(exc_info.value)


def test_validate_params_invalid_frequency():
    """Test parameter validation fails with invalid frequency."""
    client = EIAClient(api_key="test-key")
    
    with pytest.raises(ValueError) as exc_info:
        client._validate_params("petroleum/pri/spt", "invalid", 100)
    
    assert "Invalid frequency" in str(exc_info.value)
    assert "daily, weekly, monthly, annual" in str(exc_info.value)


def test_build_params_basic():
    """Test building basic query parameters."""
    client = EIAClient(api_key="test-key")
    
    params = client._build_params(
        facets=None,
        start=None,
        end=None,
        frequency="monthly",
        data_fields=["value"],
        sort=None,
        limit=100
    )
    
    assert params["api_key"] == "test-key"
    assert params["frequency"] == "monthly"
    assert params["data[0]"] == "value"
    assert params["limit"] == 100


def test_build_params_with_dates():
    """Test building parameters with date range."""
    client = EIAClient(api_key="test-key")
    
    params = client._build_params(
        facets=None,
        start="2025-01-01",
        end="2025-10-30",
        frequency="weekly",
        data_fields=["value"],
        sort=None,
        limit=50
    )
    
    assert params["start"] == "2025-01-01"
    assert params["end"] == "2025-10-30"
    assert params["frequency"] == "weekly"


def test_build_params_with_facets():
    """Test building parameters with facets."""
    client = EIAClient(api_key="test-key")
    
    facets = {"series": ["RWTC", "RBRTE"]}
    params = client._build_params(
        facets=facets,
        start=None,
        end=None,
        frequency="monthly",
        data_fields=["value"],
        sort=None,
        limit=100
    )
    
    # Check facets are formatted correctly for EIA API
    assert "facets[series][]" in str(params)


def test_rate_limit_warning(caplog):
    """Test rate limit warning is logged."""
    client = EIAClient(api_key="test-key")
    client.request_count = 4500  # Over warning threshold
    
    with caplog.at_level("WARNING"):
        client._check_rate_limit()
    
    assert "Approaching EIA API rate limit" in caplog.text


@patch('requests.get')
def test_query_success(mock_get):
    """Test successful API query."""
    # Mock successful API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": {
            "data": [
                {"period": "2025-10", "value": 71.5},
                {"period": "2025-09", "value": 70.2}
            ]
        }
    }
    mock_get.return_value = mock_response
    
    client = EIAClient(api_key="test-key")
    result = client.query(path="petroleum/pri/spt", limit=100)
    
    assert "response" in result
    assert "data" in result["response"]
    assert len(result["response"]["data"]) == 2


@patch('requests.get')
def test_query_404_error(mock_get):
    """Test API query with invalid path (404)."""
    # Mock 404 response
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = Exception("404 Error")
    mock_get.return_value = mock_response
    
    client = EIAClient(api_key="test-key")
    
    with pytest.raises(Exception):
        client.query(path="invalid/path", limit=100)


@patch('requests.get')
def test_query_rate_limit_error(mock_get):
    """Test API query when rate limit exceeded (429)."""
    # Mock 429 response
    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.raise_for_status.side_effect = Exception("429 Error")
    mock_get.return_value = mock_response
    
    client = EIAClient(api_key="test-key")
    
    with pytest.raises(Exception):
        client.query(path="petroleum/pri/spt", limit=100)

