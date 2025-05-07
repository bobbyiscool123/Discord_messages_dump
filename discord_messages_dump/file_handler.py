"""File handler for Discord Messages Dump.

This module provides a FileHandler class for handling file operations
such as opening file dialogs and saving content to files.
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional


class FileHandler:
    """
    Handler for file operations in Discord Messages Dump.
    
    This class provides methods for opening file dialogs, saving content to files,
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
    
    def get_file_type_info(self, format_type: str) -> tuple:
        """
        Get file type information for the given format type.
        
        Args:
            format_type (str): The format type (text, json, csv, markdown).
            
        Returns:
            tuple: A tuple containing (extension, filetypes, default_filename).
        """
        extension = self.get_file_extension(format_type)
        
        if format_type.lower() == "json":
            filetypes = [("JSON Files", "*.json"), ("All Files", "*.*")]
            default_filename = "discord_messages.json"
        elif format_type.lower() == "csv":
            filetypes = [("CSV Files", "*.csv"), ("All Files", "*.*")]
            default_filename = "discord_messages.csv"
        elif format_type.lower() == "markdown":
            filetypes = [("Markdown Files", "*.md"), ("All Files", "*.*")]
            default_filename = "discord_messages.md"
        else:  # Default to text
            filetypes = [("Text Files", "*.txt"), ("All Files", "*.*")]
            default_filename = "discord_messages.txt"
            
        return extension, filetypes, default_filename
    
    def open_save_dialog(self, default_filename: str = "discord_messages.txt", format_type: str = "text") -> Optional[str]:
        """
        Open a file dialog to select where to save the output file.
        
        Args:
            default_filename (str, optional): Default filename to suggest. Defaults to "discord_messages.txt".
            format_type (str, optional): Format type to determine file extension. Defaults to "text".
            
        Returns:
            Optional[str]: The selected file path, or None if canceled.
        """
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Get file type information
        extension, filetypes, _ = self.get_file_type_info(format_type)
        
        # If default_filename doesn't have the correct extension, add it
        if not default_filename.endswith(extension):
            default_filename = default_filename + extension
        
        # Open the save dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=extension,
            filetypes=filetypes,
            initialfile=default_filename,
            initialdir=self.last_directory
        )
        
        # Update the last used directory if a file was selected
        if file_path:
            self.last_directory = os.path.dirname(file_path)
            
            # Check if file exists and confirm overwrite
            if os.path.exists(file_path):
                if not self._confirm_overwrite(file_path):
                    return None
        
        return file_path
    
    def _confirm_overwrite(self, file_path: str) -> bool:
        """
        Show a confirmation dialog for overwriting an existing file.
        
        Args:
            file_path (str): Path to the file that would be overwritten.
            
        Returns:
            bool: True if the user confirms overwrite, False otherwise.
        """
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        filename = os.path.basename(file_path)
        result = messagebox.askyesno(
            "Confirm Overwrite",
            f"The file '{filename}' already exists. Do you want to overwrite it?"
        )
        
        return result
    
    def save_content(self, content: str, file_path: str) -> bool:
        """
        Save content to a file.
        
        Args:
            content (str): The content to save.
            file_path (str): Path to save the content to.
            
        Returns:
            bool: True if the save was successful, False otherwise.
            
        Raises:
            IOError: If there's an error writing to the file.
        """
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return True
        except IOError as e:
            # Show error message
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Save Error", f"Error saving file: {str(e)}")
            return False
        except Exception as e:
            # Show error message for any other exceptions
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            return False
