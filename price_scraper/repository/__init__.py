from .io import IORepository
from .inmemory import InMemoryRepository
from .sqlite import SqLiteRepository

import sys
import logging
from price_scraper import repository

from price_scraper.models import Product

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

Product = repository.IORepository(table_name="product", header=Product.header())

__all__ = [
    "IORepository",
    "InMemoryRepository",
    "SqLiteRepository",
    "Product",
]
