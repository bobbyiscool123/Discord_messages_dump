import os
import tkinter as tk
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

from discord_messages_dump.api import DiscordApiClient
from discord_messages_dump.message_processor import MessageProcessor
from discord_messages_dump.file_handler import FileHandler

load_dotenv()

def get_messages(token: str, channel_id: str, output_file: str, format_type: str = "text") -> None:
    """
    Fetches all messages from a Discord channel using the user token and saves them in the specified format.

    Args:
        token (str): Your Discord user token.
        channel_id (str): The ID of the channel to fetch messages from.
        output_file (str): Path to save the messages to.
        format_type (str, optional): Format to save messages in. Options: "text", "json", "csv", "markdown". Defaults to "text".
    """
    # Create API client
    client = DiscordApiClient(token)

    # Initialize variables
    messages: List[Dict[str, Any]] = []
    before: Optional[str] = None
    limit: int = 100

    # Fetch all messages with pagination
    while True:
        try:
            # Get batch of messages
            new_messages = client.get_messages(channel_id, limit, before)

            # If no new messages, we're done
            if not new_messages:
                break

            # Add messages to our collection
            messages.extend(new_messages)

            # Get ID of last message for pagination
            before = new_messages[-1]['id']

            print(f"Fetched {len(messages)} messages so far.")

        except Exception as e:
            print(f"Error fetching messages: {str(e)}")
            break

    # Sort messages by timestamp (oldest first)
    messages.sort(key=lambda x: x['timestamp'])

    # Create a message processor
    processor = MessageProcessor(messages)

    # Format messages based on the specified format type
    try:
        if format_type.lower() == "json":
            formatted_content = processor.format_json()
        elif format_type.lower() == "csv":
            formatted_content = processor.format_csv()
        elif format_type.lower() == "markdown":
            formatted_content = processor.format_markdown()
        else:  # Default to text format
            formatted_content = processor.format_text()

        # Save formatted content to file using FileHandler
        file_handler = FileHandler()
        if file_handler.save_content(formatted_content, output_file):
            print(f"All messages saved to: {output_file} in {format_type} format")
        else:
            print(f"Failed to save messages to: {output_file}")
    except Exception as e:
        print(f"Error processing messages: {str(e)}")

def open_file_dialog(format_type: str = "text") -> Optional[str]:
    """
    Open a file dialog to select where to save the output file.

    Args:
        format_type (str, optional): Format type to determine file extension. Defaults to "text".

    Returns:
        Optional[str]: The selected file path, or None if canceled.
    """
    file_handler = FileHandler()

    # Get default filename based on format type
    _, _, default_filename = file_handler.get_file_type_info(format_type)

    # Open save dialog
    return file_handler.open_save_dialog(default_filename, format_type)

def select_format() -> str:
    """
    Display a simple dialog for the user to select the output format.

    Returns:
        str: Selected format type ("text", "json", "csv", or "markdown").
    """
    root = tk.Tk()
    root.title("Select Output Format")
    root.geometry("300x200")

    selected_format = tk.StringVar(value="text")

    # Create format selection frame
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)

    # Add a label
    label = tk.Label(frame, text="Select output format:")
    label.pack(anchor=tk.W, pady=(0, 10))

    # Add radio buttons for each format
    formats = [
        ("Plain Text", "text"),
        ("JSON", "json"),
        ("CSV", "csv"),
        ("Markdown", "markdown")
    ]

    for text, value in formats:
        rb = tk.Radiobutton(frame, text=text, value=value, variable=selected_format)
        rb.pack(anchor=tk.W)

    # Add OK button
    def on_ok():
        root.destroy()

    ok_button = tk.Button(frame, text="OK", command=on_ok, width=10)
    ok_button.pack(pady=(20, 0))

    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Run the dialog
    root.mainloop()

    return selected_format.get()

if __name__ == "__main__":
    """Main execution block."""
    # Load values from the environment file
    TOKEN: Optional[str] = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID: Optional[str] = os.getenv("DISCORD_CHANNEL_ID")

    if not TOKEN or not CHANNEL_ID:
        print("Error: DISCORD_TOKEN and DISCORD_CHANNEL_ID must be set in the .env file.")
        exit(1)

    # Let the user select the output format
    format_type = select_format()
    print(f"Selected format: {format_type}")

    # Open file dialog to choose save location
    output_file_path = open_file_dialog(format_type)

    if output_file_path:
        # Call the get messages function with the token, channel ID, output filename, and format
        get_messages(TOKEN, CHANNEL_ID, output_file_path, format_type)
    else:
        print("No file selected. Exiting.")