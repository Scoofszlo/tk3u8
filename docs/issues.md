This page covers the issues that may arise within the usage of the program, explains what causes them, and what you should do.


## `WAFChallengeError` occasionally pops up

Occasionally, when you download a stream from a user, you may encounter `WAFChallengeError` raised by the program. There is no solid evidence for this one, but one possible reason is that it is just the site's prevention of handling bot requests to their server.

Based on testing so far, here are some possible temporary fixes.:

- Wait for a minute or two and try again.
- Use a VPN; or
- Set up `session_id_ss` and `tt_target_idc` in the config file. [[Guide]](guide.md#grabbing-and-setting-up-sessionid_ss-andor-tt_target_idc)

## `HLSLinkNotFoundError` occurs

There are three scenarios in why this error happens:

- It just sometimes pops up.
- If you live in the US region (or other nearby countriy), or if you set `tt_target_idc` to `useast2a` in the config file.
- You are downloading a stream from someone who lives in a different continent or region from you (e.g., you are somewhere from Southeast Asia but you are downloading a stream from Europe or US region.)

As I have observed, no stream links appear for any quality (original, uhd, hd, sd, etc.), causing this error to occur. Below is an example from what gets scraped from source (with actual data removed).


```json
{
    "common": { "..." },
    "data": {
        "sd": {
            "main": {
                "flv": "https://pull-q5-sg01.fcdn.eu.tiktokcdn.com/stage/stream-0000000000000000000_sd.flv?expire=0000000000&sign=00000000000000000000000000000000",
                "hls": "",  // There should be an HLS link here, but the source only provides an empty string.
                "other_keys": "..."
            }
        },
        "ld": {
            "main": {
                "flv": "https://pull-q5-sg01.fcdn.eu.tiktokcdn.com/stage/stream-0000000000000000000_sd.flv?expire=0000000000&sign=00000000000000000000000000000000",
                "hls": "",  // There should be an HLS link here, but the source only provides an empty string.
                "other_keys": "..."
            }
        },
        "other_qualities": { "..." }
    }
}
```

To fix this issue:

- For the first scenario, just retry again.
- For the second scenario, use a VPN and/or avoid setting `tt_target_idc` in the config file. If you are using a VPN, the server that you should connect could be anywhere, as long as it is not the US servers or one nearby.
    - Alternatively, if one prefers not using VPN, you can set the `tt_target_idc` to any valid values such as `alisg` or `useast1a`. These are the valid values that I have tested and have work so far.
- For the third scenario, use a VPN and connect to a server that is the same with the location of the user you are downloading from. 

The guide for setting up `tt_target_idc` in your config file is available [here](./guide.md#grabbing-and-setting-up-sessionid_ss-andor-tt_target_idc).

## Program randomly finishes downloading

You may encounter issues wherein the program will stop downloading, with a message saying `Finished downloading username-20250101_120015-original.mp4...` even if you didn't do anything. My guess is that it could be a source issue. If the user's live stream is unstable, FFmpeg may abrutply end the downloading of stream. That's the pattern that I have observed for some time, but I still need some confirmation for this one. 

This issue can't be fixed directly with this program. However, I've implemented a feature called force redownloading, which dictates the program to reattempt downloading again as long as the user is still live. Once the user goes offline, the live stream will be saved and the program will exit normally.

To use force redownloading, you can use [`--force-redownload`](./usage/using-through-terminal.md#force-redownloading) command through your terminal or specify [`force_redownload=True`](./usage/using-through-a-script.md#force-redownloading) in the parameter of `download()` in your script.

## `StreamDataNotFoundError` occurs

The cause of this exception is not yet confirmed due to limited testing, but I suspect that this is due to live restrictions. To fix this, you have to supply `sessionid_ss` in your [config file](guide.md#grabbing-and-setting-up-sessionid_ss-andor-tt_target_idc).

## Sometimes H.265 encoded stream has the same size as the default ones

For some context, in video compression world, to save a lot of space, H.265 is the video codec that is used by many people as it offers 30-40% space savings at the same quality as H.264. For that reason, you will be tempted to use this to save space, hence the availability of option `--use-h265`.

However, there is a tendency that if you tried downloading the H.265 and H.264 encoded live streams, you might noticed both has same file sizes. In this case, it might be better to compare both videos and see which one has the better quality. Based on my past testings, H.265 encoded ones has slightly better quality as there is some detail loss with H.264 version when zoomed in.

Personally, I would recommended choosing H.265 for that particular case but you should still check it by yourself just to be sure.
