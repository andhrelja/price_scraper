import sys
import logging
from price_scraper import repository

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout
)

Repository = repository.IORepository(table_name='product', header=['name', 'short_name', 'source', 'price', 'created_at'])
