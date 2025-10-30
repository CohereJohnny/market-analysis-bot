"""
Logging configuration for Market Analysis Bot MCP server.
Provides structured logging with debug mode support.
"""

import logging
import sys
from typing import Optional


def setup_logging(debug: bool = False, log_file: Optional[str] = None) -> None:
    """
    Configure logging for the application.
    
    Args:
        debug: If True, set log level to DEBUG for detailed output
        log_file: Optional path to log file. If None, only log to console.
    """
    # Determine log level
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Create formatters
    if debug:
        # Detailed format for debug mode
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(message)s"
        )
    else:
        # Simpler format for normal operation
        log_format = "%(asctime)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(
        log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            logging.info(f"Logging to file: {log_file}")
        except Exception as e:
            logging.error(f"Failed to setup file logging: {e}")
    
    # Set third-party library log levels
    # Reduce noise from verbose libraries
    if not debug:
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
    
    # Log initial configuration
    if debug:
        logging.debug("Debug mode enabled - verbose logging active")
        logging.debug(f"Log level set to: {logging.getLevelName(log_level)}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (typically __name__ of the module)
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)

