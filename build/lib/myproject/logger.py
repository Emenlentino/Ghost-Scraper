# src/myproject/logger.py

import logging
from rich.logging import RichHandler

def setup_logging(level=logging.DEBUG):
    """
    Configures the logging system to use RichHandler.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s :: %(levelname)s :: %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]",
        handlers=[RichHandler()]
    )
