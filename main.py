import os
import sys
import time
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
# 2. Progress bar for images
# -------------------------------
def image_progress(current, total):
    bar_length = 12
    filled = int(bar_length * current / total)

    bar = "█" * filled + " " * (bar_length - filled)

    print(f"\r💾 Pictures [{bar}] ⬇ {current}/{total}", end="")
    

# -------------------------------
# 3. TikTok image fetch
# -------------------------------
def get_tiktok_images(url):
    api = "https://www.tikwm.com/api/"
    try:
        res = requests.get(api, params={"url": url}, headers=HEADERS, timeout=10)
        data = res.json().get("data", {})
        return data.get("images")
    except:
        return None


# -------------------------------
# 4. Download images
# -------------------------------
def download_images(images):
    total = len(images)
    success = 0

    for i, img in enumerate(images, 1):
        filename = DOWNLOAD_DIR / f"image_{i}.jpg"

        for _ in range(3):  # retry
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
# 5. yt-dlp progress
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
# 6. Download video
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
# 7. Main logic (auto detect)
# -------------------------------
def process_url(url):
    print(f"\n🔗 Processing: {url}")

    images = get_tiktok_images(url)

    if images:
        print(f"📸 {len(images)} images found\n")
        download_images(images)
    else:
        print("🎥 Switching to video mode...\n")
        download_video([url])


# -------------------------------
# 8. Entry
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