# src/myproject/logger.py
import logging
from rich.logging import RichHandler
import sentry_sdk
from myproject.config import SENTRY_DSN

# Initialize Sentry (use environment variables for production secrets)
sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=1.0)

def setup_logging(level=logging.DEBUG):
    """
    Configures logging to use RichHandler for colorful, structured logs.
    All exceptions logged will also be sent to Sentry.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s :: %(levelname)s :: %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S]",
        handlers=[RichHandler()]
    )
