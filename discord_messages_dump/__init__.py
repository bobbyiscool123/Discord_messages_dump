"""Discord Messages Dump - A tool to download and save message history from Discord channels."""

__version__ = "0.1.0"

from discord_messages_dump.api import DiscordApiClient
from discord_messages_dump.message_processor import MessageProcessor
from discord_messages_dump.file_handler import FileHandler
from discord_messages_dump.cli import main as cli_main

__all__ = ["DiscordApiClient", "MessageProcessor", "FileHandler", "cli_main"]
