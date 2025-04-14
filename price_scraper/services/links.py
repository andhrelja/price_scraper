"""HTML - <script type="application/ld+json">
==========================================
"""

from typing import Iterable
from bs4 import BeautifulSoup

from price_scraper import models
from price_scraper import repository


def html_parser(html_text: str, features="html.parser") -> Iterable:
    soup = BeautifulSoup(html_text, features)
    [meta] = soup.findAll("meta", itemprop="price")
    return meta


def apply(html_text: str, **kwargs) -> models.Product:
    parsed = html_parser(html_text)
    if not parsed:
        return parsed
    product = models.Product(price=float(parsed["content"]), **kwargs)
    repository.Product.add(product.asdict())
    return product
