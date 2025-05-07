"""Example script demonstrating how to use the Discord Messages Dump CLI."""

import os
import subprocess
import sys

# Ensure the package is installed
try:
    import discord_messages_dump
except ImportError:
    print("Discord Messages Dump package not installed. Please install it first:")
    print("pip install -e .")
    sys.exit(1)

# Example 1: Basic usage with all options specified
def example_1():
    """Basic usage with all options specified."""
    print("\n=== Example 1: Basic usage with all options specified ===")
    
    # Replace these with your actual values
    token = os.getenv("DISCORD_TOKEN", "your_discord_token")
    channel_id = os.getenv("DISCORD_CHANNEL_ID", "your_channel_id")
    
    command = [
        "discord-dump", "dump",
        "--token", token,
        "--channel-id", channel_id,
        "--format", "text",
        "--output-file", "example_output.txt",
        "--limit", "10",
        "--no-gui"
    ]
    
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command)

# Example 2: Using environment variables
def example_2():
    """Using environment variables for token and channel ID."""
    print("\n=== Example 2: Using environment variables for token and channel ID ===")
    
    # Make sure DISCORD_TOKEN and DISCORD_CHANNEL_ID are set in your environment
    if not os.getenv("DISCORD_TOKEN") or not os.getenv("DISCORD_CHANNEL_ID"):
        print("Error: DISCORD_TOKEN and DISCORD_CHANNEL_ID must be set in the environment.")
        return
    
    command = [
        "discord-dump", "dump",
        "--format", "json",
        "--output-file", "example_output.json",
        "--limit", "20",
        "--no-gui"
    ]
    
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command)

# Example 3: Using the GUI file dialog
def example_3():
    """Using the GUI file dialog to select output file."""
    print("\n=== Example 3: Using the GUI file dialog to select output file ===")
    
    # Replace these with your actual values
    token = os.getenv("DISCORD_TOKEN", "your_discord_token")
    channel_id = os.getenv("DISCORD_CHANNEL_ID", "your_channel_id")
    
    command = [
        "discord-dump", "dump",
        "--token", token,
        "--channel-id", channel_id,
        "--format", "markdown",
        "--limit", "5"
    ]
    
    print(f"Running command: {' '.join(command)}")
    print("A file dialog should open to select the output file location.")
    subprocess.run(command)

# Example 4: Installing command completion
def example_4():
    """Installing command completion for bash/zsh."""
    print("\n=== Example 4: Installing command completion for bash/zsh ===")
    
    command = ["discord-dump", "install-completion"]
    
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command)

if __name__ == "__main__":
    print("Discord Messages Dump CLI Examples")
    print("=================================")
    print("This script demonstrates various ways to use the Discord Messages Dump CLI.")
    print("Make sure you have installed the package with 'pip install -e .'")
    
    # Uncomment the examples you want to run
    # example_1()
    # example_2()
    # example_3()
    # example_4()
    
    print("\nTo run an example, uncomment the corresponding line in this script.")
