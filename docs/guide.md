## Grabbing and setting up `sessionid_ss` and/or `tt_target_idc`

To fix issues related to `WAFChallengeError`, `HLSLinkNotFoundError`, and `StreamDataNotFoundError`, you can supply a value to `tt_target_idc` in the config file. If it doesn't work, try to supply both `sessionid_ss` and `tt_target_idc`. 

To grab these values, do the following:

1. In your browser, go to https://tiktok.com and login your account.
2. Open Inspect Element in your browser.
3. Go to Cookies section:
    - For Google Chrome users, click the `Application`. If you can't see it, click the `>>`.
    - For Firefox users, click the `Storage`. If you can't see it, click the `>>`.
4. On Cookies dropdown, click the `https://tiktok.com`.
5. On the right hand side, find the `sessionid_ss`, as well as the `tt-target-idc`.
6. Get those values and paste it in your config file located in your [user data](configuration.md) folder.
7. Your config should look like this.
    ```toml
    [config]
    sessionid_ss = "0124124abcdeuj214124mfncb23tgejf"  # Include this if only supplying tt-target-idc doesn't work
    tt_target_idc = "alisg"
    ```
8. Save it.

!!! warning
    Do not share this to anyone as this is a sensitive data tied to your TikTok account.
