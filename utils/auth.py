"""
Authentication utilities for Market Analysis Bot MCP server.
Provides helpers for accessing authenticated user information.
"""

import logging
from typing import Optional, Dict, Any

# Import from North MCP SDK
try:
    from north_mcp_python_sdk import get_authenticated_user as _get_authenticated_user
except ImportError:
    _get_authenticated_user = None
    logging.warning("North MCP SDK not available - authentication features disabled")


logger = logging.getLogger(__name__)


class AuthenticatedUser:
    """
    Represents an authenticated user from North platform.
    
    Attributes:
        email: User's email address
        connector_access_tokens: Dict of OAuth tokens for third-party services
        raw_data: Original user data from North SDK
    """
    
    def __init__(self, email: str, connector_access_tokens: Optional[Dict[str, str]] = None, raw_data: Optional[Any] = None):
        self.email = email
        self.connector_access_tokens = connector_access_tokens or {}
        self.raw_data = raw_data
    
    def has_connector(self, connector_name: str) -> bool:
        """Check if user has access token for a specific connector."""
        return connector_name in self.connector_access_tokens
    
    def get_connector_token(self, connector_name: str) -> Optional[str]:
        """Get OAuth token for a specific connector."""
        return self.connector_access_tokens.get(connector_name)
    
    def __repr__(self) -> str:
        connectors = list(self.connector_access_tokens.keys())
        return f"AuthenticatedUser(email='{self.email}', connectors={connectors})"


def get_authenticated_user() -> Optional[AuthenticatedUser]:
    """
    Get the currently authenticated user from the request context.
    
    This function retrieves user information from the North MCP authentication
    context. It should be called within an MCP tool handler to access the
    user who made the request.
    
    Returns:
        AuthenticatedUser if authentication is present, None otherwise
    
    Example:
        ```python
        @mcp.tool()
        def my_tool(param: str) -> str:
            user = get_authenticated_user()
            if user:
                logger.info(f"Tool called by: {user.email}")
                # Access OAuth tokens if needed
                if user.has_connector("google"):
                    google_token = user.get_connector_token("google")
            return "Result"
        ```
    """
    if _get_authenticated_user is None:
        logger.warning("North MCP SDK not available - cannot retrieve authenticated user")
        return None
    
    try:
        # Call the North SDK function to get user from context
        sdk_user = _get_authenticated_user()
        
        if sdk_user is None:
            logger.debug("No authenticated user in current context")
            return None
        
        # Extract user information
        # Note: Adjust field names based on actual North SDK user object structure
        email = getattr(sdk_user, 'email', 'unknown@example.com')
        connector_tokens = getattr(sdk_user, 'connector_access_tokens', {})
        
        user = AuthenticatedUser(
            email=email,
            connector_access_tokens=connector_tokens,
            raw_data=sdk_user
        )
        
        logger.debug(f"Retrieved authenticated user: {user}")
        return user
        
    except Exception as e:
        logger.error(f"Error retrieving authenticated user: {e}", exc_info=True)
        return None


def require_authentication(func):
    """
    Decorator to require authentication for a tool.
    
    If no authenticated user is present, the tool will return an error message
    instead of executing.
    
    Example:
        ```python
        @mcp.tool()
        @require_authentication
        def protected_tool(param: str) -> str:
            user = get_authenticated_user()
            return f"Hello {user.email}"
        ```
    """
    def wrapper(*args, **kwargs):
        user = get_authenticated_user()
        if user is None:
            error_msg = "Authentication required. Please provide valid credentials."
            logger.warning(f"Unauthenticated access attempt to {func.__name__}")
            return error_msg
        return func(*args, **kwargs)
    
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper

