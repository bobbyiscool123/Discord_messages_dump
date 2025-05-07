"""Tests for the message processor module."""

import json
import unittest
from typing import Any, Dict, List

from discord_messages_dump.message_processor import (
    CsvFormatter,
    JsonFormatter,
    MarkdownFormatter,
    MessageProcessor,
    MessageProcessingError,
    TextFormatter
)


class TestMessageProcessor(unittest.TestCase):
    """Test cases for the MessageProcessor class."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_messages = [
            {
                "id": "123456789012345678",
                "channel_id": "987654321098765432",
                "author": {
                    "id": "111222333444555666",
                    "username": "test_user1",
                    "discriminator": "1234",
                    "avatar": "abcdef0123456789"
                },
                "content": "This is a test message",
                "timestamp": "2023-01-01T12:00:00.000000+00:00",
                "edited_timestamp": None,
                "attachments": []
            },
            {
                "id": "876543210987654321",
                "channel_id": "987654321098765432",
                "author": {
                    "id": "666555444333222111",
                    "username": "test_user2",
                    "discriminator": "4321",
                    "avatar": "9876543210abcdef"
                },
                "content": "This is another test message",
                "timestamp": "2023-01-01T12:05:00.000000+00:00",
                "edited_timestamp": None,
                "attachments": []
            }
        ]
        self.processor = MessageProcessor(self.sample_messages)

    def test_init_with_invalid_messages(self):
        """Test initialization with invalid message data."""
        with self.assertRaises(ValueError):
            MessageProcessor("not a list")

    def test_format_text(self):
        """Test formatting messages as plain text."""
        formatted = self.processor.format_text()
        self.assertIsInstance(formatted, str)
        self.assertIn("test_user1", formatted)
        self.assertIn("This is a test message", formatted)
        self.assertIn("2023-01-01T12:00:00.000000+00:00", formatted)
        self.assertIn("test_user2", formatted)
        self.assertIn("This is another test message", formatted)

    def test_format_json(self):
        """Test formatting messages as JSON."""
        formatted = self.processor.format_json()
        self.assertIsInstance(formatted, str)
        # Verify it's valid JSON
        parsed = json.loads(formatted)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0]["id"], "123456789012345678")
        self.assertEqual(parsed[1]["id"], "876543210987654321")

    def test_format_csv(self):
        """Test formatting messages as CSV."""
        formatted = self.processor.format_csv()
        self.assertIsInstance(formatted, str)
        lines = formatted.strip().split("\n")
        self.assertEqual(len(lines), 3)  # Header + 2 messages
        self.assertIn("timestamp,author_id,author_username,content", lines[0])
        self.assertIn("test_user1", lines[1])
        self.assertIn("test_user2", lines[2])

    def test_format_markdown(self):
        """Test formatting messages as Markdown."""
        formatted = self.processor.format_markdown()
        self.assertIsInstance(formatted, str)
        self.assertIn("# Discord Messages", formatted)
        self.assertIn("## Channel:", formatted)
        self.assertIn("### test_user1", formatted)
        self.assertIn("### test_user2", formatted)


class TestTextFormatter(unittest.TestCase):
    """Test cases for the TextFormatter class."""

    def test_format_with_malformed_data(self):
        """Test formatting with malformed message data."""
        formatter = TextFormatter()
        malformed_messages = [
            {},  # Empty message
            {"author": {}},  # Missing username
            {"timestamp": "2023-01-01", "content": "No author"}  # Missing author
        ]
        formatted = formatter.format(malformed_messages)
        self.assertIn("unknown_user", formatted)
        self.assertIn("unknown_time", formatted)


class TestJsonFormatter(unittest.TestCase):
    """Test cases for the JsonFormatter class."""

    def test_format_with_malformed_data(self):
        """Test formatting with malformed message data."""
        formatter = JsonFormatter()
        # Create a message with a non-serializable object
        class NonSerializable:
            pass
        
        malformed_messages = [{"non_serializable": NonSerializable()}]
        
        with self.assertRaises(MessageProcessingError):
            formatter.format(malformed_messages)


class TestCsvFormatter(unittest.TestCase):
    """Test cases for the CsvFormatter class."""

    def test_format_with_malformed_data(self):
        """Test formatting with malformed message data."""
        formatter = CsvFormatter()
        malformed_messages = [
            {},  # Empty message
            {"author": {}},  # Missing username
            {"timestamp": "2023-01-01", "content": "No author"}  # Missing author
        ]
        formatted = formatter.format(malformed_messages)
        lines = formatted.strip().split("\n")
        self.assertEqual(len(lines), 4)  # Header + 3 messages


class TestMarkdownFormatter(unittest.TestCase):
    """Test cases for the MarkdownFormatter class."""

    def test_format_with_malformed_data(self):
        """Test formatting with malformed message data."""
        formatter = MarkdownFormatter()
        malformed_messages = [
            {},  # Empty message
            {"author": {}},  # Missing username
            {"timestamp": "2023-01-01", "content": "No author"}  # Missing author
        ]
        formatted = formatter.format(malformed_messages)
        self.assertIn("unknown_user", formatted)
        self.assertIn("unknown_time", formatted)


if __name__ == "__main__":
    unittest.main()
