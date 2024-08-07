import json
import logging
import requests

logger = logging.getLogger(__name__)


def get(url, *args, **kwargs):
    # client = httpx.Client(http2=True)
    try:
        response = requests.get(url, *args, **kwargs)
    except requests.exceptions.ConnectTimeout as e:
        logger.warning("Connection timeout occured for %s", url)
        return
    logger.debug("args: %s", json.dumps(args, indent=2))
    logger.debug("kwargs: %s", json.dumps(kwargs, indent=2))
    logger.debug("response: %s", json.dumps(response, default=str, indent=2))
    if response.status_code != 404:
        response.raise_for_status()
    if response.status_code == 404:
        logger.warning("Page not found: %s", url)
        return
    return response
