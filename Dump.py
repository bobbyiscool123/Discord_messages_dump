import os
import sys
import time
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from discord_messages_dump.api import DiscordApiClient
from discord_messages_dump.message_processor import MessageProcessor
from discord_messages_dump.file_handler import FileHandler

load_dotenv()

def fetch_messages(token: str, channel_id: str, format_type: str = "text") -> Optional[str]:
    """
    Fetches all messages from a Discord channel using the user token and returns the formatted content.

    Args:
        token (str): Your Discord user token.
        channel_id (str): The ID of the channel to fetch messages from.
        format_type (str, optional): Format to save messages in. Options: "text", "json", "csv", "markdown". Defaults to "text".

    Returns:
        Optional[str]: The formatted content, or None if an error occurred.
    """
    print("\n" + "="*60)
    print("FETCHING DISCORD MESSAGES")
    print("="*60)
    print(f"Channel ID: {channel_id}")
    print(f"Output format: {format_type}")
    print("="*60)

    try:
        # Create API client
        print("\nInitializing Discord API client...")
        client = DiscordApiClient(token)

        # Initialize variables
        messages: List[Dict[str, Any]] = []
        before: Optional[str] = None
        limit: int = 100
        batch_count: int = 0

        print("\nFetching messages from Discord (this may take a while)...")
        print("Press Ctrl+C to cancel at any time.")

        # Fetch all messages with pagination
        while True:
            try:
                # Get batch of messages
                batch_count += 1
                new_messages = client.get_messages(channel_id, limit, before)

                # If no new messages, we're done
                if not new_messages:
                    print(f"\rCompleted! Total messages fetched: {len(messages)}                ")
                    break

                # Add messages to our collection
                messages.extend(new_messages)

                # Get ID of last message for pagination
                before = new_messages[-1]['id']

                # Update progress message - show messages fetched instead of batch number
                print(f"\rMessages fetched: {len(messages)}                ", end="")

            except KeyboardInterrupt:
                print("\n\nFetching canceled by user.")
                if not messages:
                    print("No messages were fetched. Exiting.")
                    return None
                print(f"Proceeding with {len(messages)} messages that were already fetched.")
                break
            except Exception as e:
                print(f"\nError fetching messages: {str(e)}")
                if not messages:
                    print("No messages were fetched. Exiting.")
                    return None
                print(f"Proceeding with {len(messages)} messages that were already fetched.")
                break

        print("\n\nProcessing messages...")

        # Sort messages by timestamp (oldest first)
        print("Sorting messages by timestamp...")
        messages.sort(key=lambda x: x['timestamp'])

        # Create a message processor
        processor = MessageProcessor(messages)

        # Format messages based on the specified format type
        print(f"Formatting messages as {format_type}...")
        if format_type.lower() == "json":
            formatted_content = processor.format_json()
        elif format_type.lower() == "csv":
            formatted_content = processor.format_csv()
        elif format_type.lower() == "markdown":
            formatted_content = processor.format_markdown()
        else:  # Default to text format
            formatted_content = processor.format_text()

        # Return the formatted content
        return formatted_content

    except KeyboardInterrupt:
        print("\n\nOperation canceled by user.")
        return None
    except Exception as e:
        print("\n" + "="*60)
        print(f"ERROR: {str(e)}")
        print("="*60)
        return None

def save_messages(formatted_content: str, token: str, channel_id: str, format_type: str) -> bool:
    """
    Save formatted messages to a file.

    Args:
        formatted_content (str): The formatted message content.
        token (str): Discord token for authentication.
        channel_id (str): The Discord channel ID.
        format_type (str): The format type.

    Returns:
        bool: True if successful, False otherwise.
    """
    # Get output file path from user
    output_file = get_output_file_path(token, channel_id, format_type)

    if not output_file:
        print("No output file specified. Exiting.")
        return False

    # Save formatted content to file using FileHandler
    print(f"Saving to {output_file}...")
    file_handler = FileHandler()
    if file_handler.save_content(formatted_content, output_file):
        print("\n" + "="*60)
        print(f"SUCCESS: Messages saved to: {output_file}")
        print(f"Format: {format_type}")
        print("="*60)
        return True
    else:
        print("\n" + "="*60)
        print(f"ERROR: Failed to save messages to: {output_file}")
        print("="*60)
        return False

def ensure_saved_messages_dir() -> str:
    """
    Ensure the saved_messages directory exists and is in .gitignore.

    Returns:
        str: Path to the saved_messages directory
    """
    # Create saved_messages directory in the current working directory
    saved_dir = os.path.join(os.getcwd(), "saved_messages")

    # Create the directory if it doesn't exist
    if not os.path.exists(saved_dir):
        try:
            os.makedirs(saved_dir)
            print(f"Created directory: {saved_dir}")
        except Exception as e:
            print(f"Error creating directory: {str(e)}")
            # Try to create in user's home directory as fallback
            try:
                saved_dir = os.path.join(os.path.expanduser("~"), "saved_messages")
                if not os.path.exists(saved_dir):
                    os.makedirs(saved_dir)
                    print(f"Created directory in home folder instead: {saved_dir}")
                return saved_dir
            except Exception as e2:
                print(f"Error creating directory in home folder: {str(e2)}")
                return os.getcwd()  # Last resort, use current directory

    # Check if .gitignore exists
    gitignore_path = os.path.join(os.getcwd(), ".gitignore")

    # Add saved_messages to .gitignore if needed
    try:
        if os.path.exists(gitignore_path):
            # Read existing .gitignore
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()

            # Check if saved_messages is already in .gitignore
            if "saved_messages" not in gitignore_content and "saved_messages/" not in gitignore_content:
                # Append to .gitignore
                with open(gitignore_path, 'a') as f:
                    f.write("\n# Discord messages output directory\nsaved_messages/\n")
                print("Added saved_messages/ to .gitignore")
        else:
            # Create new .gitignore
            with open(gitignore_path, 'w') as f:
                f.write("# Discord messages output directory\nsaved_messages/\n")
            print("Created .gitignore with saved_messages/ entry")
    except Exception as e:
        print(f"Warning: Could not update .gitignore: {str(e)}")

    # Double-check that the directory exists
    if not os.path.exists(saved_dir):
        print(f"Warning: Could not verify saved_messages directory exists at: {saved_dir}")
        print("Will use current directory instead.")
        return os.getcwd()

    print(f"Using saved_messages directory: {saved_dir}")
    return saved_dir

def get_channel_name(token: str, channel_id: str) -> str:
    """
    Get the actual name of a Discord channel.

    Args:
        token (str): Discord token for authentication.
        channel_id (str): The Discord channel ID.

    Returns:
        str: The channel name, or a fallback if it can't be retrieved.
    """
    try:
        # Create API client
        client = DiscordApiClient(token)

        # Get channel info
        channel_info = client.get_channel_info(channel_id)

        # Extract channel name
        if 'name' in channel_info:
            # Sanitize channel name for filename
            channel_name = channel_info['name']
            # Replace any characters that aren't safe for filenames
            channel_name = channel_name.replace('/', '_').replace('\\', '_')
            channel_name = channel_name.replace(':', '_').replace('*', '_')
            channel_name = channel_name.replace('?', '_').replace('"', '_')
            channel_name = channel_name.replace('<', '_').replace('>', '_')
            channel_name = channel_name.replace('|', '_')
            return channel_name
    except Exception as e:
        print(f"Could not get channel name: {str(e)}")

    # Fallback to channel ID if we couldn't get the name
    safe_channel_id = channel_id.replace('/', '_').replace('\\', '_')
    return f"channel-{safe_channel_id}"

def generate_filename(token: str, channel_id: str, format_type: str) -> str:
    """
    Generate a filename using the current date and Discord channel name.

    Args:
        token (str): Discord token for authentication.
        channel_id (str): The Discord channel ID.
        format_type (str): Format type to determine file extension.

    Returns:
        str: The generated filename.
    """
    # Get current date in YYYY-MM-DD format
    current_date = time.strftime("%Y-%m-%d")

    # Get the actual channel name
    channel_name = get_channel_name(token, channel_id)

    # Create filename: YYYY-MM-DD_channel-name.extension
    file_handler = FileHandler()
    extension = file_handler.get_file_extension(format_type)
    filename = f"{current_date}_{channel_name}{extension}"

    return filename

def get_output_file_path(token: str, channel_id: str, format_type: str) -> Optional[str]:
    """
    Get the output file path from the user via multiple-choice selection.

    Args:
        token (str): Discord token for authentication.
        channel_id (str): The Discord channel ID.
        format_type (str): Format type to determine file extension.

    Returns:
        Optional[str]: The selected file path, or None if canceled.
    """
    file_handler = FileHandler()

    # Generate filename using date and channel
    default_filename = generate_filename(token, channel_id, format_type)

    # Ensure saved_messages directory exists and is in .gitignore
    saved_dir = ensure_saved_messages_dir()

    # Get user home directory
    home_dir = os.path.expanduser("~")

    print("\n" + "-"*60)
    print("OUTPUT FILE SELECTION")
    print("-"*60)

    # Present directory options
    print("Select where to save the output file:")
    print(f"1. saved_messages directory: {saved_dir} (recommended)")
    print(f"2. Home directory: {home_dir}")
    print("3. Current directory: " + os.getcwd())
    print("4. Custom directory")
    print("Or press Enter for option 1, or type 'cancel' to exit")

    # Get user choice
    while True:
        choice = input("\nEnter your choice (1-4, default: 1): ").strip()

        # Default to option 1 if empty
        if not choice:
            choice = "1"

        # Check if user wants to cancel
        if choice.lower() == 'cancel':
            print("Operation canceled.")
            return None

        # Process the choice
        if choice == '1':
            output_dir = saved_dir
            break
        elif choice == '2':
            output_dir = home_dir
            break
        elif choice == '3':
            output_dir = os.getcwd()
            break
        elif choice == '4':
            # Ask for custom directory
            print("\nEnter the custom directory path:")
            custom_dir = input("> ").strip()

            if custom_dir.lower() == 'cancel':
                print("Operation canceled.")
                return None

            # Expand user directory if needed
            output_dir = os.path.expanduser(custom_dir)

            # Create directory if it doesn't exist
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir)
                    print(f"Created directory: {output_dir}")
                    break
                except Exception as e:
                    print(f"Error creating directory: {str(e)}")
                    print("Please enter a valid directory path or choose another option.")
                    continue
            else:
                break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    # Show the default filename (which is now based on date and channel)
    print(f"\nDefault filename: {default_filename}")
    print("Press Enter to use this filename or type a custom filename")
    print("Or type 'cancel' to exit")
    filename = input("> ").strip()

    # Check if user wants to cancel
    if filename.lower() == 'cancel':
        print("Operation canceled.")
        return None

    # Use default if empty
    if not filename:
        filename = default_filename

    # Add extension if needed
    extension = file_handler.get_file_extension(format_type)
    if not filename.endswith(extension):
        filename += extension

    # Construct full path
    file_path = os.path.join(output_dir, filename)

    # Confirm the file path
    print(f"\nOutput will be saved to: {file_path}")
    print("Is this correct? (y/n, default: y)")
    confirm = input("> ").strip().lower()

    if confirm in ['', 'y', 'yes']:
        return file_path
    else:
        print("Let's try again.")
        return get_output_file_path(channel_id, format_type)  # Recursive call to try again

def select_format() -> str:
    """
    Ask the user to select the output format via console input.

    Returns:
        str: Selected format type ("text", "json", "csv", or "markdown").
    """
    formats = {
        "1": "text",
        "2": "json",
        "3": "csv",
        "4": "markdown"
    }

    print("\n" + "-"*60)
    print("OUTPUT FORMAT SELECTION")
    print("-"*60)
    print("Select the format for saving Discord messages:")
    print("1. Plain Text (.txt) - Simple readable format")
    print("2. JSON (.json) - Structured data format for programmatic use")
    print("3. CSV (.csv) - Spreadsheet compatible format")
    print("4. Markdown (.md) - Formatted text with headers and styling")
    print("Or type 'cancel' to exit")

    while True:
        choice = input("\nEnter your choice (1-4, default: 1): ").strip()

        # Check if user wants to cancel
        if choice.lower() == 'cancel':
            print("Operation canceled.")
            sys.exit(0)

        # Default to text format
        if not choice:
            print("Selected format: Plain Text (.txt)")
            return "text"

        if choice in formats:
            format_name = {
                "text": "Plain Text (.txt)",
                "json": "JSON (.json)",
                "csv": "CSV (.csv)",
                "markdown": "Markdown (.md)"
            }[formats[choice]]
            print(f"Selected format: {format_name}")
            return formats[choice]
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    """Main execution block."""
    print("\n" + "="*60)
    print("DISCORD MESSAGES DUMP")
    print("="*60)
    print("This tool allows you to download and save message history from Discord channels.")
    print("="*60)

    # Load values from the environment file
    print("\nChecking environment variables...")

    # Force reload of .env file to ensure we have the latest values
    from dotenv import load_dotenv
    load_dotenv(override=True)

    # Get environment variables
    TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID: Optional[str] = os.getenv("DISCORD_CHANNEL_ID")

    # Check if we found the environment variables
    if TOKEN and CHANNEL_ID:
        print("Found environment variables in .env file.")

    # Check if environment variables are set and valid
    env_vars_missing = []

    # Check TOKEN - it should exist and not be a placeholder
    if not TOKEN:
        env_vars_missing.append("DISCORD_TOKEN")
    elif TOKEN.strip('"\'') == "YOUR_DISCORD_TOKEN":
        env_vars_missing.append("DISCORD_TOKEN")

    # Check CHANNEL_ID - it should exist and not be a placeholder
    if not CHANNEL_ID:
        env_vars_missing.append("DISCORD_CHANNEL_ID")
    elif CHANNEL_ID.strip('"\'') == "YOUR_DISCORD_CHANNEL_ID":
        env_vars_missing.append("DISCORD_CHANNEL_ID")

    # If any environment variables are missing or invalid, prompt the user
    if env_vars_missing:
        print("\n" + "="*60)
        print("MISSING OR INVALID ENVIRONMENT VARIABLES")
        print("="*60)
        print("The following environment variables are not set or contain default values:")
        for var in env_vars_missing:
            print(f"- {var}")

        print("\nYou have the following options:")
        print("1. Edit the .env file and restart the application")
        print("2. Enter the values directly in the terminal (temporary, not saved)")
        print("3. Exit the application")

        while True:
            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                # Show the current .env file content
                try:
                    with open('.env', 'r') as f:
                        env_content = f.read()
                    print("\nCurrent .env file content:")
                    print("-" * 40)
                    print(env_content)
                    print("-" * 40)
                except Exception as e:
                    print(f"\nError reading .env file: {str(e)}")

                print("\nPlease edit the .env file with the following format:")
                print("DISCORD_TOKEN=your_token_here  (without quotes)")
                print("DISCORD_CHANNEL_ID=your_channel_id_here  (without quotes)")
                print("\nThen restart the application.")
                sys.exit(0)
            elif choice == "2":
                print("\nEntering values directly (these will not be saved to .env file):")
                if "DISCORD_TOKEN" in env_vars_missing:
                    TOKEN = input("Enter your Discord token: ").strip().strip('"\'')
                if "DISCORD_CHANNEL_ID" in env_vars_missing:
                    CHANNEL_ID = input("Enter the Discord channel ID: ").strip().strip('"\'')
                break
            elif choice == "3":
                print("\nExiting application.")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
    else:
        print("Environment variables found and appear to be valid.")

    # Validate the token and channel ID and remove any quotes
    if TOKEN:
        TOKEN = TOKEN.strip('"\'')
    if CHANNEL_ID:
        CHANNEL_ID = CHANNEL_ID.strip('"\'')

    if not TOKEN or not CHANNEL_ID:
        print("\nError: Discord token and channel ID are required to proceed.")
        sys.exit(1)

    # Let the user select the output format
    format_type = select_format()

    # First fetch the messages
    formatted_content = fetch_messages(TOKEN, CHANNEL_ID, format_type)

    # If we successfully fetched and formatted messages, prompt for save location
    if formatted_content:
        # Save the messages to a file
        save_messages(formatted_content, TOKEN, CHANNEL_ID, format_type)
    else:
        print("No messages to save. Exiting.")