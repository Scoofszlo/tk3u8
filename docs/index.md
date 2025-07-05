## Overview
**tk3u8** is a TikTok live downloader, written in Python. The project was based and built from <b>Michele0303's [tiktok-live-recorder](https://github.com/Michele0303/tiktok-live-recorder)</b>, and modified for ease of use and to utilize <b>yt-dlp</b> and <b>FFmpeg</b> as a downloader. The project currently supports Windows and Linux systems.

Some of the key features include:

- Download TikTok live stream by username through command-line
- Choose stream quality (original, uhd, hd, etc.)
- Let program download live stream once user goes online
- Public API support for creating your own scripts
- Proxy support
- Config support

## Quickstart

In case you're in hurry, here is a short, quick installation and usage guide. For more comprehensive details, see the [installation](./installation/index.md) and [usage](./usage/index.md) guides.

### Requirements
- Windows or Linux
- Python `v3.10` or greater
- FFmpeg
- uv

### Steps
1. Install Python 3.10.0 or above. For Windows users, ensure `Add Python x.x to PATH` is checked.
2. Install [FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z). For Windows users, follow this [guide](https://phoenixnap.com/kb/ffmpeg-windows#Step_1_Download_FFmpeg_for_Windows) for proper installation.
3. Open your command-line.
4. Install uv through `pip` command or via [Standalone installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

    ```console
    pip install uv
    ```

5. Install the latest published stable release of tk3u8 into your system.

    ```console
    uv tool install tk3u8
    ```

6. To download a live stream, simply run this:
    
    ```console
    tk3u8 username
    ```

7. To stop and save the live stream, just hit `Ctrl+C` once and wait for the program to finish processing and you're done! The live stream will be saved in your Downloads folder.
