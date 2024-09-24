"""HTML - <script type="application/ld+json">
==========================================
"""

from typing import Iterable
from bs4 import BeautifulSoup
import json

from .. import models

SCRIPT_INDEX = 1


def html_parser(html_text: str, features="html.parser") -> Iterable:
    soup = BeautifulSoup(html_text, features)
    scripts = soup.findAll("script", type="application/ld+json")
    try:
        return json.loads(scripts[SCRIPT_INDEX].string)
    except IndexError:
        return {}


def apply(html_text: str, **kwargs) -> None:
    parsed = html_parser(html_text)
    if not parsed:
        return parsed
    return models.Product(price=parsed["offers"]["price"], **kwargs)
