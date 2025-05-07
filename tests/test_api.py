"""Tests for the Discord API Client."""

import os
import unittest
from unittest.mock import patch, MagicMock

from discord_messages_dump.api import DiscordApiClient


class TestDiscordApiClient(unittest.TestCase):
    """Test cases for the DiscordApiClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.token = "test_token"
        self.client = DiscordApiClient(self.token)
        self.channel_id = "123456789012345678"

    def test_init(self):
        """Test initialization of the client."""
        self.assertEqual(self.client.token, self.token)
        self.assertEqual(self.client.base_url, "https://discord.com/api/v9")
        self.assertEqual(self.client.headers["Authorization"], self.token)

    @patch('requests.get')
    def test_get_messages_success(self, mock_get):
        """Test successful message retrieval."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": "1", "content": "Test message 1", "author": {"username": "User1"}, "timestamp": "2023-01-01T00:00:00.000000+00:00"},
            {"id": "2", "content": "Test message 2", "author": {"username": "User2"}, "timestamp": "2023-01-01T00:01:00.000000+00:00"}
        ]
        mock_get.return_value = mock_response

        # Call the method
        result = self.client.get_messages(self.channel_id)

        # Assertions
        mock_get.assert_called_once()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["content"], "Test message 1")
        self.assertEqual(result[1]["content"], "Test message 2")

    @patch('requests.get')
    def test_get_messages_with_pagination(self, mock_get):
        """Test message retrieval with pagination parameter."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # Call the method with before parameter
        self.client.get_messages(self.channel_id, limit=100, before="123456")

        # Check that the URL contains the before parameter
        args = mock_get.call_args[0]
        url = args[0]  # The URL is the first positional argument
        self.assertIn("before=123456", url)

    @patch('requests.get')
    @patch('time.sleep')
    def test_rate_limit_handling(self, mock_sleep, mock_get):
        """Test handling of rate limits."""
        # First response is rate limited, second is successful
        rate_limited_response = MagicMock()
        rate_limited_response.status_code = 429
        rate_limited_response.headers = {"X-RateLimit-Reset-After": "2.0"}

        success_response = MagicMock()
        success_response.status_code = 200
        success_response.json.return_value = []

        mock_get.side_effect = [rate_limited_response, success_response]

        # Call the method
        self.client.get_messages(self.channel_id)

        # Assertions
        self.assertEqual(mock_get.call_count, 2)
        mock_sleep.assert_called_once_with(2.0)

    @patch('requests.get')
    def test_invalid_token(self, mock_get):
        """Test handling of invalid token."""
        # Mock response for invalid token
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        # Call the method and check for exception
        with self.assertRaises(ValueError) as context:
            self.client.get_messages(self.channel_id)

        self.assertIn("Invalid Discord token", str(context.exception))

    @patch('requests.get')
    def test_channel_not_found(self, mock_get):
        """Test handling of invalid channel ID."""
        # Mock response for channel not found
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        # Call the method and check for exception
        with self.assertRaises(ValueError) as context:
            self.client.get_messages(self.channel_id)

        self.assertIn("Channel with ID", str(context.exception))


if __name__ == "__main__":
    unittest.main()
