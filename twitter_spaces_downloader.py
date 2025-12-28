"""
Simple and reliable Twitter Spaces downloader using yt-dlp
"""

import os
import uuid
import yt_dlp


def download_twitter_space(url, output_dir=None):
    """
    Download a Twitter Space to MP3 format

    Args:
        url: Twitter Spaces URL (direct space link or tweet with space)
        output_dir: Directory to save the file (defaults to ./downloads)

    Returns:
        str: Path to the downloaded MP3 file, or None if failed
    """
    try:
        # Create output directory
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(output_dir, exist_ok=True)

        # Generate unique filename
        unique_id = uuid.uuid4().hex[:12]
        output_template = os.path.join(output_dir, f"twitter_space_{unique_id}")

        print(f"Downloading Twitter Space from: {url}")
        print(f"Saving to: {output_dir}")

        # Configure yt-dlp options
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
        }

        # Download the space
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the downloaded file
        mp3_file = output_template + '.mp3'
        if os.path.exists(mp3_file):
            print(f"Successfully downloaded: {mp3_file}")
            return mp3_file

        # Search for any MP3 files with the unique ID
        for filename in os.listdir(output_dir):
            if unique_id in filename and filename.endswith('.mp3'):
                full_path = os.path.join(output_dir, filename)
                print(f"Successfully downloaded: {full_path}")
                return full_path

        print("Download completed but MP3 file not found")
        return None

    except Exception as e:
        print(f"Error downloading Twitter Space: {str(e)}")
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        url = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None

        result = download_twitter_space(url, output_dir)

        if result:
            print(f"\n✅ Success! File saved to: {result}")
        else:
            print(f"\n❌ Failed to download Twitter Space")
            sys.exit(1)
    else:
        print("Usage: python twitter_spaces_downloader.py <twitter_space_url> [output_directory]")
        print("\nExample:")
        print("  python twitter_spaces_downloader.py https://x.com/i/spaces/1BdGYZeQODDJX")
