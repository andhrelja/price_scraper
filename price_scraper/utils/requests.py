import json
import logging
import requests

logger = logging.getLogger(__name__)


def get(url, *args, **kwargs):
    # client = httpx.Client(http2=True)
    response = requests.get(url, *args, **kwargs)
    logger.debug("args: %s", json.dumps(args, indent=2))
    logger.debug("kwargs: %s", json.dumps(kwargs, indent=2))
    logger.debug("response: %s", json.dumps(response, default=str, indent=2))
    if response.status_code != 404:
        response.raise_for_status()
    return response
