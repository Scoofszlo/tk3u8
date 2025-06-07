from importlib.metadata import version
from tk3u8.constants import APP_NAME


def display_version() -> str:
    return f"{APP_NAME} v{version(APP_NAME)}"
