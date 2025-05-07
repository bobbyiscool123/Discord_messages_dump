# Discord Message Dumper

This repository provides tools to download and save message history from Discord channels. It includes both a GUI script (`Dump.py`) and a command-line interface for flexibility. The package uses the Discord API to fetch messages and can output them in various formats including text, JSON, CSV, and Markdown.

## Features

*   **Message Retrieval:** Fetches all messages from a given Discord channel.
*   **Multiple Output Formats:** Saves messages in text, JSON, CSV, or Markdown formats.
*   **Command-Line Interface:** Powerful CLI with options for token, channel ID, output format, and more.
*   **Secure Credential Handling:** Uses a `.env` file to store your Discord user token securely.
*   **File Save Dialog:** Allows users to choose where to save the output file, including filename.
*   **Pagination:** Handles Discord API's pagination, allowing retrieval of all messages in a channel without limitations.
*   **Rate Limit Handling:** Respects Discord's API rate limits with exponential backoff.
*   **Progress Bar:** Visual feedback on download progress.
*   **Verbose Logging:** Detailed logging for troubleshooting.

## How to Use

### Prerequisites

*   **Python 3.6+:** Ensure you have Python installed.
*   **Python Libraries:** Install the required libraries:
    ```bash
    pip install requests python-dotenv click tqdm
    ```
*   **Discord User Token:** You need your Discord user token. This is NOT a bot token. To obtain it:
    1.  Open Discord in your web browser or desktop app.
    2.  Press `Ctrl+Shift+I` (or `Cmd+Option+I` on macOS) to open the developer tools.
    3.  Go to the 'Network' tab.
    4.  Make any request on the Discord page, such as changing the current channel.
    5.  In the Network tab, find a request. It can be any request.
    6.  Scroll to the 'Headers' section of the request.
    7.  Find the `authorization` header. The value of that header is your user token.
        **Important:** Do not share your user token with anyone. Treat it like a password.
*   **Discord Channel ID:** You need the ID of the Discord channel you want to download messages from. To obtain the channel ID:
    1.  Enable developer mode in Discord settings (`User Settings` -> `Advanced` -> `Developer Mode` toggle).
    2.  Right-click the channel and select `Copy ID`.

### Setup

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd discord_messages_dump
    ```
    (Replace `<repository_url>` with the URL of this repository).

2.  **Create and Activate a Virtual Environment:**

    **Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

    **Linux/macOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3.  **Set Up Environment Variables:**
    *   Copy the `.env.example` file to `.env`:
        ```bash
        cp .env.example .env
        ```
    *   Open the `.env` file in a text editor and add your Discord token and channel ID:
        ```env
        DISCORD_TOKEN="YOUR_DISCORD_TOKEN"
        DISCORD_CHANNEL_ID="YOUR_DISCORD_CHANNEL_ID"
        ```
        *Replace `YOUR_DISCORD_TOKEN` and `YOUR_DISCORD_CHANNEL_ID` with your actual values.*
    *   The `.env.example` file contains detailed instructions on how to obtain these values.

4.  **Install the Package in Development Mode (Optional):**
    ```bash
    pip install -e .
    ```
    This will install the package in development mode, allowing you to use the `discord-dump` command.

5. **Run the Script (Windows):**
   * Open a command prompt or PowerShell window.
   * Navigate to the repository directory using the `cd` command, example:
    ```bash
    cd path\to\discord_messages_dump
    ```
   *   Run the script:
    ```bash
    python Dump.py
    ```
    *   The script will open a file dialog prompting you to select where the output text file is saved.

6.  **Run the Script (Linux / macOS):**
    *   Open a terminal window.
    *   Navigate to the repository directory using the `cd` command, example:
      ```bash
      cd path/to/discord_messages_dump
      ```
    *   Run the script:
        ```bash
        python3 Dump.py
        ```
    *   The script will open a file dialog prompting you to select where the output text file is saved.

### Using the Command-Line Interface

The package provides a powerful command-line interface that can be used instead of the GUI script:

1. **Install the Package:**
   ```bash
   pip install -e .
   ```

2. **Basic Usage:**
   ```bash
   # Using command-line arguments
   discord-dump dump --token "YOUR_TOKEN" --channel-id "YOUR_CHANNEL_ID" --format text --output-file messages.txt

   # Using environment variables from .env file
   discord-dump dump --format json --output-file messages.json
   ```

3. **Available Options:**
   ```
   --token TEXT           Discord user token for authentication
   --channel-id TEXT      ID of the Discord channel to fetch messages from
   --format [text|json|csv|markdown]
                          Output format for the messages (default: text)
   --output-file TEXT     Path to save the messages to
   --limit INTEGER        Maximum number of messages to retrieve (default: 100)
   --no-gui               Disable GUI file dialog for selecting output file
   --verbose              Enable verbose logging
   --help                 Show help message and exit
   ```

4. **Install Command Completion:**
   ```bash
   discord-dump install-completion
   ```

### Output

The output file will contain the messages from the specified Discord channel, formatted according to the chosen format:
