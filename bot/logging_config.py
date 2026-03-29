"""Logging configuration for the trading bot"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging(
    log_level: str = "INFO",
    log_dir: str = "logs",
    log_file: str = "trading_bot.log"
) -> None:
    """
    Configure logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
        log_file: Log file name
    """
    # Create logs directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Define log format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    root_logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_path / log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    root_logger.addHandler(file_handler)

    # Silence noisy third-party loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)

    logging.info("Logging configured successfully")
