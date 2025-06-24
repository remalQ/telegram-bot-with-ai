# bot/logger.py

import logging


def setup_logger() -> None:
    """Настраивает базовое логгирование."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
