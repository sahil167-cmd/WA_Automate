import logging
import sys
from logging.handlers import RotatingFileHandler
from .config import Config

def setup_logger(config: Config = None) -> logging.Logger:
    if config is None:
        try:
            config = Config()
        except Exception:
            # Fallback configuration in case Config fails to instantiate
            config = None

    if config:
        log_level_str = config.get("logging", "level", default="INFO").upper()
        log_file = config.get("logging", "log_file", default="wa_automate.log")
        log_to_console = config.get("logging", "log_to_console", default=True)
    else:
        log_level_str = "INFO"
        log_file = "wa_automate.log"
        log_to_console = True

    log_level = getattr(logging, log_level_str, logging.INFO)

    logger = logging.getLogger("WA_Automate")
    logger.setLevel(log_level)

    # Prevent duplicating handlers if setup is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Rotating File Handler (Max 5MB file size, keeping up to 3 backups)
    try:
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=5 * 1024 * 1024, 
            backupCount=3, 
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Failed to set up rotating file logger: {e}")

    # Console Handler
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

# Global default logger
logger = setup_logger()
