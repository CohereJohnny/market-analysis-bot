"""
Hello World MCP Tool - Example tool for testing server functionality.
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from north_mcp_python_sdk import NorthMCPServer

from utils.auth import get_authenticated_user

logger = logging.getLogger(__name__)


def register_hello_world(mcp: "NorthMCPServer") -> None:
    """
    Register the hello_world tool with the MCP server.
    
    Args:
        mcp: The NorthMCPServer instance
    """
    
    @mcp.tool()
    def hello_world(name: str = "World") -> str:
        """
        A simple greeting tool for testing the MCP server.
        
        This tool demonstrates basic MCP functionality and authentication.
        It returns a personalized greeting and shows the authenticated user
        if available.
        
        Args:
            name: Name to greet (default: "World")
        
        Returns:
            A friendly greeting message
        
        Example:
            >>> hello_world("Trader")
            "Hello, Trader! Welcome to the Market Analysis Bot."
        """
        logger.info(f"hello_world tool called with name='{name}'")
        
        # Try to get authenticated user
        user = get_authenticated_user()
        
        # Build greeting message
        greeting = f"Hello, {name}! Welcome to the Market Analysis Bot."
        
        # Add user context if available
        if user:
            greeting += f"\n\nAuthenticated as: {user.email}"
            logger.info(f"Tool called by authenticated user: {user.email}")
            
            # Show available connectors
            if user.connector_access_tokens:
                connectors = ", ".join(user.connector_access_tokens.keys())
                greeting += f"\nAvailable connectors: {connectors}"
        else:
            logger.debug("Tool called without authentication")
            greeting += "\n\n(No authentication detected)"
        
        # Add server info
        greeting += "\n\nServer Status: ✓ Running"
        greeting += "\nThis is a demonstration MCP server for energy trading market analysis."
        
        return greeting
    
    logger.debug("hello_world tool handler registered")

