# YouTube Cookies Setup

To avoid YouTube bot detection in GitHub Actions, you need to export your YouTube cookies and add them as a GitHub secret.

## Step 1: Export YouTube Cookies

### Option A: Using a Browser Extension (Recommended)
1. Install a cookies export extension:
   - Chrome/Edge: [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - Firefox: [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. Visit [youtube.com](https://www.youtube.com) and make sure you're logged in

3. Click the extension icon and export cookies for youtube.com

4. Save the exported `cookies.txt` file

### Option B: Using yt-dlp
```bash
yt-dlp --cookies-from-browser chrome --cookies cookies.txt "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
Replace `chrome` with your browser (chrome, firefox, safari, edge, etc.)

## Step 2: Add Cookies to GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `YOUTUBE_COOKIES`
5. Value: Paste the entire contents of your `cookies.txt` file
6. Click **Add secret**

## Step 3: Test

Once the secret is added, the workflow will automatically use it. You can trigger a manual run to test:
1. Go to **Actions** tab
2. Click **Aesthetic Capture Daily Run**
3. Click **Run workflow**

## Notes

- Cookies may expire after some time (weeks/months). If downloads start failing with bot detection errors, regenerate and update the secret.
- Keep your cookies private - they provide access to your YouTube account
- The cookies are only used to authenticate yt-dlp requests and bypass bot detection
