"""Integration tests for Discord Messages Dump."""

import os
import json
import pytest
from unittest.mock import patch, MagicMock

from discord_messages_dump.api import DiscordApiClient
from discord_messages_dump.message_processor import MessageProcessor
from discord_messages_dump.file_handler import FileHandler
from discord_messages_dump.cli import dump


class TestEndToEnd:
    """End-to-end integration tests for Discord Messages Dump."""
    
    @patch("discord_messages_dump.api.DiscordApiClient.get_messages")
    @patch("discord_messages_dump.file_handler.FileHandler.save_content")
    def test_end_to_end_text_format(self, mock_save_content, mock_get_messages, sample_messages, temp_output_file):
        """Test end-to-end flow with text format."""
        # Set up mocks
        mock_get_messages.return_value = sample_messages
        mock_save_content.return_value = True
        
        # Create instances
        client = DiscordApiClient(token="test_token")
        processor = MessageProcessor(sample_messages)
        file_handler = FileHandler()
        
        # Execute the flow
        messages = client.get_messages("123456789")
        formatted_content = processor.format_text()
        result = file_handler.save_content(formatted_content, temp_output_file)
        
        # Check that the mocks were called correctly
        mock_get_messages.assert_called_once_with("123456789", limit=100, before=None, after=None)
        mock_save_content.assert_called_once()
        
        # Check that the result is True
        assert result is True
    
    @patch("discord_messages_dump.api.DiscordApiClient.get_messages")
    @patch("discord_messages_dump.file_handler.FileHandler.save_content")
    def test_end_to_end_json_format(self, mock_save_content, mock_get_messages, sample_messages, temp_output_file):
        """Test end-to-end flow with JSON format."""
        # Set up mocks
        mock_get_messages.return_value = sample_messages
        mock_save_content.return_value = True
        
        # Create instances
        client = DiscordApiClient(token="test_token")
        processor = MessageProcessor(sample_messages)
        file_handler = FileHandler()
        
        # Execute the flow
        messages = client.get_messages("123456789")
        formatted_content = processor.format_json()
        result = file_handler.save_content(formatted_content, temp_output_file)
        
        # Check that the mocks were called correctly
        mock_get_messages.assert_called_once_with("123456789", limit=100, before=None, after=None)
        mock_save_content.assert_called_once()
        
        # Check that the result is True
        assert result is True
        
        # Check that the content is valid JSON
        args, kwargs = mock_save_content.call_args
        content = args[0]
        parsed_json = json.loads(content)
        assert isinstance(parsed_json, dict)
        assert "messages" in parsed_json
    
    @patch("click.echo")
    @patch("discord_messages_dump.api.DiscordApiClient.get_messages")
    @patch("discord_messages_dump.file_handler.FileHandler.save_content")
    def test_cli_dump_command(self, mock_save_content, mock_get_messages, mock_echo, sample_messages, temp_output_file):
        """Test the CLI dump command."""
        # Set up mocks
        mock_get_messages.return_value = sample_messages
        mock_save_content.return_value = True
        
        # Execute the command
        result = dump.callback(
            token="test_token",
            channel_id="123456789",
            format_type="json",
            output_file=temp_output_file,
            limit=10,
            no_gui=True,
            verbose=False
        )
        
        # Check that the mocks were called correctly
        mock_get_messages.assert_called_once()
        mock_save_content.assert_called_once()
        
        # Check that the success message was printed
        mock_echo.assert_called_with(f"Messages saved to {temp_output_file}")
    
    @patch("click.echo")
    @patch("discord_messages_dump.api.DiscordApiClient.get_messages")
    def test_cli_dump_command_no_messages(self, mock_get_messages, mock_echo):
        """Test the CLI dump command when no messages are found."""
        # Set up mocks
        mock_get_messages.return_value = []
        
        # Execute the command
        with pytest.raises(SystemExit) as excinfo:
            dump.callback(
                token="test_token",
                channel_id="123456789",
                format_type="json",
                output_file="test_output.json",
                limit=10,
                no_gui=True,
                verbose=False
            )
        
        # Check that the error message was printed
        mock_echo.assert_called_with("No messages found in the specified channel.")
        
        # Check that the exit code is 1
        assert excinfo.value.code == 1
    
    @patch("click.echo")
    @patch("discord_messages_dump.api.DiscordApiClient.get_messages")
    @patch("discord_messages_dump.file_handler.FileHandler.save_content")
    def test_cli_dump_command_save_error(self, mock_save_content, mock_get_messages, mock_echo, sample_messages):
        """Test the CLI dump command when there is an error saving the file."""
        # Set up mocks
        mock_get_messages.return_value = sample_messages
        mock_save_content.return_value = False
        
        # Execute the command
        with pytest.raises(SystemExit) as excinfo:
            dump.callback(
                token="test_token",
                channel_id="123456789",
                format_type="json",
                output_file="test_output.json",
                limit=10,
                no_gui=True,
                verbose=False
            )
        
        # Check that the error message was printed
        mock_echo.assert_called_with("Failed to save messages to: test_output.json")
        
        # Check that the exit code is 1
        assert excinfo.value.code == 1
