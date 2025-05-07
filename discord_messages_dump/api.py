"""Discord API Client for fetching messages from Discord channels."""

import time
from typing import Dict, List, Optional, Any

import requests


class DiscordApiClient:
    """
    Client for interacting with the Discord API.
    
    This class provides methods to fetch messages from Discord channels
    using a user token (selfbot). It handles rate limiting and implements
    exponential backoff retry logic.
    
    Attributes:
        token (str): The Discord user token for authentication.
        base_url (str): The base URL for Discord API requests.
    """

    def __init__(self, token: str) -> None:
        """
        Initialize the Discord API client with a user token.
        
        Args:
            token (str): The Discord user token for authentication.
        """
        self.token = token
        self.base_url = "https://discord.com/api/v9"
        self.headers = {
            'Authorization': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_messages(self, channel_id: str, limit: int = 100, before: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch messages from a Discord channel.
        
        This method retrieves messages from a specified Discord channel.
        It handles pagination and rate limits automatically.
        
        Args:
            channel_id (str): The ID of the Discord channel to fetch messages from.
            limit (int, optional): Maximum number of messages to retrieve per request. Defaults to 100.
            before (Optional[str], optional): Message ID to fetch messages before. Used for pagination. Defaults to None.
            
        Returns:
            List[Dict[str, Any]]: A list of message objects as dictionaries.
            
        Raises:
            requests.exceptions.RequestException: If there's an error with the HTTP request.
            ValueError: If the channel ID is invalid or the token is incorrect.
        """
        endpoint = f"/channels/{channel_id}/messages"
        url = f"{self.base_url}{endpoint}?limit={limit}"
        
        if before:
            url += f"&before={before}"
            
        retry_count = 0
        max_retries = 5
        retry_delays = [1, 2, 4, 8, 16]  # Exponential backoff delays in seconds
        
        while retry_count < max_retries:
            try:
                response = requests.get(url, headers=self.headers)
                
                # Handle rate limits
                if response.status_code == 429:
                    self._handle_rate_limits(response)
                    retry_count += 1
                    continue
                    
                # Handle other errors
                if response.status_code != 200:
                    if response.status_code == 401:
                        raise ValueError("Invalid Discord token. Authentication failed.")
                    elif response.status_code == 404:
                        raise ValueError(f"Channel with ID {channel_id} not found.")
                    else:
                        raise requests.exceptions.RequestException(
                            f"Error: Status code {response.status_code} - {response.text}"
                        )
                        
                # Return successful response
                return response.json()
                
            except (requests.exceptions.RequestException, ValueError) as e:
                # If it's a ValueError (invalid token or channel), re-raise immediately
                if isinstance(e, ValueError):
                    raise
                
                # Otherwise, implement retry logic with exponential backoff
                if retry_count < max_retries - 1:
                    delay = retry_delays[retry_count]
                    print(f"Request failed. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    retry_count += 1
                else:
                    # If we've exhausted all retries, raise the exception
                    raise
        
        # This should never be reached due to the raise in the else clause above
        return []

    def _handle_rate_limits(self, response: requests.Response) -> None:
        """
        Handle Discord API rate limits.
        
        This method parses the rate limit headers from the Discord API response
        and waits for the appropriate amount of time before allowing the next request.
        
        Args:
            response (requests.Response): The HTTP response from the Discord API.
            
        Returns:
            None
        """
        if 'X-RateLimit-Reset-After' in response.headers:
            # Get the number of seconds to wait before making another request
            reset_after = float(response.headers['X-RateLimit-Reset-After'])
            print(f"Rate limited. Waiting for {reset_after:.2f} seconds...")
            time.sleep(reset_after)
        else:
            # If the header is missing, use a default wait time
            print("Rate limited. Waiting for 5 seconds...")
            time.sleep(5)
