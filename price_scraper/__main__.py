import importlib
import logging
import json

from price_scraper.utils.io import read_json
from price_scraper.utils import requests

from price_scraper import config
from price_scraper import Repository
from price_scraper import services

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    configs = read_json(config.BASE_DIR / 'config.json')
    for product_cfg in configs['products']:
        jobs = map(lambda job: config.Job(**job), product_cfg['jobs'])
        cfg = config.Config(product_name=product_cfg['name'],
                            product_short_name=product_cfg['short_name'], 
                            jobs=list(jobs))

        for job in cfg.jobs:
            if not job.is_active:
                continue
            url = "{protocol}{host}{port}/{prefix}".format(**job.asdict())
            logger.info("GET %s", url)
            response = requests.get(url, headers=job.headers)
            
            try:
                module_name = 'price_scraper.services.' + job.service
                service = importlib.import_module(module_name)
            except ImportError:
                logger.error("Module '%s' not found. Was it created?", module_name)
                raise
            
            product = service.apply(response.text, name=cfg.product_name, short_name=cfg.product_short_name, source=job.host)
            Repository.add(product.asdict())
    logger.info(json.dumps(Repository.list(), indent=1, default=str))
