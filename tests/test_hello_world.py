"""
Tests for hello_world tool.

Note: These are basic structural tests. Full integration testing requires
a running MCP server and MCP Inspector.
"""

import pytest


def test_hello_world_import():
    """Test that hello_world module can be imported."""
    from tools import hello_world
    assert hasattr(hello_world, 'register_hello_world')


def test_auth_utils_import():
    """Test that auth utilities can be imported."""
    from utils import auth
    assert hasattr(auth, 'get_authenticated_user')
    assert hasattr(auth, 'AuthenticatedUser')


def test_logging_utils_import():
    """Test that logging utilities can be imported."""
    from utils import logging as logging_utils
    assert hasattr(logging_utils, 'setup_logging')
    assert hasattr(logging_utils, 'get_logger')


# Integration tests would go here
# These require a running MCP server and are best done manually
# with MCP Inspector during Sprint 1 validation phase

