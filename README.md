# tk3u8

tk3u8 is a Python program that helps you download live streams from TikTok. The project was based and built from <b>Michele0303's [tiktok-live-recorder](https://github.com/Michele0303/tiktok-live-recorder)</b>, and modified for ease of use and to utilize <b>yt-dlp</b> as a downloader. Credits to them!


## Requirements
- Windows OS
- Python `>=3.10.0`
- Git
- uv

## Installation
1. Install Python 3.10.0 or above.
2. Install [Git](https://git-scm.com/downloads/win).
3. Install uv, through `pip` command or via [Standalone installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).
    ```sh
    pip install uv
    ```
4. Clone this repository using Git.
    ```sh
    git clone https://github.com/Scoofszlo/tk3u8.git
    ```
5. Change the current directory to the project's folder.
    ```sh
    cd tk3u8
    ```
6. Use the latest published release. (Skip this step if you want to use all of latest changes and updates from this repository.)
    ```sh
    git checkout tags/v0.1.1
    ```
7. Run the program.
    ```sh
    uv run -m tk3u8 -h
    ```

## Usage
After installation, you can now use the project's folder, open the terminal there and run, for example,`uv run -m tk3u8 -h` every time.

### Downloading a live stream

To download a live stream from a user, simply run:
```sh
uv run -m tk3u8 username
```

If the user is not live, the program will raise an error:
```sh
tk3u8.exceptions.UserNotLiveError: User @username is not live.
```

### Saving the live stream

To stop recording and save the live stream, just do `Ctrl+C` on your keyboard and wait for yt-dlp to finish and cleanup everything. The stream will be saved in `user_data/downloads/username` folder with a filename, for example,`username-20251225-original.mp4`

### Choosing stream quality

By default, the program will download the highest quality stream. If you want to specify the quality, simply choose either `original`, `uhd_60`, `uhd`, `hd_60`, `hd`, `ld`, or `sd`.
```sh
uv run -m tk3u8 username -q uhd
```

### Using proxy

You can also use a proxy by specifying the `IP_ADDRESS:PORT` in `--proxy` arg:
```sh
# Replace with your actual proxy address
uv run -m tk3u8 username --proxy 127.0.0.1:80
```

Or you can supply it too in the config file located in `user_data/config.toml`:
```toml
[config]
proxy = "127.0.0.1:80" # Replace with your actual proxy address
```

If there are both proxy address supplied in the command-line arg and in the config file, the former will be used instead.

For most cases, you don't really need to supply proxy and you can just skip this one instead.

### Setting up `sessionid_ss` and/or `tt-target-idc`

To fix issues related to `ScriptTagNotFoundError` and `StreamDataNotFoundError`, you can supply `tt-target-idc` in the config file. If it doesn't work, try to supply both `sessionid_ss` and `tt-target-idc`.

1. In your browser, go to https://tiktok.com and login your account.
2. Open Inspect Element in your browser.
3. Go to Cookies section:
    - For Google Chrome users, click the `Application`. If you can't see it, click the `>>`.
    - For Firefox users, click the `Storage`. If you can't see it, click the `>>`.
4. On Cookies dropdown, click the `https://tiktok.com`.
5. On the right hand side, find the `sessionid_ss`, as well as the `tt-target-idc`.
6. Get those values and paste it in the `user_data/config.toml` of the project's folder.
7. Your config should look like this.
    ```toml
    [config]
    sessionid_ss = "0124124abcdeuj214124mfncb23tgejf"  # Include this if only supplying tt-target-idc doesn't work
    tt-target-idc = "alisg"
    ```

Remember do not share this to anyone as this is a sensitive data tied to your TikTok account.

## Issues

### `ScriptTagNotFoundError` or `StreamDataNotFoundError` occurs

Sometimes, the program may raise an `ScriptTagNotFoundError`. This is due to actual page not being loaded (most likely due to checking of browser requests), in which the program can't extract the crucial data for getting the stream links.

To fix this, you have to supply a `tt-target-idc` (or both `tt-target-idc` and `sessionid_ss`). You will put these values in `user_data/config.toml` located in the project's folder. Refer to the guide above for detailed steps.

If this doesn't work, try using other TikTok account and follow the steps again to set these.

Alternatively, using VPN may fix this issue, in which you don't have to set the both of these two values in the config file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Legal Disclaimer

The use of this software to download content without the permission may violate copyright laws or TikTok's terms of service. The author of this project is not responsible for any misuse or legal consequences arising from the use of this software. Use it at your own risk and ensure compliance with applicable laws and regulations.

This project is not affiliated, endorsed, or sponsored by TikTok or its affiliates. Use this software at your own risk.

## Credits

Special thanks to Michele0303 for their amazing work on [tiktok-live-recorder](https://github.com/Michele0303/tiktok-live-recorder), which served as the foundation for this project.

## Contact

For questions or concerns, feel free to contact me via the following!:
- [Gmail](mailto:scoofszlo@gmail.com) - scoofszlo@gmail.com
- Discord - @scoofszlo
- [Reddit](https://www.reddit.com/user/Scoofszlo/) - u/Scoofszlo
- [Twitter](https://twitter.com/Scoofszlo) - @Scoofszlo
