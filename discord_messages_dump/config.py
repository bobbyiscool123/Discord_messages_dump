"""Configuration module for Discord Messages Dump.

This module provides a Config class for loading and validating configuration
from environment variables, .env files, and command-line arguments.
"""

import os
import re
import logging
from typing import Optional, Dict, Any, Union
from pathlib import Path

import dotenv
try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False


logger = logging.getLogger("discord-dump.config")


class ConfigValidationError(Exception):
    """Exception raised when configuration validation fails."""
    pass


class Config:
    """Configuration manager for Discord Messages Dump.
    
    This class loads configuration from environment variables, .env files,
    and command-line arguments, and validates the values.
    
    Attributes:
        token (str): The Discord user token.
        channel_id (str): The Discord channel ID.
        format_type (str): The output format (text, json, csv, markdown).
        output_file (Optional[str]): The output file path.
        limit (int): The maximum number of messages to retrieve.
        log_level (str): The log level.
    """
    
    # Regular expression patterns for validation
    TOKEN_PATTERN = r"^[A-Za-z0-9._-]{59}$"
    CHANNEL_ID_PATTERN = r"^[0-9]{17,19}$"
    
    # Valid format types
    VALID_FORMATS = ["text", "json", "csv", "markdown"]
    
    # Valid log levels
    VALID_LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    def __init__(self, env_file: Optional[str] = None):
        """Initialize the configuration manager.
        
        Args:
            env_file (Optional[str], optional): Path to the .env file. If None,
                looks for .env in the current directory. Defaults to None.
        """
        # Load environment variables from .env file
        if env_file is None:
            env_file = ".env"
        
        self.env_file = env_file
        self._load_env_file()
        
        # Initialize configuration values
        self.token: Optional[str] = None
        self.channel_id: Optional[str] = None
        self.format_type: str = "text"
        self.output_file: Optional[str] = None
        self.limit: int = 100
        self.log_level: str = "INFO"
        
        # Load configuration from environment variables
        self._load_from_env()
    
    def _load_env_file(self) -> None:
        """Load environment variables from .env file."""
        if os.path.exists(self.env_file):
            dotenv.load_dotenv(self.env_file)
            logger.debug(f"Loaded environment variables from {self.env_file}")
        else:
            logger.debug(f"Environment file {self.env_file} not found")
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # Load token
        self.token = os.getenv("DISCORD_TOKEN")
        
        # Load channel ID
        self.channel_id = os.getenv("DISCORD_CHANNEL_ID")
        
        # Load format type
        format_type = os.getenv("FORMAT")
        if format_type:
            self.format_type = format_type.lower()
        
        # Load output file
        self.output_file = os.getenv("OUTPUT_FILE")
        
        # Load message limit
        limit = os.getenv("MESSAGE_LIMIT")
        if limit:
            try:
                self.limit = int(limit)
            except ValueError:
                logger.warning(f"Invalid MESSAGE_LIMIT value: {limit}. Using default: 100")
        
        # Load log level
        log_level = os.getenv("LOG_LEVEL")
        if log_level:
            self.log_level = log_level.upper()
    
    def update_from_args(self, **kwargs: Any) -> None:
        """Update configuration from command-line arguments.
        
        Args:
            **kwargs: Keyword arguments from command-line arguments.
        """
        # Update token
        if kwargs.get("token"):
            self.token = kwargs["token"]
        
        # Update channel ID
        if kwargs.get("channel_id"):
            self.channel_id = kwargs["channel_id"]
        
        # Update format type
        if kwargs.get("format_type"):
            self.format_type = kwargs["format_type"].lower()
        
        # Update output file
        if kwargs.get("output_file"):
            self.output_file = kwargs["output_file"]
        
        # Update message limit
        if kwargs.get("limit"):
            self.limit = kwargs["limit"]
        
        # Update log level
        if kwargs.get("verbose"):
            self.log_level = "DEBUG"
    
    def validate(self) -> None:
        """Validate the configuration.
        
        Raises:
            ConfigValidationError: If any configuration value is invalid.
        """
        # Validate token
        if not self.token:
            raise ConfigValidationError("Discord token is required")
        
        if not re.match(self.TOKEN_PATTERN, self.token):
            raise ConfigValidationError(
                "Invalid Discord token format. Expected a 59-character string."
            )
        
        # Validate channel ID
        if not self.channel_id:
            raise ConfigValidationError("Discord channel ID is required")
        
        if not re.match(self.CHANNEL_ID_PATTERN, self.channel_id):
            raise ConfigValidationError(
                "Invalid Discord channel ID format. Expected a 17-19 digit number."
            )
        
        # Validate format type
        if self.format_type not in self.VALID_FORMATS:
            raise ConfigValidationError(
                f"Invalid format type: {self.format_type}. "
                f"Valid options are: {', '.join(self.VALID_FORMATS)}"
            )
        
        # Validate message limit
        if self.limit <= 0:
            raise ConfigValidationError("Message limit must be greater than 0")
        
        # Validate log level
        if self.log_level not in self.VALID_LOG_LEVELS:
            raise ConfigValidationError(
                f"Invalid log level: {self.log_level}. "
                f"Valid options are: {', '.join(self.VALID_LOG_LEVELS)}"
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a dictionary.
        
        Returns:
            Dict[str, Any]: The configuration as a dictionary.
        """
        return {
            "token": self.token,
            "channel_id": self.channel_id,
            "format_type": self.format_type,
            "output_file": self.output_file,
            "limit": self.limit,
            "log_level": self.log_level
        }
    
    def save_token_to_keyring(self) -> bool:
        """Save the Discord token to the system keyring.
        
        Returns:
            bool: True if the token was saved successfully, False otherwise.
        """
        if not KEYRING_AVAILABLE:
            logger.warning("Keyring module not available. Token not saved.")
            return False
        
        if not self.token:
            logger.warning("No token to save.")
            return False
        
        try:
            keyring.set_password("discord-messages-dump", "discord-token", self.token)
            logger.debug("Token saved to keyring.")
            return True
        except Exception as e:
            logger.error(f"Error saving token to keyring: {e}")
            return False
    
    def load_token_from_keyring(self) -> bool:
        """Load the Discord token from the system keyring.
        
        Returns:
            bool: True if the token was loaded successfully, False otherwise.
        """
        if not KEYRING_AVAILABLE:
            logger.warning("Keyring module not available. Token not loaded.")
            return False
        
        try:
            token = keyring.get_password("discord-messages-dump", "discord-token")
            if token:
                self.token = token
                logger.debug("Token loaded from keyring.")
                return True
            else:
                logger.debug("No token found in keyring.")
                return False
        except Exception as e:
            logger.error(f"Error loading token from keyring: {e}")
            return False


def load_config(env_file: Optional[str] = None, **kwargs: Any) -> Config:
    """Load and validate configuration.
    
    Args:
        env_file (Optional[str], optional): Path to the .env file. Defaults to None.
        **kwargs: Additional configuration values from command-line arguments.
    
    Returns:
        Config: The validated configuration.
        
    Raises:
        ConfigValidationError: If any configuration value is invalid.
    """
    config = Config(env_file)
    
    # Try to load token from keyring if not in environment
    if not config.token:
        config.load_token_from_keyring()
    
    # Update from command-line arguments
    config.update_from_args(**kwargs)
    
    # Validate configuration
    config.validate()
    
    return config
