"""HTML - <script type="application/ld+json">
==========================================
"""

from typing import Iterable
from bs4 import BeautifulSoup

from price_scraper import models
from price_scraper import repository

SCRIPT_INDEX = 0


def html_parser(html_text: str, features="html.parser") -> Iterable:
    soup = BeautifulSoup(html_text, features)
    offer = soup.find("div", id="offer-with-min-price")
    price = offer.find_next("div", class_="offer__price")
    price = price.text.replace("€", "").strip()
    price = price.replace(".", "")
    price = price.replace(",", ".")
    return price


def apply(html_text: str, **kwargs) -> models.Product:
    parsed = html_parser(html_text)
    if not parsed:
        return parsed
    product = models.Product(price=parsed, **kwargs)
    repository.Product.add(product.asdict())
    return product
