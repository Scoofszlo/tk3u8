from dataclasses import dataclass
from enum import Enum


@dataclass
class StreamLink:
    quality: str
    link: str


class StatusCode(Enum):
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    FORBIDDEN = 403
    UNAUTHORIZED = 401
    SERVER_ERROR = 500
    GATEWAY_TIMEOUT = 504
    SERVICE_UNAVAILABLE = 503


class Quality(Enum):
    ORIGINAL = "original"
    UHD_60 = "uhd_60"
    UHD = "uhd"
    HD_60 = "hd_60"
    HD = "hd"
    LD = "ld"
    SD = "sd"


class LiveStatus(Enum):
    LIVE = "live"
    PREPARING_TO_GO_LIVE = "preparting_to_go_live"
    OFFLINE = "offline"


class OptionKey(Enum):
    SESSIONID_SS = "sessionid_ss"
    TT_TARGET_IDC = "tt_target_idc"
    PROXY = "proxy"
    USERNAME = "username"
    QUALITY = "quality"
    WAIT_UNTIL_LIVE = "wait_until_live"
    TIMEOUT = "timeout"
    FORCE_REDOWNLOAD = "force_redownload"
    USE_H265 = "use_h265"


@dataclass
class Messages:
    """A collection of message templates used throughout the program."""
    user_offline: str = "User [b]@{username}[/b] is [red]currently offline[/red]."
    preparing_to_go_live: str = "User [b]@{username}[/b] is preparing to go live. Try again in a minute or two to be able to download the stream."
    user_is_now_live: str = "User [b]@{username}[/b] is now [b][green]streaming live[/b][/green]."
    reattempting_download: str = "[grey50]Reattempting download for user [b]@{username}[/b]...[/grey50]"
    awaiting_to_go_live: str = "User [b]@{username}[/b] is [red]currently offline[/red]. Awaiting [b]@{username}[/b] to start streaming..."
    quality_not_available: str = "[grey50]Cannot proceed with downloading. The chosen quality [b]({quality})[/b] is not available for download.[/grey50]"
    empty_stream_link_error: str = "Cannot proceed with downloading as the stream link was somehow unavailable during stream data extraction. Try downloading again."
    starting_download: str = "Starting download for user [b]@{username}[/b] [grey50](quality: {stream_link.quality}, stream Link: {stream_link.link})[/grey50]"
    finished_downloading: str = "[green]Finished downloading[/green] [b]{filename}.mp4[/b] [grey50](saved at: {filename_with_download_dir})[/grey50]"
    cancelled_checking_live: str = "[grey50]Checking cancelled by user. Exiting...[/grey50]"
    retrying_to_check_live: str = "[bold yellow]Retrying in {remaining} seconds{seconds_extra_space}"
    ongoing_checking_live: str = "[grey50]Checking...[/grey50]"
    redownloading_notice: str = "You are using the [yellow]FORCE_REDOWNLOAD[/yellow] option. You have {remaining} seconds to exit the program, or the program will attempt to redownload again."
    processing_data: str = "Processing data..."
    processing_data_for_user: str = "Processing data for user @{username}"
    trying_extractor: str = "Trying extractor #{pos}: {extractor_class_name}"
    current_extractor_failed: str = "[grey50]Extractor #{current_extr_pos} ({current_extr_name}) failed due to [b]{exc_name}[/b]. Trying next extractor method (Extractor #{next_extr_pos})[grey50]"
    last_extractor_failed: str = "[grey50]Extractor #{current_extr_pos} ({current_extr_name}) failed due to [b]{exc_name}[/b]. No more extractors to be used. The program will now exit.[grey50]"
    invalid_username: str = (
        "The username [b]{username}[/b] is [red]invalid[/red]. Ensure the username is at least 2wd "
        "characters long, contains only lowercase letters, numbers, underscores, and/or periods, "
        "and is up to 24 characters in length."
    )
    no_username_entered: str = "No username was entered. Please provide a valid username."
    account_not_found: str = "User [b]@{username}[/b] is likely a private account, or it doesn't exist at all."
    fetched_content: str = "Fetched content for user @{username}: {content}"
    retrieved_stream_links: str = "Retrieved stream links for user @{username}: {stream_links}"
    extracted_stream_data: str = "Extracted stream_data for user @{username}: {stream_data}"
    extracted_status_code: str = "Extracted status_code for user @{username}: {status_code}"
    exiting_download_reattempt: str = "[grey50]Reattempting download cancelled by user. Exiting...[/grey50]"
    invalid_option_key: str = "Option key [b]{key}[/b] is invalid. Please ensure you entered a valid option key in your config file."
    config_file_decoding_error: str = "Error decoding config file due to: '[yellow]{exc_msg}[/yellow]'"
    config_file_loading_error: str = "Config file path is not valid. Ensure that the path is correct and the config file actually exists."
    config_file_parsing_error: str = "Error parsing config file."
    invalid_cookie_key_error: str = "Cookie key '{key}' is invalid. Ensure that the cookie key is either 'sessionid_ss' or 'tt_target_idc'."


APP_NAME = "tk3u8"


# Default configuration settings
DEFAULT_CONFIG = {
    "config": {
        OptionKey.SESSIONID_SS.value: "",
        OptionKey.TT_TARGET_IDC.value: "",
        OptionKey.PROXY.value: ""
    }
}


# Default user agent
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]
