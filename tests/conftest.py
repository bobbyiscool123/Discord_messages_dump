"""Pytest fixtures for Discord Messages Dump tests."""

import os
import json
import tempfile
from typing import Dict, List, Any, Generator, Optional
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_discord_response() -> Dict[str, Any]:
    """
    Returns a mock Discord API response with sample messages.
    
    Returns:
        Dict[str, Any]: A dictionary containing mock Discord API response data.
    """
    return {
        "status_code": 200,
        "headers": {
            "content-type": "application/json",
            "X-RateLimit-Limit": "5",
            "X-RateLimit-Remaining": "4",
            "X-RateLimit-Reset-After": "1.0"
        },
        "json": [
            {
                "id": "123456789012345678",
                "channel_id": "987654321098765432",
                "author": {
                    "id": "111111111111111111",
                    "username": "TestUser1",
                    "discriminator": "1234",
                    "avatar": "abcdef123456"
                },
                "content": "This is a test message 1",
                "timestamp": "2023-01-01T12:00:00.000000+00:00",
                "edited_timestamp": None,
                "attachments": [],
                "embeds": [],
                "mentions": [],
                "mention_roles": [],
                "pinned": False,
                "mention_everyone": False,
                "tts": False,
                "type": 0
            },
            {
                "id": "123456789012345679",
                "channel_id": "987654321098765432",
                "author": {
                    "id": "222222222222222222",
                    "username": "TestUser2",
                    "discriminator": "5678",
                    "avatar": "ghijkl789012"
                },
                "content": "This is a test message 2",
                "timestamp": "2023-01-01T12:01:00.000000+00:00",
                "edited_timestamp": None,
                "attachments": [],
                "embeds": [],
                "mentions": [],
                "mention_roles": [],
                "pinned": False,
                "mention_everyone": False,
                "tts": False,
                "type": 0
            }
        ]
    }


@pytest.fixture
def sample_messages() -> List[Dict[str, Any]]:
    """
    Returns a list of sample Discord messages for testing.
    
    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing sample message data.
    """
    return [
        {
            "id": "123456789012345678",
            "channel_id": "987654321098765432",
            "author": {
                "id": "111111111111111111",
                "username": "TestUser1",
                "discriminator": "1234",
                "avatar": "abcdef123456"
            },
            "content": "This is a test message 1",
            "timestamp": "2023-01-01T12:00:00.000000+00:00",
            "edited_timestamp": None,
            "attachments": [],
            "embeds": [],
            "mentions": [],
            "mention_roles": [],
            "pinned": False,
            "mention_everyone": False,
            "tts": False,
            "type": 0
        },
        {
            "id": "123456789012345679",
            "channel_id": "987654321098765432",
            "author": {
                "id": "222222222222222222",
                "username": "TestUser2",
                "discriminator": "5678",
                "avatar": "ghijkl789012"
            },
            "content": "This is a test message 2",
            "timestamp": "2023-01-01T12:01:00.000000+00:00",
            "edited_timestamp": None,
            "attachments": [],
            "embeds": [],
            "mentions": [],
            "mention_roles": [],
            "pinned": False,
            "mention_everyone": False,
            "tts": False,
            "type": 0
        },
        {
            "id": "123456789012345680",
            "channel_id": "987654321098765432",
            "author": {
                "id": "333333333333333333",
                "username": "TestUser3",
                "discriminator": "9012",
                "avatar": "mnopqr345678"
            },
            "content": "This is a test message 3 with an attachment",
            "timestamp": "2023-01-01T12:02:00.000000+00:00",
            "edited_timestamp": "2023-01-01T12:03:00.000000+00:00",
            "attachments": [
                {
                    "id": "987654321012345678",
                    "filename": "test_file.txt",
                    "size": 1234,
                    "url": "https://cdn.discordapp.com/attachments/987654321098765432/987654321012345678/test_file.txt",
                    "proxy_url": "https://media.discordapp.net/attachments/987654321098765432/987654321012345678/test_file.txt"
                }
            ],
            "embeds": [],
            "mentions": [],
            "mention_roles": [],
            "pinned": True,
            "mention_everyone": False,
            "tts": False,
            "type": 0
        }
    ]


@pytest.fixture
def temp_output_file() -> Generator[str, None, None]:
    """
    Creates a temporary file for testing output functionality.
    
    Yields:
        str: The path to the temporary file.
    """
    # Create a temporary file
    fd, path = tempfile.mkstemp()
    os.close(fd)
    
    # Yield the path to the test
    yield path
    
    # Clean up the file after the test
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def mock_requests_get(monkeypatch, mock_discord_response):
    """
    Mocks the requests.get function to return a predefined response.
    
    Args:
        monkeypatch: Pytest's monkeypatch fixture.
        mock_discord_response: The mock_discord_response fixture.
        
    Returns:
        MagicMock: A mock object for requests.get.
    """
    mock_get = MagicMock()
    mock_response = MagicMock()
    
    # Set up the mock response
    mock_response.status_code = mock_discord_response["status_code"]
    mock_response.headers = mock_discord_response["headers"]
    mock_response.json.return_value = mock_discord_response["json"]
    
    # Set up the mock get function
    mock_get.return_value = mock_response
    
    # Apply the mock to requests.get
    monkeypatch.setattr("requests.get", mock_get)
    
    return mock_get


@pytest.fixture
def mock_env_vars(monkeypatch):
    """
    Sets up mock environment variables for testing.
    
    Args:
        monkeypatch: Pytest's monkeypatch fixture.
    """
    monkeypatch.setenv("DISCORD_TOKEN", "mock_token")
    monkeypatch.setenv("DISCORD_CHANNEL_ID", "123456789012345678")
    monkeypatch.setenv("FORMAT", "json")
    monkeypatch.setenv("MESSAGE_LIMIT", "50")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")


@pytest.fixture
def mock_file_dialog(monkeypatch):
    """
    Mocks the file dialog to return a predefined path.
    
    Args:
        monkeypatch: Pytest's monkeypatch fixture.
        
    Returns:
        MagicMock: A mock object for the file dialog.
    """
    mock_dialog = MagicMock()
    mock_dialog.return_value = "test_output.txt"
    
    # Apply the mock to the appropriate function
    monkeypatch.setattr("tkinter.filedialog.asksaveasfilename", mock_dialog)
    
    return mock_dialog
