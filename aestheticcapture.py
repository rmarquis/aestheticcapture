#!/usr/bin/env python3
"""
YouTube Channel Video Thumbnail Downloader
Downloads thumbnails of all videos from YouTube channels using yt-dlp.
Fetches newest videos first, but numbers files chronologically (oldest=0000).
"""

import os
import subprocess
import json
from pathlib import Path


def load_channels(config_file='channels.txt'):
    """
    Load YouTube channels from a configuration file.

    Args:
        config_file: Path to the configuration file

    Returns:
        List of channel names
    """
    channels = []

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            for line in f:
                # Strip whitespace
                line = line.strip()

                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue

                channels.append(line)

        return channels

    except FileNotFoundError:
        print(f"Warning: {config_file} not found. Using default channel.")
        return ['@moebiusfm']

    except Exception as e:
        print(f"Error reading {config_file}: {e}")
        return ['@moebiusfm']


def get_channel_videos(channel_url):
    """
    Fetch all video URLs from a YouTube channel, ordered from newest to oldest.

    Args:
        channel_url: YouTube channel URL (e.g., '@moebiusfm')

    Returns:
        List of video information dictionaries
    """
    print(f"Fetching videos from channel: {channel_url}")

    # Get all videos metadata using yt-dlp (newest to oldest)
    cmd = [
        'yt-dlp',
        '--flat-playlist',
        '--dump-json',
        f'https://www.youtube.com/{channel_url}/videos'
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Parse JSON output - each line is a separate JSON object
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                video_data = json.loads(line)
                videos.append({
                    'id': video_data.get('id'),
                    'title': video_data.get('title'),
                    'url': video_data.get('url')
                })

        print(f"Found {len(videos)} videos")
        return videos

    except subprocess.CalledProcessError as e:
        print(f"Error fetching channel videos: {e}")
        print(f"stderr: {e.stderr}")
        return []


def sanitize_filename(filename):
    """
    Sanitize filename to remove invalid characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename safe for file system
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # Replace spaces with underscores
    filename = filename.replace(' ', '_')

    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')

    # Limit length to avoid file system issues
    max_length = 200
    if len(filename) > max_length:
        filename = filename[:max_length]

    return filename


def download_thumbnail(video_id, video_title, output_dir, index, cookies_file=None):
    """
    Download the thumbnail of a video using yt-dlp.

    Args:
        video_id: YouTube video ID
        video_title: Title of the video
        output_dir: Directory to save the thumbnail
        index: Index number for filename
        cookies_file: Optional path to cookies file for authentication
    """
    # Sanitize the title for use in filename
    safe_title = sanitize_filename(video_title)

    # Create base filename with index, video ID, and title (without extension)
    base_filename = f"{index:04d}_{video_id}_{safe_title}"

    # Check if file already exists with any extension
    for ext in ['.jpg', '.webp', '.png', '.jpeg']:
        output_path = os.path.join(output_dir, f"{base_filename}{ext}")
        if os.path.exists(output_path):
            print(f"  Skipping (already exists): {base_filename}{ext}")
            return True

    print(f"  Downloading: {base_filename}")
    output_path = os.path.join(output_dir, f"{base_filename}.jpg")

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        # Download thumbnail using yt-dlp
        # Use a temporary name pattern for yt-dlp output
        temp_output = os.path.join(output_dir, f"temp_{video_id}")

        cmd = [
            'yt-dlp',
            '--write-thumbnail',
            '--skip-download',
            '--quiet',
            '--no-warnings',
            '-o', temp_output,
            video_url
        ]

        # Add cookies if provided
        if cookies_file and os.path.exists(cookies_file):
            cmd.extend(['--cookies', cookies_file])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60  # 1 minute timeout
        )

        if result.returncode != 0:
            print(f"  ✗ Failed to download thumbnail: {base_filename}")
            if result.stderr:
                print(f"    Error: {result.stderr}")
            return False

        # Find the downloaded thumbnail file (could be .jpg, .webp, .png, etc.)
        # Check for common thumbnail extensions
        temp_thumb_path = None
        for ext in ['.jpg', '.webp', '.png', '.jpeg']:
            candidate = f"{temp_output}{ext}"
            if os.path.exists(candidate):
                temp_thumb_path = candidate
                break

        if not temp_thumb_path:
            print(f"  ✗ Thumbnail file not found: {base_filename}")
            return False

        # Rename to final filename (keep original extension)
        _, ext = os.path.splitext(temp_thumb_path)
        final_output = os.path.join(output_dir, f"{base_filename}{ext}")
        os.rename(temp_thumb_path, final_output)
        print(f"  ✓ Downloaded: {os.path.basename(final_output)}")
        return True

    except subprocess.TimeoutExpired:
        print(f"  ✗ Timeout downloading {base_filename}")
        return False
    except Exception as e:
        print(f"  ✗ Error downloading {base_filename}: {e}")
        return False


def main():
    """Main function to download thumbnails from YouTube channels."""
    # Load channels from configuration file
    YOUTUBE_CHANNELS = load_channels('channels.txt')

    # Check for cookies file
    cookies_file = 'cookies.txt'
    if not os.path.exists(cookies_file):
        cookies_file = None
        print("Note: cookies.txt not found. Some videos may fail due to bot detection.")
    else:
        print(f"Using cookies from: {cookies_file}")

    print("=" * 60)
    print("YouTube Channel Video Thumbnail Downloader")
    print("=" * 60)
    print()
    print(f"Loaded {len(YOUTUBE_CHANNELS)} channel(s) from config")
    print()

    total_success = 0
    total_videos_count = 0

    # Process each channel
    for channel_num, channel in enumerate(YOUTUBE_CHANNELS, start=1):
        print(f"\n{'=' * 60}")
        print(f"Processing channel {channel_num}/{len(YOUTUBE_CHANNELS)}: {channel}")
        print(f"{'=' * 60}\n")

        # Create channel-specific output directory (no parent directory)
        # Remove @ symbol and sanitize channel name for directory
        channel_output_dir = sanitize_filename(channel.lstrip('@'))
        Path(channel_output_dir).mkdir(parents=True, exist_ok=True)

        # Get all videos from the channel (oldest to newest)
        videos = get_channel_videos(channel)

        if not videos:
            print(f"No videos found for {channel} or error occurred.")
            continue

        print()
        print(f"Starting download of {len(videos)} thumbnails from {channel}...")
        print(f"Output directory: {channel_output_dir}")
        print(f"Note: Videos fetched newest-to-oldest, numbered chronologically (oldest=0000)")
        print()

        # Download thumbnails of each video
        # Videos are newest-to-oldest, but we number chronologically (oldest=0000)
        total_videos = len(videos)
        channel_success = 0
        for loop_index, video in enumerate(videos):
            # Calculate chronological index (oldest=0000, newest=highest)
            file_index = (total_videos - 1) - loop_index

            print(f"[{loop_index+1}/{total_videos}] {video['title']}")

            if download_thumbnail(video['id'], video['title'], channel_output_dir, file_index, cookies_file):
                channel_success += 1

        total_success += channel_success
        total_videos_count += len(videos)

        print(f"\nChannel {channel} complete: {channel_success}/{len(videos)} successful")

    print()
    print("=" * 60)
    print(f"All downloads complete!")
    print(f"Processed {len(YOUTUBE_CHANNELS)} channel(s)")
    print(f"Successfully downloaded: {total_success}/{total_videos_count}")
    print("=" * 60)


if __name__ == '__main__':
    main()
