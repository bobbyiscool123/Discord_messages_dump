"""Tests for the CLI module."""

import os
import unittest
from unittest.mock import patch, MagicMock

from click.testing import CliRunner

from discord_messages_dump.cli import cli


class TestCli(unittest.TestCase):
    """Test cases for the CLI module."""

    def setUp(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.mock_messages = [
            {
                "id": "123456789",
                "content": "Test message 1",
                "author": {"username": "testuser1"},
                "timestamp": "2023-01-01T12:00:00.000Z"
            },
            {
                "id": "123456790",
                "content": "Test message 2",
                "author": {"username": "testuser2"},
                "timestamp": "2023-01-01T12:01:00.000Z"
            }
        ]

    @patch('discord_messages_dump.cli.DiscordApiClient')
    @patch('discord_messages_dump.cli.MessageProcessor')
    @patch('discord_messages_dump.cli.FileHandler')
    def test_dump_command_with_all_options(self, mock_file_handler, mock_processor, mock_client):
        """Test the dump command with all options provided."""
        # Set up mocks
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_messages.return_value = self.mock_messages
        
        mock_processor_instance = mock_processor.return_value
        mock_processor_instance.format_text.return_value = "Formatted text"
        
        mock_file_handler_instance = mock_file_handler.return_value
        mock_file_handler_instance.save_content.return_value = True
        
        # Run the command
        result = self.runner.invoke(cli, [
            'dump',
            '--token', 'test_token',
            '--channel-id', 'test_channel',
            '--format', 'text',
            '--output-file', 'test_output.txt',
            '--limit', '10',
            '--no-gui'
        ])
        
        # Check the result
        self.assertEqual(result.exit_code, 0)
        
        # Verify the mocks were called correctly
        mock_client.assert_called_once_with('test_token')
        mock_client_instance.get_messages.assert_called()
        mock_processor.assert_called_once_with(self.mock_messages)
        mock_processor_instance.format_text.assert_called_once()
        mock_file_handler_instance.save_content.assert_called_once_with(
            "Formatted text", 'test_output.txt'
        )

    @patch('discord_messages_dump.cli.DiscordApiClient')
    @patch('discord_messages_dump.cli.MessageProcessor')
    @patch('discord_messages_dump.cli.FileHandler')
    def test_dump_command_with_json_format(self, mock_file_handler, mock_processor, mock_client):
        """Test the dump command with JSON format."""
        # Set up mocks
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_messages.return_value = self.mock_messages
        
        mock_processor_instance = mock_processor.return_value
        mock_processor_instance.format_json.return_value = '{"messages": []}'
        
        mock_file_handler_instance = mock_file_handler.return_value
        mock_file_handler_instance.save_content.return_value = True
        
        # Run the command
        result = self.runner.invoke(cli, [
            'dump',
            '--token', 'test_token',
            '--channel-id', 'test_channel',
            '--format', 'json',
            '--output-file', 'test_output.json',
            '--no-gui'
        ])
        
        # Check the result
        self.assertEqual(result.exit_code, 0)
        
        # Verify the format_json method was called
        mock_processor_instance.format_json.assert_called_once()

    @patch('discord_messages_dump.cli.DiscordApiClient')
    def test_dump_command_with_no_messages(self, mock_client):
        """Test the dump command when no messages are found."""
        # Set up mocks
        mock_client_instance = mock_client.return_value
        mock_client_instance.get_messages.return_value = []
        
        # Run the command
        result = self.runner.invoke(cli, [
            'dump',
            '--token', 'test_token',
            '--channel-id', 'test_channel',
            '--output-file', 'test_output.txt',
            '--no-gui'
        ])
        
        # Check the result
        self.assertEqual(result.exit_code, 1)
        self.assertIn("No messages found", result.output)

    def test_dump_command_without_token(self):
        """Test the dump command without providing a token."""
        # Run the command without token
        result = self.runner.invoke(cli, [
            'dump',
            '--channel-id', 'test_channel',
            '--output-file', 'test_output.txt',
            '--no-gui'
        ])
        
        # Check the result
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Discord token not provided", result.output)

    def test_dump_command_without_channel_id(self):
        """Test the dump command without providing a channel ID."""
        # Run the command without channel ID
        result = self.runner.invoke(cli, [
            'dump',
            '--token', 'test_token',
            '--output-file', 'test_output.txt',
            '--no-gui'
        ])
        
        # Check the result
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Channel ID not provided", result.output)


if __name__ == '__main__':
    unittest.main()
