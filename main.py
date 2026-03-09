import yt_dlp
from pathlib import Path

Path("downloads").mkdir(exist_ok=True)

urls = input("TikTok URL: ").split()

ydl_opts = {
    "format": "best",
    "outtmpl": "downloads/%(title)s_%(playlist_index)s.%(ext)s",
    "noplaylist": True,

    "retries": 3,
    "fragment_retries": 3,
    "socket_timeout": 30,

    "concurrent_fragment_downloads": 4
}

MAX_TRIES = 3

for attempt in range(1, MAX_TRIES + 1):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)

        print("Download finished")
        break

    except Exception as e:
        print(f"Attempt {attempt} failed:", e)

        if attempt == MAX_TRIES:
            print("Download failed after 3 tries")