"""
Twitter Spaces Downloader Class for Telegram Bot
"""

import os
import uuid
import yt_dlp
from urllib.parse import urlparse


class TwitterSpacesDownloader:
    """
    Class for downloading Twitter Spaces audio recordings
    """

    def __init__(self, temp_folder):
        """
        Initialize the downloader

        Args:
            temp_folder: Directory for temporary files
        """
        self.temp_folder = temp_folder
        os.makedirs(temp_folder, exist_ok=True)

    def is_valid_twitter_url(self, url):
        """Check if URL is from Twitter/X"""
        parsed_url = urlparse(url)
        return parsed_url.netloc in ['twitter.com', 'x.com', 'www.twitter.com', 'www.x.com']

    def is_valid_twitter_space_url(self, url):
        """Check if URL is a Twitter Space"""
        if not self.is_valid_twitter_url(url):
            return False
        parsed_url = urlparse(url)
        return '/spaces/' in parsed_url.path or '/i/spaces/' in parsed_url.path

    def is_twitter_status_url(self, url):
        """Check if URL is a tweet status"""
        if not self.is_valid_twitter_url(url):
            return False
        parsed_url = urlparse(url)
        return '/status/' in parsed_url.path

    def download_twitter_space(self, url):
        """
        Download a Twitter Space from URL

        Args:
            url: Twitter Space URL or tweet URL containing a space

        Returns:
            str: Path to downloaded MP3 file, or None if failed
        """
        # Validate URL
        if not self.is_valid_twitter_url(url):
            print("Invalid Twitter/X URL")
            return None

        try:
            # Generate unique filename
            unique_id = uuid.uuid4().hex[:12]
            output_template = os.path.join(self.temp_folder, f"space_{unique_id}")

            print(f"Downloading Twitter Space from: {url}")

            # Configure yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': False,
                'no_warnings': False,
                'verbose': True
            }

            # Download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Find downloaded file
            mp3_file = output_template + '.mp3'
            if os.path.exists(mp3_file):
                return mp3_file

            # Search for file with unique ID
            for filename in os.listdir(self.temp_folder):
                if unique_id in filename and filename.endswith('.mp3'):
                    return os.path.join(self.temp_folder, filename)

            return None

        except Exception as e:
            print(f"Error downloading Twitter Space: {str(e)}")
            return None


if __name__ == "__main__":
    from config import TEMP_FOLDER

    downloader = TwitterSpacesDownloader(TEMP_FOLDER)

    # Test URL
    test_url = "https://x.com/i/spaces/1BdGYZeQODDJX"
    result = downloader.download_twitter_space(test_url)

    if result:
        print(f"✅ Success: {result}")
    else:
        print("❌ Failed to download")
