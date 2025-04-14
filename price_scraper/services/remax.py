"""HTML - <script type="application/ld+json">
==========================================
"""

from typing import Iterable
from bs4 import BeautifulSoup
import json

from price_scraper import models
from price_scraper import repository


SCRIPT_INDEX = 0


def html_parser(html_text: str, features="html.parser") -> Iterable:
    soup = BeautifulSoup(html_text, features)
    scripts = soup.find_all("script", type="application/ld+json")
    json_str = scripts[SCRIPT_INDEX].string
    json_str = json_str.replace("\n\n", "\\n")
    json_str = json_str.replace(".\n", ".\\n")
    return json.loads(json_str)


def apply(html_text: str, **kwargs) -> None:
    parsed = html_parser(html_text)
    if not parsed:
        return parsed
    product = models.Product(price=parsed["offers"]["price"], **kwargs)
    repository.Product.add(product.asdict())
    return product
