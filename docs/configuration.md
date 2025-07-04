This section explains how to configure `tk3u8` using the `tk3u8.conf` file, as well as some guides for setting up each key and value.

## Configuring tk3u8

tk3u8 can be configured through config file so that you don't have to specify some commands through command-line every time. The main configuration file is located at various locations:

- Windows: `%LocalAppData%/tk3u8/tk3u8.conf`
- Linux: `/home/username/.local/share/tk3u8/tk3u8.conf`
- macOS: `/Users/username/Library/Application Support/tk3u8/tk3u8.conf`

This config file will be created once you have started downloading a live stream.

By default, the program will load the config files from these directories. However, if you want to specify the custom path of config file, simply supply the location of the config file through [command-line](usage/using-through-terminal.md#custom-config-file-location), or if you use it through [scripts](usage/using-through-a-script.md#custom-config-file-location), you put that upon class instantiation.

## Config file structure

Here's what it looks like:

```toml
[config]
sessionid_ss = "0124124abcdeuj214124mfncb23tgejf"
wait_until_live = false
timeout = 45
```
The `sessionid_ss`, `wait_until_live`, and `proxy` are what we called the <b>keys</b>. The corresponding values, i.e., string, boolean, and integer, are what we called <b>values</b>. All of these key-value pairs are group under `config`, which is called <b>table</b>.

## Precedence between config and CLI commands

Command-line options always take precedence over values set in the config file. This means any option specified from the CLI will override the corresponding values in the config file.

For example, if you have a `timeout = 45` in the config file but you specify `--timeout 100` on the command-line, the value 100 will be used.

## Supported config keys

### sessionid_ss

Type: `string`

This key is used from your `sessionid_ss` cookie. You can use this to bypass certain [restrictions](issues.md) when downloading streams. The value should be a 32-character string, which you can [obtain from your browser's TikTok cookies](guide.md#grabbing-and-setting-up-sessionid_ss-andor-tt_target_idc).

Example:

```toml
[config]
sessionid_ss = "0124124abcdeuj214124mfncb23tgejf"
```

### tt_target_idc

Type: `string`

This key is used from your `tt_target_idc` cookie. You can use this to bypass certain [restrictions](issues.md) when downloading streams. The value can be [obtained from your browser's TikTok cookies](guide.md#grabbing-and-setting-up-sessionid_ss-andor-tt_target_idc).

Example:

```toml
[config]
tt_target_idc = "alisg"
```

### wait_until_live

Type: `bool` (boolean)

This key determines whether the program should wait for the user to go live before attempting to download. 

Set this to `true` to keep checking until the user goes live. Otherwise, the program will just exit normally.

Example:

```toml
[config]
wait_until_live = true  # Remember this is case-sensitive
```

### timeout

Type: `int` (integer)

This key sets the timeout duration (in seconds) on how long the program will wait before reching if the user is live. This value accepts an integer that is at least 1.

Example:

```toml
[config]
timeout = 45  # Remember int musn't be enclosed with quotation marks
```

### force_redownload

Type: `bool` (boolean)

This key determines whether the program should reattempt to redownload the live stream. This is usually used when FFmpeg suddenly stops downloading the live stream.

Set this to `true` to allow download reattempt.

Example:

```toml
[config]
force_redownload = true
```

### use_h265

Type: `bool` (boolean)

This key allows the program to download the HEVC (H.265) encoded stream instead of the default ones, which is the AVC (H.264).

Set this to `true` to download HEVC-encoded stream.

Example:

```toml
[config]
use_h265 = true
```

### proxy

Type: `string`

This key allows you to specify a proxy server for network requests. The value should be a valid proxy URL (e.g., `http://127.0.0.1:8080`). Leave it empty if you do not want to use a proxy.

Example:

```toml
[config]
proxy = "http://127.0.0.1:8080"
```
