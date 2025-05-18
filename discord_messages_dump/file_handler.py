"""File handler for Discord Messages Dump.

This module provides a FileHandler class for handling file operations
such as saving content to files and managing file extensions.
"""

import os
from typing import Optional


class FileHandler:
    """
    Handler for file operations in Discord Messages Dump.

    This class provides methods for saving content to files
    and handling file extensions based on format types.

    Attributes:
        last_directory (str): The last directory used for file operations.
    """

    def __init__(self):
        """Initialize the FileHandler with default values."""
        self.last_directory = os.path.expanduser("~")  # Default to user's home directory

    def get_file_extension(self, format_type: str) -> str:
        """
        Get the appropriate file extension for the given format type.

        Args:
            format_type (str): The format type (text, json, csv, markdown).

        Returns:
            str: The file extension including the dot (e.g., ".txt").
        """
        format_map = {
            "text": ".txt",
            "json": ".json",
            "csv": ".csv",
            "markdown": ".md"
        }
        return format_map.get(format_type.lower(), ".txt")

    def get_default_filename(self, format_type: str) -> str:
        """
        Get the default filename for the given format type.

        Args:
            format_type (str): The format type (text, json, csv, markdown).

        Returns:
            str: The default filename with appropriate extension.
        """
        if format_type.lower() == "json":
            return "discord_messages.json"
        elif format_type.lower() == "csv":
            return "discord_messages.csv"
        elif format_type.lower() == "markdown":
            return "discord_messages.md"
        else:  # Default to text
            return "discord_messages.txt"

    def construct_file_path(self, output_dir: str, format_type: str) -> str:
        """
        Construct a file path using the output directory and format type.

        Args:
            output_dir (str): Directory to save the file in.
            format_type (str): Format type to determine file extension.

        Returns:
            str: The constructed file path.
        """
        # Get default filename
        default_filename = self.get_default_filename(format_type)

        # Construct full path
        file_path = os.path.join(output_dir, default_filename)

        # Update the last used directory
        self.last_directory = output_dir

        return file_path

    def confirm_overwrite(self, file_path: str) -> bool:
        """
        Ask user to confirm overwriting an existing file via console.

        Args:
            file_path (str): Path to the file that would be overwritten.

        Returns:
            bool: True if the user confirms overwrite, False otherwise.
        """
        filename = os.path.basename(file_path)

        while True:
            response = input(f"The file '{filename}' already exists. Do you want to overwrite it? (y/n): ").lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'.")

    def save_content(self, content: str, file_path: str) -> bool:
        """
        Save content to a file.

        Args:
            content (str): The content to save.
            file_path (str): Path to save the content to.

        Returns:
            bool: True if the save was successful, False otherwise.
        """
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Check if file exists and confirm overwrite
            if os.path.exists(file_path):
                if not self.confirm_overwrite(file_path):
                    return False

            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return True
        except IOError as e:
            # Print error message
            print(f"Error saving file: {str(e)}")
            return False
        except Exception as e:
            # Print error message for any other exceptions
            print(f"An unexpected error occurred: {str(e)}")
            return False
