# A E S T H E T I C C A P T U R E

Your Playlist, Visualized.

## Channels

* [@DreamToneRealm](https://www.youtube.com/@DreamToneRealm)
* [@moebiusfm](https://www.youtube.com/@moebiusfm)
* [@NOXORAMUSIC](https://www.youtube.com/@NOXORAMUSIC)
* [@synthodysseyfm](https://www.youtube.com/@synthodysseyfm)
* [@veltrixfm](https://www.youtube.com/@veltrixfm)
* [@VHSFMMemory](https://www.youtube.com/@VHSFMMemory)

## What is This?

Aesthetic Capture is an automated YouTube channel thumbnail archiver that downloads thumbnails from your favorite YouTube channels. Perfect for creating visual galleries of music playlists, video series, or any YouTube content you want to preserve and visualize.

The project automatically runs daily via GitHub Actions, capturing new video thumbnails and organizing them by channel.

## How It Works

1. **Daily Automation**: GitHub Actions runs the script every day at 00:00 UTC
2. **Smart Detection**: Only downloads thumbnails for new videos (skips already-downloaded content)
3. **Efficient Downloading**: Fetches newest videos first to quickly detect and skip existing content
4. **Channel Organization**: Creates separate directories for each YouTube channel
5. **Chronological Numbering**: Files numbered from oldest (0000) to newest for consistent ordering
6. **Automatic Commits**: New thumbnails are automatically committed to the repository

## Repository Structure

This repository uses a **dual-branch architecture**:

### `main` Branch
Contains the automation code and configuration:
- `aestheticcapture.py` - Python script that downloads video thumbnails
- `channels.txt` - List of YouTube channels to monitor (one per line, e.g., `@channelname`)
- `.github/workflows/aesthetic-capture.yml` - GitHub Actions workflow

### `images` Branch
Contains only the downloaded images:
- Organized by channel name (e.g., `channelname/`)
- Each image named: `####_videoID_VideoTitle.webp` (or `.jpg`, `.png` depending on source)
- No code or scripts, just pure image gallery

## Configuration

### Adding Channels

Edit `channels.txt` on the `main` branch:

```
@channel1
@channel2
```

Lines starting with `#` are treated as comments and ignored.

### Setting Up Cookies (Optional)

**Cookies are completely optional** - the script works without them, but YouTube may block some video downloads due to bot detection.

#### For GitHub Actions (Recommended)

Add your browser cookies as a repository secret:

1. Get cookies from your browser using an extension like "Get cookies.txt LOCALLY"
2. Go to repository **Settings → Secrets and variables → Actions**
3. Create a new secret named `YOUTUBE_COOKIES` and paste the cookies content
4. The workflow automatically creates `cookies.txt` from this secret during execution

#### For Local Execution

Create a `cookies.txt` file in the same directory as the script with your browser cookies.

## Manual Execution

### GitHub Actions (Manual Trigger)

Go to the **Actions** tab and manually trigger the "Aesthetic Capture Daily Run" workflow.

### Local Execution

```bash
# Clone the repository (main branch contains the script)
git clone https://github.com/yourusername/aestheticcapture.git
cd aestheticcapture

# Create virtual environment
uv venv --python 3.13

# Install dependencies
uv pip install -r requirements.txt

# Update channels.txt with your channels
# (Optional) Add cookies.txt for authentication

# Run the script
python aestheticcapture.py
```


## Why Separate Branches?

- **main**: Version-controlled code and configuration
- **images**: Clean image gallery without code clutter
- Allows the script to check for existing files without mixing code and data
- Makes the images branch usable as a pure image CDN or gallery

