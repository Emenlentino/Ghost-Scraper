# src/myproject/compliance.py
from urllib.parse import urljoin, urlparse
import urllib.robotparser
import logging

logger = logging.getLogger(__name__)

def is_allowed(url, user_agent="*"):
    """
    Check if scraping the URL is permitted according to robots.txt.
    """
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    robots_url = urljoin(base_url, "/robots.txt")
    logger.debug(f"Fetching robots.txt from {robots_url}")

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        allowed = rp.can_fetch(user_agent, url)
        if not allowed:
            logger.warning(f"Scraping is disallowed by robots.txt for URL: {url}")
        return allowed
    except Exception as e:
        logger.exception(f"Error reading robots.txt at {robots_url}. Defaulting to disallow.")
        return False
