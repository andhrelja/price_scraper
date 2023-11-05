import importlib
import logging
import os
import json
import argparse

from price_scraper.utils.io import read_json
from price_scraper.utils import requests

from price_scraper import config
from price_scraper import Repository
from price_scraper import services

logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)

PR_NAME = 'price_scraper'
PR_DESC = 'Scrape pre-configured websites for product prices'
CL_ARGS = (
    (('-l', '--all'), dict(action="store_true", 
                           help='Scrape all products',)),
)

def all_list(configs):
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

CL_MAPS = {
    'all': all_list
}
    

if __name__ == '__main__':
    logger.info(json.dumps(dict(os.environ), indent=2))
    
    configs = read_json(config.BASE_DIR / 'config.json') # TODO: imporlib_resource
    parser = argparse.ArgumentParser(prog=PR_NAME, description=PR_DESC)
    for args, kwargs in CL_ARGS:
        logger.debug(args, kwargs)
        parser.add_argument(*args, **kwargs)
    args = parser.parse_args()
    kwargs = vars(args)
    logger.debug("Parsed args: %s", args)
    
    for fn in CL_MAPS:
        if getattr(args, fn):
            ex = CL_MAPS[fn]
            ex(configs)
    