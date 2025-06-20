from datetime import datetime
import logging
import os
from platformdirs import user_data_path
from tk3u8.constants import APP_NAME


def setup_logging(log_level: str | None) -> None:
    if not log_level:
        logging.basicConfig(level=logging.CRITICAL + 1)  # Avoid printing of log messages
        return

    log_directory = os.path.join(user_data_path(), APP_NAME, "logs")

    if not os.path.exists(log_directory):
        os.makedirs(log_directory, exist_ok=True)

    log_filename = f"logs-{datetime.now().strftime('%Y%m%d')}.log"
    log_file = os.path.join(log_directory, log_filename)

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S%z'))

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler]
    )
