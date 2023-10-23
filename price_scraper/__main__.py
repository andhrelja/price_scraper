import importlib
import logging
from io import StringIO

from price_scraper.utils.io import read_json
from price_scraper.utils import requests

from price_scraper import config
from price_scraper import services
from price_scraper import repository

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)

Repository = repository.io.IORepository(
    file_name='../data/products',
    mode='a+',
    s_io=StringIO()
)
Repository.add('name,source,price,created_at')

# if __name__ == '__main__':
configs = read_json(config.BASE_DIR / 'config.json')
for product_cfg in configs['products']:
    jobs = map(lambda job: config.Job(**job), product_cfg['jobs'])
    cfg = config.Config(product_name=product_cfg['name'], 
                        jobs=list(jobs))

    for job in cfg.jobs:
        if not job.is_active:
            continue
        url = "{protocol}{host}{port}/{prefix}".format(**job.asdict())
        response = requests.get(url)
        
        try:
            module_name = 'price_scraper.services.' + job.service
            service = importlib.import_module(module_name)
        except ImportError:
            logger.error("Module '%s' not found. Was it created?", module_name)
            raise
        
        product = service.apply(response.text, name=cfg.product_name, source=job.host)
        Repository.add(product.asrow())
Repository.list()
