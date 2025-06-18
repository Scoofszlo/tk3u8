There are two ways to use this program. For the easiest and straightforward approach, you can [use the program through your terminal](#using-through-terminal). Advanced users may choose to use the program within a script, however, the steps will not be included in this guide as I have to create one yet. If you are knowledgeable and have explored the source code, you can do it!

## Using through terminal

The simplest way to use this program is through your terminal (e.g., Command Prompt on Windows). After following the [installation](https://github.com/Scoofszlo/tk3u8/wiki/Installation) steps, you can now use several commands to perform basic stuff like [downloading a live stream](#downloading-a-live-stream). Refer to the following steps below on each command usage.


!!! info
    For users who have installed the program through system-wide installation, omit the `uv run` for each command listed below.

### Downloading a live stream

To download a live stream from a user, simply run:
```console
uv run tk3u8 username  # Replace 'username` with actual username of the user
```

If the user is not live, the program will show a message saying:
```console
User @username is currently offline.
```

If the user is live, the program will show the following output:
```console
User @username is now streaming live.
Starting download for user @username (quality: original, stream Link: https://pull-hls-f16-va01.tiktokcdn.com/...) # Stream link may vary
```

After this appears, you will see many messages popping up, which is from ffmpeg. If this kinda overwhelms you, you don't have to worry about these messages. It is just the library that logs its activity as it is processing and capturing the live stream data.

### Saving the live stream

To stop recording and save the live stream, just hit `Ctrl+C` on your keyboard and wait for ffmpeg to finish and cleanup everything. The stream will be saved in `tk3u8` directory inside your Downloads folder. This folder will contain subfolders for each user you have downloaded from, with a filename, for example, `username-20251225_081015-original.mp4`

### Choosing stream quality

By default, the program will download the highest quality available. If you want to specify the quality to download, simply choose either `original`, `uhd_60`, `uhd`, `hd_60`, `hd`, `ld`, or `sd`.
```console
uv run tk3u8 username -q uhd
```

When the specified quality is not available, you will not be able to download it, thus printing this error message:

```console
User @username is now streaming live.
Cannot proceed with downloading. The chosen quality (uhd_60) is not available for download.
```

### Wait until live before downloading

If a user is not live yet  but you want the program to start downloading as soon as they go live, you can do this by simply adding `--wait-until-live` option in the command-line just like this:

```console
uv run tk3u8 username --wait-until-live
```

With this command, the program will check if the user is live. If the user is live, the program will attempt to download the stream. Otherwise, the program will wait for the user to go live, and will check again every 30 seconds by default. To change how often it will check, refer to the guide below on [setting the timeout](#setting-timeout-for-checking-live-status).

### Setting timeout for checking live status

This argument is use along with `--wait-until-live` arg. This specifies how many seconds the program will wait before rechecking if the user is live. To use this arg, put `--timeout value` in the command-line, where `value` must be an integer that is at least 1:

```console
uv run tk3u8 username --wait-until-live --timeout=45
```

However, I do not suggest entering a number less than 30 seconds to avoid sending too many requests to the server. Doing this could cause potential problems with the program, and may potentially ban your IP or account (though I'm not sure with this one, but it is better to be safe than sorry).

### Using proxy

You can also use a proxy by specifying the `IP_ADDRESS:PORT` in `--proxy` arg:
```console
# Replace with your actual proxy address
uv run tk3u8 username --proxy 127.0.0.1:80
```

Or you can supply it too in the config file located in `user_data/config.toml`:
```toml
[config]
proxy = "127.0.0.1:80" # Replace with your actual proxy address
```

If there are both proxy address supplied in the command-line arg and in the config file, the former will be used instead.

For most cases, you don't really need to supply proxy and you can just skip this one instead.
