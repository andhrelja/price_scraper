"""HTML - <script type="application/ld+json">
==========================================
"""
from typing import Iterable
from bs4 import BeautifulSoup
import json

from .. import models


def html_parser(html_text: str, features='html.parser') -> Iterable:
    soup = BeautifulSoup(html_text, features)
    [meta] = soup.findAll('meta', itemprop='price')
    return meta

def apply(html_text: str, **kwargs) -> None:
    parsed = html_parser(html_text)
    return models.Product(price=float(parsed['content']), **kwargs)
