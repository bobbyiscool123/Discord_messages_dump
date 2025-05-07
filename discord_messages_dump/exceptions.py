"""Custom exceptions for Discord Messages Dump.

This module provides a hierarchy of custom exceptions for the Discord Messages Dump
package. These exceptions are used to provide more specific error information
and to make error handling more granular.
"""

from typing import Optional


class DiscordApiError(Exception):
    """Base exception for all Discord API errors.
    
    This is the parent class for all exceptions related to the Discord API.
    It provides a common interface for catching all API-related errors.
    
    Attributes:
        message (str): The error message.
        status_code (Optional[int]): The HTTP status code, if applicable.
    """
    
    def __init__(self, message: str, status_code: Optional[int] = None):
        """Initialize the exception with a message and optional status code.
        
        Args:
            message (str): The error message.
            status_code (Optional[int], optional): The HTTP status code. Defaults to None.
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Return a string representation of the exception.
        
        Returns:
            str: The string representation.
        """
        if self.status_code:
            return f"{self.message} (Status code: {self.status_code})"
        return self.message


class RateLimitError(DiscordApiError):
    """Exception raised when Discord API rate limits are hit.
    
    This exception is raised when the Discord API returns a 429 Too Many Requests
    response, indicating that rate limits have been exceeded.
    
    Attributes:
        message (str): The error message.
        status_code (int): The HTTP status code (429).
        retry_after (float): The number of seconds to wait before retrying.
    """
    
    def __init__(self, message: str, retry_after: float):
        """Initialize the exception with a message and retry_after value.
        
        Args:
            message (str): The error message.
            retry_after (float): The number of seconds to wait before retrying.
        """
        self.retry_after = retry_after
        super().__init__(message, 429)
    
    def __str__(self) -> str:
        """Return a string representation of the exception.
        
        Returns:
            str: The string representation.
        """
        return f"{self.message} (Status code: {self.status_code}, Retry after: {self.retry_after}s)"


class AuthenticationError(DiscordApiError):
    """Exception raised when authentication with Discord API fails.
    
    This exception is raised when the Discord API returns a 401 Unauthorized
    or 403 Forbidden response, indicating that the provided token is invalid
    or does not have the required permissions.
    
    Attributes:
        message (str): The error message.
        status_code (int): The HTTP status code (401 or 403).
    """
    
    def __init__(self, message: str, status_code: int = 401):
        """Initialize the exception with a message and status code.
        
        Args:
            message (str): The error message.
            status_code (int, optional): The HTTP status code. Defaults to 401.
        """
        super().__init__(message, status_code)


class ChannelNotFoundError(DiscordApiError):
    """Exception raised when the specified Discord channel is not found.
    
    This exception is raised when the Discord API returns a 404 Not Found
    response when trying to access a channel, indicating that the channel
    does not exist or the user does not have access to it.
    
    Attributes:
        message (str): The error message.
        channel_id (str): The ID of the channel that was not found.
    """
    
    def __init__(self, channel_id: str):
        """Initialize the exception with the channel ID.
        
        Args:
            channel_id (str): The ID of the channel that was not found.
        """
        self.channel_id = channel_id
        message = f"Channel with ID '{channel_id}' not found or you do not have access to it."
        super().__init__(message, 404)


class MessageProcessingError(Exception):
    """Exception raised when there is an error processing messages.
    
    This exception is raised when there is an error formatting or processing
    message data, such as when the message data is malformed or when there
    is an error writing to a file.
    
    Attributes:
        message (str): The error message.
        format_type (Optional[str]): The format type that was being processed.
    """
    
    def __init__(self, message: str, format_type: Optional[str] = None):
        """Initialize the exception with a message and optional format type.
        
        Args:
            message (str): The error message.
            format_type (Optional[str], optional): The format type that was being processed. Defaults to None.
        """
        self.format_type = format_type
        if format_type:
            message = f"Error processing messages in {format_type} format: {message}"
        super().__init__(message)
