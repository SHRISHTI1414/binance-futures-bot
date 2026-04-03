"""
Logging configuration for the trading bot.
Sets up both a rotating file handler and a console handler.
"""

import logging
import logging.handlers
import os
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_FILE = LOG_DIR / "trading_bot.log"

_CONFIGURED = False


def setup_logging(level: str = "INFO", log_file: Path = LOG_FILE) -> None:
    """
    Configure root logger with:
      - RotatingFileHandler  → logs/trading_bot.log  (structured, DEBUG+)
      - StreamHandler        → console               (INFO+ by default)

    Safe to call multiple times; subsequent calls are no-ops.
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    log_file.parent.mkdir(parents=True, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # capture everything; handlers filter

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    # --- file handler (rotating, max 5 MB × 3 backups) ---
    fh = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    root.addHandler(fh)

    # --- console handler ---
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, level.upper(), logging.INFO))
    ch.setFormatter(fmt)
    root.addHandler(ch)

    _CONFIGURED = True
    logging.getLogger(__name__).debug("Logging initialised. File: %s", log_file)
