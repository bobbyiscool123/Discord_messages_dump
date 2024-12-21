# Discord Message Dumper

This repository contains a Python script (`discord_scraper.py`) that allows you to download and save message history from a specified Discord channel. It uses the official Discord API and provides a formatted text file as output.

## Features

*   **Message Retrieval:** Fetches all messages from a given Discord channel.
*   **Formatted Output:** Saves messages to a text file with author names, timestamps, and message content.
*   **Secure Credential Handling:** Uses a `.env` file (already included, not committed to the repository) to store your Discord user token securely.
*   **File Save Dialog:** Allows users to choose where to save the output file, including filename.
*   **Pagination:** Handles Discord API's pagination, allowing retrieval of all messages in a channel without limitations.
*   **Rate Limit Handling:** Respects Discord's API rate limits with a slight delay between requests.

## How to Use

### Prerequisites

*   **Python 3.6+:** Ensure you have Python installed.
*   **Python Libraries:** Install the required libraries:
    ```bash
    pip install requests python-dotenv
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

2.  **Modify the `.env` File:**
    *   Open the existing `.env` file in the root directory of the repository.
    *   Add your Discord token and channel ID to the file:
        ```env
        DISCORD_TOKEN="YOUR_DISCORD_TOKEN"
        DISCORD_CHANNEL_ID="YOUR_DISCORD_CHANNEL_ID"
        ```
        *Replace `YOUR_DISCORD_TOKEN` and `YOUR_DISCORD_CHANNEL_ID` with your actual values.*

3. **Run the Script (Windows):**
   * Open a command prompt or PowerShell window.
   * Navigate to the repository directory using the `cd` command, example:
    ```bash
    cd path\to\discord_messages_dump
    ```
   *   Run the script:
    ```bash
    python discord_scraper.py
    ```
    *   The script will open a file dialog prompting you to select where the output text file is saved.

4.  **Run the Script (Linux / macOS):**
    *   Open a terminal window.
    *   Navigate to the repository directory using the `cd` command, example:
      ```bash
      cd path/to/discord_messages_dump
      ```
    *   Run the script:
        ```bash
        python3 discord_scraper.py
        ```
    *   The script will open a file dialog prompting you to select where the output text file is saved.

### Output

The output text file will contain the messages from the specified Discord channel, formatted as follows:
