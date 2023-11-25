import logging
import requests

logger = logging.getLogger(__name__)

def get(url, *args, **kwargs):
    # client = httpx.Client(http2=True)
    response = requests.get(url, *args, **kwargs)
    if response.status_code != 404:
        response.raise_for_status()
    return response
