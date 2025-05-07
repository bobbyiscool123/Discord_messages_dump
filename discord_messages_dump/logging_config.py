"""Logging configuration for Discord Messages Dump.

This module provides a centralized configuration for logging in the Discord Messages Dump
package. It sets up console and file handlers with colored output and rotation.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
import sys
from typing import Optional, Dict, Any


# Define custom colors for log levels
class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log level names in console output.
    
    This formatter adds ANSI color codes to the log level names in the log messages,
    making it easier to distinguish between different log levels in the console.
    
    Attributes:
        COLORS (Dict[str, str]): A dictionary mapping log level names to ANSI color codes.
        FORMAT (str): The log message format string.
        DATE_FORMAT (str): The date format string.
    """
    
    # ANSI color codes
    COLORS: Dict[str, str] = {
        'DEBUG': '\033[36m',  # Cyan
        'INFO': '\033[32m',   # Green
        'WARNING': '\033[33m', # Yellow
        'ERROR': '\033[31m',  # Red
        'CRITICAL': '\033[41m\033[37m', # White on Red background
        'RESET': '\033[0m'    # Reset to default
    }
    
    FORMAT = "[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with colors.
        
        Args:
            record (logging.LogRecord): The log record to format.
            
        Returns:
            str: The formatted log message with colors.
        """
        # Save the original levelname
        original_levelname = record.levelname
        
        # Add color to the levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        # Format the message
        result = super().format(record)
        
        # Restore the original levelname
        record.levelname = original_levelname
        
        return result


def setup_logging(
    logger_name: str = "discord-dump",
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    console: bool = True
) -> logging.Logger:
    """Set up logging with console and file handlers.
    
    This function sets up a logger with console and file handlers. The console handler
    uses colored output, and the file handler uses rotation at 5MB.
    
    Args:
        logger_name (str, optional): The name of the logger. Defaults to "discord-dump".
        log_level (Optional[str], optional): The log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            If None, it will be read from the LOG_LEVEL environment variable, defaulting to INFO.
            Defaults to None.
        log_file (Optional[str], optional): The path to the log file. If None, no file handler
            will be added. Defaults to None.
        console (bool, optional): Whether to add a console handler. Defaults to True.
        
    Returns:
        logging.Logger: The configured logger.
    """
    # Get the logger
    logger = logging.getLogger(logger_name)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Determine log level
    if log_level is None:
        log_level = os.environ.get("LOG_LEVEL", "INFO")
    
    # Convert log level string to logging level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    # Create formatters
    console_formatter = ColoredFormatter(
        fmt=ColoredFormatter.FORMAT,
        datefmt=ColoredFormatter.DATE_FORMAT
    )
    
    file_formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Add console handler if requested
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    # Add file handler if log file is specified
    if log_file:
        # Create the directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create a rotating file handler (5MB max size, keep 3 backups)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3,
            encoding="utf-8"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger with the specified name.
    
    This is a convenience function to get a logger with the specified name.
    If no name is provided, it returns the root logger for the package.
    
    Args:
        name (Optional[str], optional): The name of the logger. If None, returns
            the root logger for the package. Defaults to None.
            
    Returns:
        logging.Logger: The logger.
    """
    if name is None:
        return logging.getLogger("discord-dump")
    return logging.getLogger(f"discord-dump.{name}")
