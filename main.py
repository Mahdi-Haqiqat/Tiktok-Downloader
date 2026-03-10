import os
import sys
from pathlib import Path
import yt_dlp

# -------------------------------
# 1. Determine the downloads path
# -------------------------------
if "com.termux" in os.environ.get("PREFIX", ""):
    # Termux
    DOWNLOAD_DIR = Path("/storage/emulated/0/Download/TikTok")
else:
    # Desktop (Windows, Linux, macOS)
    DOWNLOAD_DIR = Path.home() / "Downloads" / "TikTok"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# 2. Get URLs
# -------------------------------
urls = input("Enter TikTok URL(s), separated by space: ").split()
if not urls:
    print("❌ No URL provided")
    sys.exit(1)

# -------------------------------
# 3. Progress hook
# -------------------------------
def progress(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\r⬇ {percent} | {speed} | ETA {eta}", end="")
    elif d["status"] == "finished":
        print("\n✔ Download complete")

# -------------------------------
# 4. yt-dlp options
# -------------------------------
ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),  # full filename
    "noplaylist": True,
    "retries": 3,
    "fragment_retries": 3,
    "socket_timeout": 30,
    "concurrent_fragment_downloads": 4,
    "quiet": True,
    "no_warnings": True,
    "progress_hooks": [progress],
}

# -------------------------------
# 5. Download with retry logic
# -------------------------------
MAX_TRIES = 3
for attempt in range(1, MAX_TRIES + 1):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)

        print(f"\n📁 Saved to: {DOWNLOAD_DIR}")
        print("✅ Download finished")
        break

    except Exception as e:
        print(f"\n⚠ Attempt {attempt} failed:", e)
        if attempt == MAX_TRIES:
            print("❌ Download failed after 3 tries")
