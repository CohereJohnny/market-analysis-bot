"""
MCP Tools for Market Analysis Bot.
This module handles tool registration and discovery.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from north_mcp_python_sdk import NorthMCPServer

from .hello_world import register_hello_world
from .eia_data_extractor import register_eia_data_extractor

logger = logging.getLogger(__name__)


def register_all_tools(mcp: "NorthMCPServer") -> None:
    """
    Register all available MCP tools with the server.
    
    Args:
        mcp: The NorthMCPServer instance
    
    This function discovers and registers all tool modules. Add new tool
    registration calls here as tools are implemented.
    """
    logger.info("Registering MCP tools...")
    
    # Track registration count
    registered_count = 0
    
    # Register hello_world tool
    try:
        register_hello_world(mcp)
        registered_count += 1
        logger.info("✓ hello_world tool registered")
    except Exception as e:
        logger.error(f"✗ Failed to register hello_world tool: {e}")
    
    # Register EIA data extractor tool (Sprint 2)
    try:
        register_eia_data_extractor(mcp)
        registered_count += 1
        logger.info("✓ eia_data_extractor tool registered")
    except Exception as e:
        logger.error(f"✗ Failed to register eia_data_extractor tool: {e}")
    
    # Future tools will be registered here:
    # - OPEC report extractor (Sprint 3)
    # - Analysis tools (Sprint 3)
    
    logger.info(f"Tool registration complete: {registered_count} tool(s) registered")
    
    if registered_count == 0:
        logger.warning("No tools were registered successfully")

