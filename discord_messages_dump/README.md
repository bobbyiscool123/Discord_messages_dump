# Discord Messages Dump API

This package provides a clean, type-annotated API for interacting with Discord's API to fetch messages from channels and process them into various output formats.

## Features

- Type-annotated API for better IDE support and code quality
- Proper rate limit handling with exponential backoff
- Detailed error handling and reporting
- Comprehensive docstrings in Google format
- Multiple output formats (text, JSON, CSV, Markdown)
- Extensible formatter architecture

## Usage

### Fetching Messages

```python
from discord_messages_dump.api import DiscordApiClient

# Initialize the client with your Discord token
client = DiscordApiClient("YOUR_DISCORD_TOKEN")

# Fetch messages from a channel
messages = client.get_messages("CHANNEL_ID", limit=100)

# Process the messages
for message in messages:
    print(f"[{message['timestamp']}] {message['author']['username']}: {message['content']}")
```

### Formatting Messages

```python
from discord_messages_dump.api import DiscordApiClient
from discord_messages_dump.message_processor import MessageProcessor

# Initialize the client and fetch messages
client = DiscordApiClient("YOUR_DISCORD_TOKEN")
messages = client.get_messages("CHANNEL_ID", limit=100)

# Create a message processor
processor = MessageProcessor(messages)

# Format messages in different formats
text_output = processor.format_text()
json_output = processor.format_json()
csv_output = processor.format_csv()
markdown_output = processor.format_markdown()

# Save the formatted output to files
with open("messages.txt", "w", encoding="utf-8") as f:
    f.write(text_output)

with open("messages.json", "w", encoding="utf-8") as f:
    f.write(json_output)

with open("messages.csv", "w", encoding="utf-8") as f:
    f.write(csv_output)

with open("messages.md", "w", encoding="utf-8") as f:
    f.write(markdown_output)
```

## API Reference

### DiscordApiClient

The main class for interacting with Discord's API.

#### `__init__(self, token: str) -> None`

Initialize the Discord API client with a user token.

**Parameters:**
- `token (str)`: The Discord user token for authentication.

#### `get_messages(self, channel_id: str, limit: int = 100, before: Optional[str] = None) -> List[Dict[str, Any]]`

Fetch messages from a Discord channel.

**Parameters:**
- `channel_id (str)`: The ID of the Discord channel to fetch messages from.
- `limit (int, optional)`: Maximum number of messages to retrieve per request. Defaults to 100.
- `before (Optional[str], optional)`: Message ID to fetch messages before. Used for pagination. Defaults to None.

**Returns:**
- `List[Dict[str, Any]]`: A list of message objects as dictionaries.

**Raises:**
- `requests.exceptions.RequestException`: If there's an error with the HTTP request.
- `ValueError`: If the channel ID is invalid or the token is incorrect.

#### `_handle_rate_limits(self, response: requests.Response) -> None`

Handle Discord API rate limits.

**Parameters:**
- `response (requests.Response)`: The HTTP response from the Discord API.

**Returns:**
- `None`

### MessageProcessor

The main class for processing and formatting Discord message data.

#### `__init__(self, messages: List[Dict[str, Any]]) -> None`

Initialize the message processor with raw message data.

**Parameters:**
- `messages (List[Dict[str, Any]])`: List of Discord message objects.

**Raises:**
- `ValueError`: If messages is not a list or is empty.

#### `format_text(self) -> str`

Format messages as plain text.

**Returns:**
- `str`: Messages formatted as plain text.

**Raises:**
- `MessageProcessingError`: If there's an error formatting the messages.

#### `format_json(self) -> str`

Format messages as JSON.

**Returns:**
- `str`: Messages formatted as JSON.

**Raises:**
- `MessageProcessingError`: If there's an error formatting the messages.

#### `format_csv(self) -> str`

Format messages as CSV.

**Returns:**
- `str`: Messages formatted as CSV.

**Raises:**
- `MessageProcessingError`: If there's an error formatting the messages.

#### `format_markdown(self) -> str`

Format messages as Markdown.

**Returns:**
- `str`: Messages formatted as Markdown.

**Raises:**
- `MessageProcessingError`: If there's an error formatting the messages.
