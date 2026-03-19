import os
import sys
import time
import re
import requests
from pathlib import Path
import yt_dlp

# -------------------------------
# 1. Download path
# -------------------------------
if "com.termux" in os.environ.get("PREFIX", ""):
    DOWNLOAD_DIR = Path("/storage/emulated/0/Download/TikTok")
else:
    DOWNLOAD_DIR = Path.home() / "Downloads" / "TikTok"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# -------------------------------
# 2. Clean title
# -------------------------------
def clean_title(title):
    if not title:
        return "TikTok"

    # remove useless words
    title = re.sub(r'\b(video|official|tiktok)\b', '', title, flags=re.IGNORECASE)

    # remove invalid characters
    title = re.sub(r'[\\/*?:"<>|]', '', title)

    # normalize spaces
    title = re.sub(r'\s+', ' ', title).strip()

    return title or "TikTok"

# -------------------------------
# 3. Unique filename (no overwrite)
# -------------------------------
def get_unique_filename(path):
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    counter = 1

    while True:
        new_path = path.with_name(f"{stem}_{counter}{suffix}")
        if not new_path.exists():
            return new_path
        counter += 1

# -------------------------------
# 4. Progress bar for images
# -------------------------------
def image_progress(current, total):
    bar_length = 12
    filled = int(bar_length * current / total)
    bar = "█" * filled + " " * (bar_length - filled)

    print(f"\r💾 Pictures [{bar}] ⬇ {current}/{total}", end="")

# -------------------------------
# 5. TikTok data fetch
# -------------------------------
def get_tiktok_data(url):
    api = "https://www.tikwm.com/api/"
    try:
        res = requests.get(api, params={"url": url}, headers=HEADERS, timeout=10)
        data = res.json().get("data", {})
        return {
            "images": data.get("images"),
            "title": data.get("title") or "TikTok"
        }
    except:
        return None

# -------------------------------
# 6. Download images
# -------------------------------
def download_images(images, title):
    title = clean_title(title)
    total = len(images)
    success = 0

    for i, img in enumerate(images, 1):
        base_filename = DOWNLOAD_DIR / f"{title} ({i}).jpg"
        filename = get_unique_filename(base_filename)

        for _ in range(3):
            try:
                r = requests.get(img, headers=HEADERS, timeout=10)
                if r.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(r.content)
                    success += 1
                    break
            except:
                time.sleep(1)

        image_progress(i, total)

    print(f"\n📸 Done: {success}/{total} images")

# -------------------------------
# 7. yt-dlp progress
# -------------------------------
def video_progress(d):
    if d["status"] == "downloading":
        percent = d.get("_percent_str", "").strip()
        speed = d.get("_speed_str", "").strip()
        eta = d.get("_eta_str", "").strip()
        print(f"\r⬇ {percent} | {speed} | ETA {eta}", end="")
    elif d["status"] == "finished":
        print("\n✔ Video download complete")

# -------------------------------
# 8. Download video
# -------------------------------
def download_video(urls):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        "noplaylist": True,
        "retries": 3,
        "fragment_retries": 3,
        "socket_timeout": 30,
        "concurrent_fragment_downloads": 4,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [video_progress],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)

# -------------------------------
# 9. Main logic
# -------------------------------
def process_url(url):
    print(f"\n🔗 Processing: {url}")

    data = get_tiktok_data(url)

    if data and data["images"]:
        download_images(data["images"], data["title"])
    else:
        download_video([url])

# -------------------------------
# 10. Entry
# -------------------------------
urls = input("Enter TikTok URL(s), separated by space: ").split()

if not urls:
    print("❌ No URL provided")
    sys.exit(1)

for url in urls:
    try:
        process_url(url)
    except Exception as e:
        print(f"❌ Failed: {e}")

print(f"\n📁 Saved to: {DOWNLOAD_DIR}")