"""HTML - <script type="application/ld+json">
==========================================
"""

from typing import Iterable
from bs4 import BeautifulSoup
import json
import logging
import os

from price_scraper import models
from price_scraper import repository

SCRIPT_INDEX = 0


logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.DEBUG))

## mediaworld.com
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'en-US,en;q=0.9',
#     'Sec-Ch-Ua': '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
#     'Sec-Ch-Ua-Mobile': '?0',
#     'Sec-Ch-Ua-Platform': '"Windows"',
#     'Sec-Fetch-Dest': 'document',
#     'Sec-Fetch-Mode': 'navigate',
#     'Sec-Fetch-Site': 'none',
#     'Sec-Fetch-User': '?1',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46'
# }


def html_parser(html_text: str, features="html.parser") -> Iterable:
    soup = BeautifulSoup(html_text, features)
    scripts = soup.find_all("script", type="application/ld+json")
    return json.loads(scripts[SCRIPT_INDEX].string)


def apply(html_text: str, **kwargs) -> models.Product:
    parsed = html_parser(html_text)
    if not parsed:
        return parsed
    product = models.Product(price=parsed["object"]["offers"]["price"], **kwargs)
    repository.Product.add(product.asdict())
    return product
