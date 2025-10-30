#!/usr/bin/env python3
"""
Market Analysis Bot - MCP Server
A demonstration MCP server for energy trading market analysis using Cohere North.
"""

import argparse
import logging
import os
import signal
import sys
from typing import Optional

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import North MCP SDK (will be available after uv sync)
try:
    from north_mcp_python_sdk import NorthMCPServer
except ImportError:
    print("Error: North MCP Python SDK not found.")
    print("Please install it with: uv pip install git+https://github.com/cohere-ai/north-mcp-python-sdk.git")
    sys.exit(1)

from utils.logging import setup_logging
from tools import register_all_tools


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Market Analysis Bot - MCP Server for Energy Trading"
    )
    parser.add_argument(
        "--transport",
        type=str,
        choices=["streamable-http", "stdio"],
        default=os.getenv("TRANSPORT", "streamable-http"),
        help="Transport protocol (default: streamable-http)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("SERVER_PORT", "5222")),
        help="Server port for streamable-http transport (default: 5222)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=os.getenv("DEBUG", "false").lower() == "true",
        help="Enable debug mode for detailed logging",
    )
    parser.add_argument(
        "--server-secret",
        type=str,
        default=os.getenv("SERVER_SECRET"),
        help="Server secret for authentication (can also use SERVER_SECRET env var)",
    )
    return parser.parse_args()


def validate_configuration(args: argparse.Namespace) -> None:
    """Validate server configuration."""
    if args.transport == "streamable-http" and not args.server_secret:
        logging.error(
            "SERVER_SECRET is required for streamable-http transport. "
            "Set it via --server-secret flag or SERVER_SECRET environment variable."
        )
        sys.exit(1)
    
    # Warn if EIA API key is missing (not critical for basic server operation)
    if not os.getenv("EIA_API_KEY"):
        logging.warning(
            "EIA_API_KEY not set. EIA data tool will not function. "
            "Register at https://signups.eia.gov/api/signup/"
        )


def create_server(args: argparse.Namespace) -> NorthMCPServer:
    """Create and configure the MCP server."""
    server_kwargs = {
        "name": "Market Analysis Assistant",
        "debug": args.debug,
    }
    
    # Add transport-specific configuration
    if args.transport == "streamable-http":
        server_kwargs["port"] = args.port
        server_kwargs["server_secret"] = args.server_secret
        logging.info(f"Configuring server with streamable-http on port {args.port}")
    else:
        logging.info("Configuring server with stdio transport")
    
    # Create server instance
    try:
        mcp = NorthMCPServer(**server_kwargs)
        logging.info("MCP server instance created successfully")
        return mcp
    except Exception as e:
        logging.error(f"Failed to create MCP server: {e}")
        sys.exit(1)


def setup_signal_handlers(server: Optional[NorthMCPServer] = None) -> None:
    """Setup graceful shutdown signal handlers."""
    def signal_handler(signum, frame):
        logging.info(f"Received signal {signum}, shutting down gracefully...")
        if server:
            try:
                # The server should have a method to stop gracefully
                # This is a placeholder - adjust based on actual North SDK API
                logging.info("Server shutdown complete")
            except Exception as e:
                logging.error(f"Error during shutdown: {e}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def main() -> None:
    """Main entry point for the MCP server."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging(debug=args.debug)
    
    logging.info("=" * 60)
    logging.info("Market Analysis Bot - MCP Server")
    logging.info("=" * 60)
    logging.info(f"Transport: {args.transport}")
    if args.transport == "streamable-http":
        logging.info(f"Port: {args.port}")
    logging.info(f"Debug Mode: {args.debug}")
    logging.info("=" * 60)
    
    # Validate configuration
    validate_configuration(args)
    
    # Create MCP server
    mcp = create_server(args)
    
    # Register all tools
    try:
        register_all_tools(mcp)
        logging.info("All tools registered successfully")
    except Exception as e:
        logging.error(f"Failed to register tools: {e}")
        sys.exit(1)
    
    # Setup signal handlers for graceful shutdown
    setup_signal_handlers(mcp)
    
    # Start the server
    try:
        logging.info("Starting MCP server...")
        if args.transport == "streamable-http":
            logging.info(f"Server available at: http://localhost:{args.port}/mcp")
            logging.info("Waiting for connections from North platform...")
        else:
            logging.info("Server running in stdio mode")
        
        # Start server (blocking call)
        # Note: Adjust this based on actual North SDK API
        # This is a placeholder that assumes a start() method exists
        if hasattr(mcp, 'start'):
            mcp.start()
        else:
            # Fallback if SDK uses different method
            logging.error("Unable to start server - please check North SDK API")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logging.info("\nShutdown requested by user")
    except Exception as e:
        logging.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logging.info("Server stopped")


if __name__ == "__main__":
    main()

