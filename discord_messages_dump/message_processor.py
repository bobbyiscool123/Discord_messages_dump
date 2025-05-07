"""Message processor and formatters for Discord message data.

This module provides classes for processing and formatting Discord message data
into various output formats including plain text, JSON, CSV, and Markdown.
"""

import abc
import csv
import io
import json
from typing import Any, Dict, List, Optional


class MessageProcessingError(Exception):
    """Exception raised for errors in the message processing."""
    pass


class MessageFormatter(abc.ABC):
    """Abstract base class for message formatters.
    
    This class defines the interface for all message formatters.
    Concrete formatter classes should inherit from this class and
    implement the format method.
    """
    
    @abc.abstractmethod
    def format(self, messages: List[Dict[str, Any]]) -> str:
        """Format the messages into a specific output format.
        
        Args:
            messages (List[Dict[str, Any]]): List of Discord message objects.
            
        Returns:
            str: Formatted messages as a string.
            
        Raises:
            MessageProcessingError: If there's an error formatting the messages.
        """
        pass


class TextFormatter(MessageFormatter):
    """Formatter for plain text output."""
    
    def format(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages as plain text.
        
        Format: [timestamp] username: content
        
        Args:
            messages (List[Dict[str, Any]]): List of Discord message objects.
            
        Returns:
            str: Messages formatted as plain text.
            
        Raises:
            MessageProcessingError: If there's an error formatting the messages.
        """
        try:
            result = []
            for message in messages:
                # Extract required fields with fallbacks for malformed data
                timestamp = message.get('timestamp', 'unknown_time')
                author = message.get('author', {})
                username = author.get('username', 'unknown_user')
                content = message.get('content', '')
                
                # Format the message
                result.append(f"[{timestamp}] {username}: {content}")
            
            return "\n".join(result)
        except Exception as e:
            raise MessageProcessingError(f"Error formatting messages as text: {str(e)}")


class JsonFormatter(MessageFormatter):
    """Formatter for JSON output."""
    
    def format(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages as JSON.
        
        Args:
            messages (List[Dict[str, Any]]): List of Discord message objects.
            
        Returns:
            str: Messages formatted as a JSON string.
            
        Raises:
            MessageProcessingError: If there's an error formatting the messages.
        """
        try:
            return json.dumps(messages, indent=2)
        except Exception as e:
            raise MessageProcessingError(f"Error formatting messages as JSON: {str(e)}")


class CsvFormatter(MessageFormatter):
    """Formatter for CSV output."""
    
    def format(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages as CSV.
        
        CSV columns: timestamp, author_id, author_username, content
        
        Args:
            messages (List[Dict[str, Any]]): List of Discord message objects.
            
        Returns:
            str: Messages formatted as CSV.
            
        Raises:
            MessageProcessingError: If there's an error formatting the messages.
        """
        try:
            output = io.StringIO()
            writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
            
            # Write header
            writer.writerow(['timestamp', 'author_id', 'author_username', 'content'])
            
            # Write message data
            for message in messages:
                timestamp = message.get('timestamp', '')
                author = message.get('author', {})
                author_id = author.get('id', '')
                username = author.get('username', '')
                content = message.get('content', '')
                
                writer.writerow([timestamp, author_id, username, content])
            
            return output.getvalue()
        except Exception as e:
            raise MessageProcessingError(f"Error formatting messages as CSV: {str(e)}")


class MarkdownFormatter(MessageFormatter):
    """Formatter for Markdown output."""
    
    def format(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages as Markdown.
        
        Format:
        # Discord Messages
        
        ## Channel: channel_name
        
        ### username - timestamp
        
        message content
        
        Args:
            messages (List[Dict[str, Any]]): List of Discord message objects.
            
        Returns:
            str: Messages formatted as Markdown.
            
        Raises:
            MessageProcessingError: If there's an error formatting the messages.
        """
        try:
            result = ["# Discord Messages\n"]
            
            # Try to get channel name from the first message
            if messages and 'channel_id' in messages[0]:
                channel_id = messages[0].get('channel_id', 'unknown')
                result.append(f"## Channel: {channel_id}\n")
            
            # Format each message
            for message in messages:
                timestamp = message.get('timestamp', 'unknown_time')
                author = message.get('author', {})
                username = author.get('username', 'unknown_user')
                content = message.get('content', '')
                
                result.append(f"### {username} - {timestamp}\n")
                result.append(f"{content}\n")
            
            return "\n".join(result)
        except Exception as e:
            raise MessageProcessingError(f"Error formatting messages as Markdown: {str(e)}")


class MessageProcessor:
    """Processor for Discord message data.
    
    This class provides methods to format Discord message data into
    various output formats using the appropriate formatter classes.
    """
    
    def __init__(self, messages: List[Dict[str, Any]]):
        """Initialize the message processor with raw message data.
        
        Args:
            messages (List[Dict[str, Any]]): List of Discord message objects.
            
        Raises:
            ValueError: If messages is not a list or is empty.
        """
        if not isinstance(messages, list):
            raise ValueError("Messages must be a list")
        
        self.messages = messages
    
    def format_text(self) -> str:
        """Format messages as plain text.
        
        Returns:
            str: Messages formatted as plain text.
            
        Raises:
            MessageProcessingError: If there's an error formatting the messages.
        """
        formatter = TextFormatter()
        return formatter.format(self.messages)
    
    def format_json(self) -> str:
        """Format messages as JSON.
        
        Returns:
            str: Messages formatted as JSON.
            
        Raises:
            MessageProcessingError: If there's an error formatting the messages.
        """
        formatter = JsonFormatter()
        return formatter.format(self.messages)
    
    def format_csv(self) -> str:
        """Format messages as CSV.
        
        Returns:
            str: Messages formatted as CSV.
            
        Raises:
            MessageProcessingError: If there's an error formatting the messages.
        """
        formatter = CsvFormatter()
        return formatter.format(self.messages)
    
    def format_markdown(self) -> str:
        """Format messages as Markdown.
        
        Returns:
            str: Messages formatted as Markdown.
            
        Raises:
            MessageProcessingError: If there's an error formatting the messages.
        """
        formatter = MarkdownFormatter()
        return formatter.format(self.messages)
