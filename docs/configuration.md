This section explains how to configure `tk3u8` using the `tk3u8.conf` file, as well as some guides for setting up each key and value.

## The configuration file: `tk3u8.conf`

The main configuration file is located at various locations:

- Windows: `%LocalAppData%/tk3u8/tk3u8.conf`
- Linux: `/home/username/.local/share/tk3u8/tk3u8.conf`
- macOS: `/Users/username/Library/Application Support/tk3u8/tk3u8.conf`

This config file will be created once you have started downloading a live stream. Alternatively, you can manually create one with this format:

```toml
[config]
sessionid_ss = ""      # Your TikTok sessionid_ss cookie
tt_target_idc = ""     # Your TikTok tt-target-idc cookie
proxy = ""             # Replace with your actual proxy address, or leave blank
```

- **sessionid_ss**: (Optional) Used to bypass certain restrictions.
- **tt_target_idc**: (Optional) Used to change the server for retrieving source data.
- **proxy**: (Optional) Set a proxy in the format `IP_ADDRESS:PORT`.

## Guides

### Grabbing and setting up `sessionid_ss` and/or `tt_target_idc`

To fix issues related to `WAFChallengeError`, `StreamLinkNotFoundError`, and `StreamDataNotFoundError`, you can supply a value to `tt_target_idc` in the config file. If it doesn't work, try to supply both `sessionid_ss` and `tt_target_idc`. To grab these values, do the following:

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
    tt_target_idc = "alisg"
    ```
8. Save it.

Remember do not share this to anyone as this is a sensitive data tied to your TikTok account.

### Setting your own proxy

To set up the proxy, specify the value in `IP_ADDRESS:PORT` format.

```toml
[config]
proxy = "127.0.0.1:80"  # Replace with your actual proxy address
```
