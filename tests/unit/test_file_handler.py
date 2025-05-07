"""Unit tests for the FileHandler class."""

import os
import unittest
from unittest.mock import patch, MagicMock

from discord_messages_dump.file_handler import FileHandler


class TestFileHandler(unittest.TestCase):
    """Test cases for the FileHandler class."""

    def setUp(self):
        """Set up test fixtures."""
        self.file_handler = FileHandler()
        self.test_content = "Test content"
        self.test_file_path = "test_file.txt"

    def test_get_file_extension(self):
        """Test getting file extensions for different format types."""
        self.assertEqual(self.file_handler.get_file_extension("text"), ".txt")
        self.assertEqual(self.file_handler.get_file_extension("json"), ".json")
        self.assertEqual(self.file_handler.get_file_extension("csv"), ".csv")
        self.assertEqual(self.file_handler.get_file_extension("markdown"), ".md")
        # Test default case
        self.assertEqual(self.file_handler.get_file_extension("unknown"), ".txt")

    def test_get_file_type_info(self):
        """Test getting file type information for different format types."""
        # Test text format
        extension, filetypes, default_filename = self.file_handler.get_file_type_info("text")
        self.assertEqual(extension, ".txt")
        self.assertEqual(filetypes[0][0], "Text Files")
        self.assertEqual(default_filename, "discord_messages.txt")

        # Test JSON format
        extension, filetypes, default_filename = self.file_handler.get_file_type_info("json")
        self.assertEqual(extension, ".json")
        self.assertEqual(filetypes[0][0], "JSON Files")
        self.assertEqual(default_filename, "discord_messages.json")

        # Test CSV format
        extension, filetypes, default_filename = self.file_handler.get_file_type_info("csv")
        self.assertEqual(extension, ".csv")
        self.assertEqual(filetypes[0][0], "CSV Files")
        self.assertEqual(default_filename, "discord_messages.csv")

        # Test Markdown format
        extension, filetypes, default_filename = self.file_handler.get_file_type_info("markdown")
        self.assertEqual(extension, ".md")
        self.assertEqual(filetypes[0][0], "Markdown Files")
        self.assertEqual(default_filename, "discord_messages.md")

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_open_save_dialog(self, mock_asksaveasfilename):
        """Test opening a save dialog."""
        # Mock the file dialog to return a file path
        mock_asksaveasfilename.return_value = "/path/to/file.txt"
        
        # Call the method
        result = self.file_handler.open_save_dialog()
        
        # Check that the result is the mocked file path
        self.assertEqual(result, "/path/to/file.txt")
        
        # Check that the last directory was updated
        self.assertEqual(self.file_handler.last_directory, "/path/to")

    @patch('tkinter.filedialog.asksaveasfilename')
    @patch('os.path.exists')
    @patch('discord_messages_dump.file_handler.FileHandler._confirm_overwrite')
    def test_open_save_dialog_with_existing_file(self, mock_confirm, mock_exists, mock_asksaveasfilename):
        """Test opening a save dialog with an existing file."""
        # Mock the file dialog to return a file path
        mock_asksaveasfilename.return_value = "/path/to/file.txt"
        # Mock that the file exists
        mock_exists.return_value = True
        # Mock the confirmation dialog to return True (user confirms overwrite)
        mock_confirm.return_value = True
        
        # Call the method
        result = self.file_handler.open_save_dialog()
        
        # Check that the result is the mocked file path
        self.assertEqual(result, "/path/to/file.txt")
        
        # Check that the confirmation dialog was called
        mock_confirm.assert_called_once_with("/path/to/file.txt")

    @patch('tkinter.filedialog.asksaveasfilename')
    @patch('os.path.exists')
    @patch('discord_messages_dump.file_handler.FileHandler._confirm_overwrite')
    def test_open_save_dialog_cancel_overwrite(self, mock_confirm, mock_exists, mock_asksaveasfilename):
        """Test canceling overwrite in the save dialog."""
        # Mock the file dialog to return a file path
        mock_asksaveasfilename.return_value = "/path/to/file.txt"
        # Mock that the file exists
        mock_exists.return_value = True
        # Mock the confirmation dialog to return False (user cancels overwrite)
        mock_confirm.return_value = False
        
        # Call the method
        result = self.file_handler.open_save_dialog()
        
        # Check that the result is None (canceled)
        self.assertIsNone(result)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_content(self, mock_open):
        """Test saving content to a file."""
        # Call the method
        result = self.file_handler.save_content(self.test_content, self.test_file_path)
        
        # Check that the result is True (success)
        self.assertTrue(result)
        
        # Check that the file was opened with the correct parameters
        mock_open.assert_called_once_with(self.test_file_path, 'w', encoding='utf-8')
        
        # Check that the content was written to the file
        mock_open().write.assert_called_once_with(self.test_content)

    @patch('builtins.open')
    @patch('tkinter.messagebox.showerror')
    def test_save_content_error(self, mock_showerror, mock_open):
        """Test handling errors when saving content."""
        # Mock the open function to raise an IOError
        mock_open.side_effect = IOError("Test error")
        
        # Call the method
        result = self.file_handler.save_content(self.test_content, self.test_file_path)
        
        # Check that the result is False (failure)
        self.assertFalse(result)
        
        # Check that the error dialog was shown
        mock_showerror.assert_called_once()


if __name__ == "__main__":
    unittest.main()
