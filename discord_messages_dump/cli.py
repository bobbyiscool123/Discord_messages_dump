"""Command-line interface for Discord Messages Dump.

This module provides a command-line interface for the Discord Messages Dump
package using Click. It allows users to fetch messages from Discord channels
and save them in various formats.
"""

import os
import sys
import logging
from typing import Optional, List, Dict, Any

import click
from dotenv import load_dotenv
from tqdm import tqdm

from discord_messages_dump.api import DiscordApiClient
from discord_messages_dump.message_processor import MessageProcessor
from discord_messages_dump.file_handler import FileHandler


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(module)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("discord-dump")


def setup_logging(verbose: bool) -> None:
    """
    Set up logging based on verbosity level.

    Args:
        verbose (bool): Whether to enable verbose logging.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    else:
        logger.setLevel(logging.INFO)


def get_messages_with_progress(
    client: DiscordApiClient,
    channel_id: str,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Fetch messages from Discord with a progress bar.

    Args:
        client (DiscordApiClient): The Discord API client.
        channel_id (str): The ID of the channel to fetch messages from.
        limit (int, optional): Maximum number of messages to retrieve. Defaults to 100.

    Returns:
        List[Dict[str, Any]]: A list of message objects as dictionaries.
    """
    messages: List[Dict[str, Any]] = []
    before: Optional[str] = None

    # Create a progress bar
    with tqdm(total=limit, desc="Fetching messages", unit="msg",
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]") as pbar:

        while len(messages) < limit:
            # Calculate how many messages to fetch in this batch
            batch_size = min(100, limit - len(messages))

            # Fetch messages
            logger.debug(f"Fetching batch of {batch_size} messages before ID: {before}")
            batch = client.get_messages(channel_id, limit=batch_size, before=before)

            # If no messages were returned, we've reached the end
            if not batch:
                logger.debug("No more messages to fetch")
                break

            # Add messages to our list
            messages.extend(batch)

            # Update progress bar
            pbar.update(len(batch))

            # Update 'before' for pagination
            before = batch[-1]["id"]

            # Log progress
            logger.debug(f"Fetched {len(messages)}/{limit} messages")

    # Trim to limit if we fetched more than requested
    return messages[:limit]


@click.group()
def cli():
    """Discord Messages Dump - Download and save message history from Discord channels."""
    pass


@cli.command()
def install_completion():
    """Install command completion for bash/zsh."""
    from discord_messages_dump.completion import install_completion
    install_completion()


@cli.command()
@click.option(
    "--token",
    help="Discord user token for authentication. Can also be set via DISCORD_TOKEN environment variable."
)
@click.option(
    "--channel-id",
    help="ID of the Discord channel to fetch messages from. Can also be set via DISCORD_CHANNEL_ID environment variable."
)
@click.option(
    "--format",
    "format_type",
    type=click.Choice(["text", "json", "csv", "markdown"], case_sensitive=False),
    default="text",
    help="Output format for the messages. Default: text"
)
@click.option(
    "--output-file",
    help="Path to save the messages to. If not provided and --no-gui is not set, a file dialog will open."
)
@click.option(
    "--limit",
    type=int,
    default=100,
    help="Maximum number of messages to retrieve. Default: 100"
)
@click.option(
    "--no-gui",
    is_flag=True,
    help="Disable GUI file dialog for selecting output file."
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging."
)
def dump(
    token: Optional[str],
    channel_id: Optional[str],
    format_type: str,
    output_file: Optional[str],
    limit: int,
    no_gui: bool,
    verbose: bool
) -> None:
    """
    Fetch messages from a Discord channel and save them to a file.

    If --token or --channel-id are not provided, the tool will attempt to load them
    from environment variables DISCORD_TOKEN and DISCORD_CHANNEL_ID respectively.

    If --output-file is not provided and --no-gui is not set, a file dialog will open
    to select the output file location.
    """
    # Set up logging based on verbosity
    setup_logging(verbose)

    # Load environment variables
    load_dotenv()

    # Get token from option or environment
    token = token or os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("Discord token not provided. Use --token option or set DISCORD_TOKEN environment variable.")
        sys.exit(1)

    # Get channel ID from option or environment
    channel_id = channel_id or os.getenv("DISCORD_CHANNEL_ID")
    if not channel_id:
        logger.error("Channel ID not provided. Use --channel-id option or set DISCORD_CHANNEL_ID environment variable.")
        sys.exit(1)

    # Create API client
    logger.debug("Initializing Discord API client")
    client = DiscordApiClient(token)

    try:
        # Fetch messages with progress bar
        logger.info(f"Fetching up to {limit} messages from channel {channel_id}")
        messages = get_messages_with_progress(client, channel_id, limit)

        if not messages:
            logger.error("No messages found in the specified channel.")
            sys.exit(1)

        logger.info(f"Successfully fetched {len(messages)} messages")

        # Process messages
        logger.debug(f"Processing messages in {format_type} format")
        processor = MessageProcessor(messages)

        # Format messages based on the specified format type
        if format_type.lower() == "json":
            formatted_content = processor.format_json()
        elif format_type.lower() == "csv":
            formatted_content = processor.format_csv()
        elif format_type.lower() == "markdown":
            formatted_content = processor.format_markdown()
        else:  # Default to text format
            formatted_content = processor.format_text()

        # Initialize file handler
        file_handler = FileHandler()

        # Determine output file path
        if not output_file and not no_gui:
            # Get default filename based on format type
            _, _, default_filename = file_handler.get_file_type_info(format_type)

            logger.info("Opening file dialog to select output location")
            output_file = file_handler.open_save_dialog(default_filename, format_type)

            if not output_file:
                logger.error("No output file selected. Exiting.")
                sys.exit(1)
        elif not output_file and no_gui:
            logger.error("No output file specified and GUI is disabled. Use --output-file option.")
            sys.exit(1)

        # Save formatted content to file
        logger.debug(f"Saving content to {output_file}")
        if file_handler.save_content(formatted_content, output_file):
            logger.info(f"All messages saved to: {output_file} in {format_type} format")
        else:
            logger.error(f"Failed to save messages to: {output_file}")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if verbose:
            logger.exception("Detailed error information:")
        sys.exit(1)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
