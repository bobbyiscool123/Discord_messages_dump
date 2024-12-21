import requests
import json
import time
import os
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv

load_dotenv()

def get_messages(token, channel_id, output_file):
    """
    Fetches all messages from a Discord channel using the user token.

    Args:
      token: Your Discord user token.
      channel_id: The ID of the channel to fetch messages from.
      output_file: Path to save the messages to.
    """

    headers = {
        'Authorization': token  # Adds your token to request headers
    }
    base_url = "https://discord.com/api/v9" # API Base URL
    endpoint = f"/channels/{channel_id}/messages" # Endpoint for fetching messages for the channel

    messages = [] # List to store the messages
    before = None # Used for pagination
    limit = 100 # How many messages to get at a time

    while True: # Loop until no more messages
        url = f"{base_url}{endpoint}?limit={limit}"
        if before: # If there is a last message ID, append it for pagination.
            url += f"&before={before}"

        response = requests.get(url, headers=headers)  # Make a GET request to the API
        if response.status_code == 200: # Check that the response was successful
            new_messages = response.json() # Convert the data to a python object.
            if not new_messages: # If no new messages, we must be done
                break # Exit the loop

            messages.extend(new_messages)  # Add the new messages to the message list
            before = new_messages[-1]['id']  # Get the last message ID for pagination

            # Add a delay to respect rate limits
            time.sleep(0.5)  # Adjust if needed

            print(f"Fetched {len(messages)} messages so far.") # Output the current progress.

        else:
            print(f"Error: Status code {response.status_code} - {response.text}")  #Print error message
            break  # Stop the loop

    # Sort messages by timestamp (oldest first)
    messages.sort(key=lambda x: x['timestamp'])  # Sort messages

    # Save messages to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        for message in messages:
            author_name = message['author']['username']  # Get the author name from message
            content = message['content'] # Get the message content
            timestamp = message['timestamp'] # Get the timestamp
            f.write(f"[{timestamp}] {author_name}: {content}\n")  #Write to file in formatted string format

    print(f"All messages saved to: {output_file}")

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], initialfile="discord_messages.txt")
    return file_path

if __name__ == "__main__":
    """Main execution block."""
    # Load values from the environment file
    TOKEN = os.getenv("DISCORD_TOKEN")
    CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

    if not TOKEN or not CHANNEL_ID:
        print("Error: DISCORD_TOKEN and DISCORD_CHANNEL_ID must be set in the .env file.")
        exit()


    # Open file dialog to choose save location
    output_file_path = open_file_dialog()

    if output_file_path:
         # Call the get messages function with the token, channel ID and output filename.
         get_messages(TOKEN, CHANNEL_ID, output_file_path)
    else:
      print("No file selected. Exiting.")