# TikTok Downloader (CLI)

A simple command-line tool to download videos and photo slideshows from TikTok for personal and educational use.

---

## Features

* Download TikTok videos
* Supports `vm.tiktok.com` short links
* Saves media to a `downloads/` folder
* Simple CLI interface
* Lightweight and fast

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Mahdi-Haqiqat/Tiktok-Downloader.git
cd Tiktok-Downloader
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Run the program:

```bash
python main.py
```

Then paste a TikTok URL when prompted.

Example:

```
TikTok URL: https://www.tiktok.com/@username/video/123456789
```

Downloaded media will be saved in the `downloads` folder.

---

## Requirements

* Python 3.8+
* Internet connection

Python dependencies:

```
yt-dlp
```

---

## Project Structure

```
tiktok-downloader
│
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── downloads/
```

---

## Disclaimer

This project is intended for **educational and personal use only**.

Users are responsible for complying with the Terms of Service of TikTok and any applicable laws in their country.

This project does **not encourage or support copyright infringement, illegal downloading, or misuse of content**.

The author of this repository is **not responsible for how this software is used**.

---

## License

This project is licensed under the MIT License.
