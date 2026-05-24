import logging
import sys
from config import Config

def setup_logger(config: Config = None):
    if config is None:
        config = Config()

    log_level_str = config.get("logging", "level", default="INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    log_file = config.get("logging", "log_file", default="wa_automate.log")
    log_to_console = config.get("logging", "log_to_console", default=True)

    logger = logging.getLogger("WA_Automate")
    logger.setLevel(log_level)

    # Prevent duplicating handlers if setup is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File Handler
    try:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Failed to set up file logger: {e}")

    # Console Handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Global default logger
logger = setup_logger()
