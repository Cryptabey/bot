from pathlib import Path
import logging
import sys
from typing import Optional

PROJECT_ROOT = Path(__file__).parents[3]  # Go up 3 levels to reach project root

class Formatter(logging.Formatter):
    grey = "\x1b[38;1m"
    white = "\x1b[37;1m"
    yellow = "\x1b[33;1m"
    red = "\x1b[31;1m"
    purple = "\x1b[35;1m"
    reset = "\x1b[0m"
    format_string = "[{asctime}] [{levelname:<8}] {name}: {message}"

    FORMATS = {
        logging.DEBUG: grey + format_string + reset,
        logging.INFO: white + format_string + reset,
        logging.WARNING: yellow + format_string + reset,
        logging.ERROR: red + format_string + reset,
        logging.CRITICAL: purple + format_string + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


def install(name: str, level: str = "INFO") -> None:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(Formatter())
    logger.addHandler(console_handler)

    # File handler
    log_path = PROJECT_ROOT / "logs" / f"{name}.log"
    log_path.parent.mkdir(exist_ok=True)  # Create logs directory if it doesn't exist
    file_handler = logging.FileHandler(str(log_path), encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}",
            "%Y-%m-%d %H:%M:%S",
            style="{",
        )
    )
    logger.addHandler(file_handler)

    return None


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name)

