# tk3u8

**tk3u8** is a TikTok live downloader, written in Python. The project was based and built from <b>Michele0303's [tiktok-live-recorder](https://github.com/Michele0303/tiktok-live-recorder)</b>, and modified for ease of use and to utilize <b>yt-dlp</b> and <b>FFmpeg</b> as a downloader. The project currently supports Windows and Linux systems.

Some of the key features include:

- Download TikTok live stream by username through command-line
- Choose stream quality (original, uhd, hd, etc.)
- Let program download live stream once user goes online
- Public API support for creating your own scripts
- Proxy support
- Config support

## Quickstart

In case you're in hurry, here is a short, quick installation and usage guide. For more comprehensive details, see the [installation](https://scoofszlo.github.io/tk3u8/latest/installation/) and [usage](https://scoofszlo.github.io/tk3u8/latest/usage/) guides.

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

## Documentation

The project documentation is available at [scoofszlo.github.io/tk3u8](https://scoofszlo.github.io/tk3u8/). These includes detailed step-by-step installation,  usage guide, configuration guide, and some information about common issues and how to fix them. Here are some of the specific links for each one:

- [Installation Guide](https://scoofszlo.github.io/tk3u8/latest/installation/)
- [Usage Guide](https://scoofszlo.github.io/tk3u8/latest/usage/)
- [Configuration Guide](https://scoofszlo.github.io/tk3u8/latest/configuration/)
- [Issues](https://scoofszlo.github.io/tk3u8/latest/issues/) - Recommended to check for those who are having regular issues with `HLSLinkNotFoundError`, `WAFChallengeError`,and `StreamDataNotFoundError` errors.

## License

tk3u8 is an open-source program licensed under the [MIT](LICENSE) license.

If you can, please contribute to this project by suggesting a feature, reporting issues, or make code contributions!

## Legal Disclaimer

The use of this software to download content without the permission may violate copyright laws or TikTok's terms of service. The author of this project is not responsible for any misuse or legal consequences arising from the use of this software. Use it at your own risk and ensure compliance with applicable laws and regulations.

This project is not affiliated, endorsed, or sponsored by TikTok or its affiliates. Use this software at your own risk.

## Acknowledgements

Special thanks to Michele0303 for their amazing work on [tiktok-live-recorder](https://github.com/Michele0303/tiktok-live-recorder), which served as the foundation for this project.

## Contact

For questions or concerns, feel free to contact me via the following!:
- [Gmail](mailto:scoofszlo@gmail.com) - scoofszlo@gmail.com
- Discord - @scoofszlo
- [Reddit](https://www.reddit.com/user/Scoofszlo/) - u/Scoofszlo
- [Twitter](https://twitter.com/Scoofszlo) - @Scoofszlo
