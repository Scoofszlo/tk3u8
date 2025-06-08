# tk3u8

tk3u8 is a Python program that helps you download live streams from TikTok. The project was based and built from <b>Michele0303's [tiktok-live-recorder](https://github.com/Michele0303/tiktok-live-recorder)</b>, and modified for ease of use and to utilize <b>yt-dlp</b> and <b>ffmpeg</b> as a downloader. Credits to them!


## Requirements
- Windows or Linux
- Python `>=3.10.0`
- ffmpeg
- uv
- Git

## Installation
1. Install Python 3.10.0 or above. Ensure `Add Python x.x to PATH` is checked.
2. Install [ffmpeg](https://ffmpeg.org/download.html). Ensure ffmpeg is added to [PATH](https://phoenixnap.com/kb/ffmpeg-windows#Step_3_Add_FFmpeg_to_PATH).
3. Install [Git](https://git-scm.com/downloads/win).
4. Install uv, through `pip` command or via [Standalone installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).
    ```sh
    pip install uv
    ```
5. Clone this repository using Git.
    ```sh
    git clone https://github.com/Scoofszlo/tk3u8.git
    ```
6. Change the current directory to the project's folder.
    ```sh
    cd tk3u8
    ```
7. Use the latest published release. (Skip this step if you want to use all of latest changes and updates from this repository.)
    ```sh
    git checkout tags/v0.3.1
    ```
8. Run the program.
    ```sh
    uv run tk3u8 -h
    ```
    When installed properly, the output should look like this:
    ```text
    Usage: tk3u8 [-h] [-q {original,uhd_60,uhd,hd_60,hd,ld,sd}] [--proxy PROXY]
                 [--wait-until-live] [--timeout TIMEOUT] [--log-level {DEBUG,ERROR}] 
                 [-v] username

    tk3u8 - A TikTok live downloader

    Positional Arguments:
      username              The username to be used for recording live stream

    Options:
      -h, --help            show this help message and exit
      -q {original,uhd_60,uhd,hd_60,hd,ld,sd}
                            Specify the quality of the video to download. Default: original
      --proxy PROXY         The proxy server to use for downloading. Sample format: 127.0.0.1:8080
      --wait-until-live     Let the program wait until the user goes live to start downloading stream
      --timeout TIMEOUT     Set the timeout in seconds before rechecking if the user is live.
      --log-level {DEBUG,ERROR}
                            Set the logging level (default: no logging if not used)
      -v, --version         Show the program's version
    ```

## Quickstart
After installation, you can now use the project's folder, open the terminal there and run, for example,`uv run tk3u8 -h` every time.

To download a live stream from a user, simply run:
```sh
uv run tk3u8 username
```

If the user is not live, the program will raise an error:
```sh
tk3u8.exceptions.UserNotLiveError: User @username is not live.
```

For complete guide on how to use the program, head over to the [Usage](https://github.com/Scoofszlo/tk3u8/wiki/Usage) guide.

## Documentation

The project documentation is available at the [wiki](https://github.com/Scoofszlo/tk3u8/wiki) of this repository. These includes detailed step-by-step installation,  usage guide, configuration guide, and some information about common issues and how to fix them. Here are some of the specific links for each one:

- [Installation Guide](https://github.com/Scoofszlo/tk3u8/wiki/Installation)
- [Usage Guide](https://github.com/Scoofszlo/tk3u8/wiki/Usage)
- [Configuration Guide](https://github.com/Scoofszlo/tk3u8/wiki/Configuration)
- [Issues](https://github.com/Scoofszlo/tk3u8/wiki/Issues) - Recommended to check for those who are having regular issues with `WAFChallengeError`, `StreamLinkNotFoundError`, and `StreamDataNotFoundError` errors.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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
