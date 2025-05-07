"""Tests for the Discord API Client."""

import pytest
import json
from unittest.mock import MagicMock, patch

from discord_messages_dump.api import DiscordApiClient
from discord_messages_dump.exceptions import (
    DiscordApiError,
    RateLimitError,
    AuthenticationError,
    ChannelNotFoundError
)


class TestDiscordApiClient:
    """Test cases for the DiscordApiClient class."""
    
    def test_init(self):
        """Test initialization of the DiscordApiClient."""
        # Test with token
        client = DiscordApiClient(token="test_token")
        assert client.token == "test_token"
        assert client.base_url == "https://discord.com/api/v9"
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == "test_token"
        
        # Test with custom base URL
        client = DiscordApiClient(token="test_token", base_url="https://custom.api.url")
        assert client.base_url == "https://custom.api.url"
    
    def test_get_messages_success(self, mock_requests_get, mock_discord_response):
        """Test successful retrieval of messages."""
        client = DiscordApiClient(token="test_token")
        messages = client.get_messages("123456789")
        
        # Check that the request was made correctly
        mock_requests_get.assert_called_once()
        args, kwargs = mock_requests_get.call_args
        assert kwargs["url"] == "https://discord.com/api/v9/channels/123456789/messages"
        assert kwargs["headers"]["Authorization"] == "test_token"
        assert kwargs["params"]["limit"] == 100
        
        # Check that the messages were returned correctly
        assert messages == mock_discord_response["json"]
    
    def test_get_messages_with_parameters(self, mock_requests_get):
        """Test retrieval of messages with custom parameters."""
        client = DiscordApiClient(token="test_token")
        client.get_messages("123456789", limit=50, before="987654321", after="123456789")
        
        # Check that the request was made with the correct parameters
        args, kwargs = mock_requests_get.call_args
        assert kwargs["params"]["limit"] == 50
        assert kwargs["params"]["before"] == "987654321"
        assert kwargs["params"]["after"] == "123456789"
    
    @patch("requests.get")
    def test_get_messages_rate_limit(self, mock_get):
        """Test handling of rate limit errors."""
        # Set up mock response for rate limit
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {"X-RateLimit-Reset-After": "2.0"}
        mock_response.json.return_value = {"retry_after": 2.0, "message": "You are being rate limited."}
        mock_get.return_value = mock_response
        
        client = DiscordApiClient(token="test_token")
        
        # Test that a RateLimitError is raised
        with pytest.raises(RateLimitError) as excinfo:
            client.get_messages("123456789")
        
        # Check the error message and retry_after value
        assert "rate limit" in str(excinfo.value).lower()
        assert excinfo.value.retry_after == 2.0
    
    @patch("requests.get")
    def test_get_messages_authentication_error(self, mock_get):
        """Test handling of authentication errors."""
        # Set up mock response for authentication error
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "401: Unauthorized"}
        mock_get.return_value = mock_response
        
        client = DiscordApiClient(token="invalid_token")
        
        # Test that an AuthenticationError is raised
        with pytest.raises(AuthenticationError) as excinfo:
            client.get_messages("123456789")
        
        # Check the error message
        assert "401" in str(excinfo.value)
    
    @patch("requests.get")
    def test_get_messages_channel_not_found(self, mock_get):
        """Test handling of channel not found errors."""
        # Set up mock response for channel not found
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "404: Not Found"}
        mock_get.return_value = mock_response
        
        client = DiscordApiClient(token="test_token")
        
        # Test that a ChannelNotFoundError is raised
        with pytest.raises(ChannelNotFoundError) as excinfo:
            client.get_messages("invalid_channel")
        
        # Check the error message
        assert "invalid_channel" in str(excinfo.value)
    
    @patch("requests.get")
    def test_get_messages_other_error(self, mock_get):
        """Test handling of other API errors."""
        # Set up mock response for other error
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"message": "Internal Server Error"}
        mock_get.return_value = mock_response
        
        client = DiscordApiClient(token="test_token")
        
        # Test that a DiscordApiError is raised
        with pytest.raises(DiscordApiError) as excinfo:
            client.get_messages("123456789")
        
        # Check the error message
        assert "500" in str(excinfo.value)
    
    @patch("time.sleep")
    @patch("requests.get")
    def test_get_messages_retry_on_rate_limit(self, mock_get, mock_sleep):
        """Test automatic retry on rate limit."""
        # Set up mock responses for rate limit and then success
        mock_rate_limit_response = MagicMock()
        mock_rate_limit_response.status_code = 429
        mock_rate_limit_response.headers = {"X-RateLimit-Reset-After": "0.1"}
        mock_rate_limit_response.json.return_value = {"retry_after": 0.1, "message": "You are being rate limited."}
        
        mock_success_response = MagicMock()
        mock_success_response.status_code = 200
        mock_success_response.json.return_value = [{"id": "123", "content": "Test message"}]
        
        # Configure mock to return rate limit response first, then success response
        mock_get.side_effect = [mock_rate_limit_response, mock_success_response]
        
        client = DiscordApiClient(token="test_token", auto_retry=True)
        messages = client.get_messages("123456789")
        
        # Check that sleep was called with the retry_after value
        mock_sleep.assert_called_once_with(0.1)
        
        # Check that get was called twice
        assert mock_get.call_count == 2
        
        # Check that the messages were returned correctly
        assert messages == [{"id": "123", "content": "Test message"}]
