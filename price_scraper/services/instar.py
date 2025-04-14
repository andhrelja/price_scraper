"""HTML - <script type="application/ld+json">
==========================================
"""

from typing import Iterable
from bs4 import BeautifulSoup
import json

from price_scraper import models
from price_scraper import repository

SCRIPT_INDEX = 2


def html_parser(html_text: str, features="html.parser") -> Iterable:
    soup = BeautifulSoup(html_text, features)
    scripts = soup.find_all("script", type="application/ld+json")
    return json.loads(scripts[SCRIPT_INDEX].string)


def apply(html_text: str, **kwargs) -> models.Product:
    parsed = html_parser(html_text)
    if not parsed:
        return parsed
    product = models.Product(price=parsed["offers"]["price"], **kwargs)
    repository.Product.add(product.asdict())
    return product
