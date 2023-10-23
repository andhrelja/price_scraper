# import httpx
import requests

def get(url, *args, **kwargs):
    # client = httpx.Client(http2=True)
    response = requests.get(url, *args, **kwargs)
    response.raise_for_status()
    return response
