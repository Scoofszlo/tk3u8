This section explains how to use the program through terminal, as well as the commands that you need.

## Executing a command

If you installed the program using system-wide installation (either via [uv](../installation/system-wide-installation-via-uv.md) or [pip](../installation/system-wide-installation-via-pip.md)), here are some sample commands you can execute:


```console
tk3u8 -v
tk3u8 username
tk3u8 username --quality sd
```

However, if you installed the program using [isolated installation via uv](../installation/isolated-installation-via-uv.md), open the terminal from the folder of the installed program and these will be the syntax of sample commands instead:


```console
uv run tk3u8 -v
uv run tk3u8 username
uv run tk3u8 username --quality sd
```

With this method, you have to type `uv run ...` first every time you execute a command.

## Commands

### Downloading a live stream

To download a live stream from a user, simply run:
```console
tk3u8 username
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

After this message appears, you will see many messages popping up, which is from FFmpeg. If this kinda overwhelms you, you don't have to worry about these messages. It is just the library that logs its activity as it is processing and capturing the live stream data.

### Saving the live stream

To stop recording and save the live stream, just hit `Ctrl+C` on your keyboard and wait for FFmpeg to finish and cleanup everything. The stream will be saved in `tk3u8` directory inside your Downloads folder. This folder will contain subfolders for each user you have downloaded from, with a filename, for example, `username-20251225_081015-original.mp4`.

If you save a live stream with a length that is more than an hour, it may take some time for FFmpeg to save, so please be patient.

!!! info
    Please don't spam `Ctrl+C` when saving the live stream. When you attempt to do a single press of it, it may seem to be unresponsive at first but it isn't actually. Just let the FFmpeg handle all of these stuff and you will be fine.

### Choosing stream quality

By default, the program will download the highest quality available. If you want to specify the quality to download, simply choose either `original`, `uhd_60`, `uhd`, `hd_60`, `hd`, `ld`, or `sd`:
```console
tk3u8 username -q uhd
```

When the specified quality is not available, you will not be able to download it, thus printing this error message:

```console
User @username is now streaming live.
Cannot proceed with downloading. The chosen quality (uhd_60) is not available for download.
```

### Wait until live before downloading

If a user is not live yet  but you want the program to start downloading as soon as they go live, you can do this by simply adding `--wait-until-live` option in the command-line just like this:

```console
tk3u8 username --wait-until-live
```

Alternatively, you can also set this up in the config file:

```toml
[config]
wait_until_live = true  # Only accepts `true` or `false` values (case-sensitive)
```

With this command, the program will check if the user is live. If the user is live, the program will attempt to download the stream. Otherwise, the program will wait for the user to go live, and will check again every 30 seconds by default.

To change how often it will check, refer to the guide below on [setting the timeout](#setting-timeout-for-checking-live-status).

!!! tip
    The config file is located in dedicated directories depending on your operating system. Check the [Configuration](../configuration.md#configuring-tk3u8) guide for more details.

### Setting timeout for checking live status

This command specifies how many seconds the program will wait before rechecking if the user is live.

To use this command, put `--timeout value` in the command-line, where `value` must be an integer that is at least 1:

```console
tk3u8 username --wait-until-live --timeout=45
```

Ensure that `--wait-until-live` is supplied in the command-line, where order doesn't matter.

Alternatively, you can also set this up in the config file:
```toml
[config]
wait_until_live = true  # Ensure that this is included and is set to true
timeout = 45  # Must not be enclosed with quotation marks

# Order also doesn't matter here, which applies the same with other config keys
```

I do not suggest entering a number less than 30 seconds to avoid sending too many requests to the server. Doing this could cause potential problems with the program, and may potentially ban your IP or account (though I'm not sure with this one, but it is better to be safe than sorry).

### Force redownloading

If the program happens to stop downloading randomly, you can use this feature to automatically reattempt downloading the live stream as long as the user is still live, so that you don't have to manually re-run the commands just to start downloading again.

To use this, add `--force-redownload` in the command-line:

```console
tk3u8 username --force-redownload
```

Alternatively, you can also set this up in the config file:

```toml
[config]
force_redownload = true
```

### Custom download location

If you don't want to use the default download location of live streams, you can customize it by specifying the location of folder through `--download-dir location`, where `location` is the location of folder you want to save the live stream:

```console
tk3u8 username --download-dir "C:\path\to\download_dir"
```

Enclosing `dir` with quotation marks is recommended so that the system can read the path properly.

### Custom config file location

If you want to specify the custom path to config file to use, simply supply the `--config-file dir` where `dir` is the location of the config file:

```console
tk3u8 username --config-file "C:\path\to\config-file.conf"
```

Enclosing `dir` with quotation marks is recommended so that the system can read the path properly.

### Using proxy

You can also use a proxy by specifying the `IP_ADDRESS:PORT` in `--proxy` arg:

```console
tk3u8 username --proxy 127.0.0.1:80
```

Or you can supply it too in the config file:

```toml
[config]
proxy = "127.0.0.1:80" # Replace with your actual proxy address
```

If there are both proxy address supplied in the command-line arg and in the config file, the former will be used instead.

For most cases, you don't really need to supply proxy and you can just skip this one instead.

### Downloading H.265 encoded live stream

Users can opt to download H.265 (HEVC) encoded streams instead of the default ones (H.264/AVC) for potential file size savings or if one wants slightly better stream quality.

To use this, add the `--use-h265` command:

```console
tk3u8 username --use-h265
```

Alternatively, you can also set this up in the config file:

```toml
[config]
use_h265 = true
```

This option may not always work, typically for the `original` quality, as sometimes H.265 encoded version link that is scraped by the program returns a H.264 version for some reason.

Additionally, for some reason, there is an instance that both video codecs in some streams offer similar file sizes. However, when compared, quality is generally a bit better for H.265 version.

For these reasons, using this option does not guarantee smaller file sizes or the same quality as H.264 ones because it is the source that controls the quality of both video codecs, so I would advise you to compare both to see if there is a file size saving or if there is a quality difference. In that way, you can decide whether to use this option or not.

