import argparse
import importlib
import json
import logging
import os

from price_scraper import config
from price_scraper import Repository

from price_scraper.utils import requests
from price_scraper.utils.io import read_json

# from price_scraper import services
# services are dynamically imported by importlib.import_module


logger = logging.getLogger(__package__)
logger.setLevel(logging.INFO)

PR_NAME = "price_scraper"
PR_DESC = "Scrape pre-configured websites for product prices"
CL_ARGS = (
    (
        ("-l", "--all"),
        dict(
            action="store_true",
            help="Scrape all products",
        ),
    ),
)


def scrape_all_products(configs):
    for product_cfg in configs["products"]:
        jobs = map(lambda job: config.Job(**job), product_cfg["jobs"])
        cfg = config.Config(
            product_name=product_cfg["name"],
            product_short_name=product_cfg["short_name"],
            jobs=list(jobs),
        )

        for job in cfg.jobs:
            if not job.is_active:
                continue
            url = "{protocol}{host}{port}/{prefix}".format(**job.asdict())
            response = requests.get(url, headers=job.headers)
            logger.info("GET %s - %s", response.status_code, url)
            if response.status_code == 404:
                logger.warning("Page not found: %s", url)
                continue

            try:
                module_name = "price_scraper.services." + job.service
                service = importlib.import_module(module_name)
            except ImportError:
                logger.error("Module '%s' not found. Was it created?", module_name)
                raise

            product = service.apply(
                response.text,
                name=cfg.product_name,
                short_name=cfg.product_short_name,
                source=job.host,
            )
            Repository.add(product.asdict())

    logger.info("Updated records: %s", len(Repository.list()))


CL_MAPS = {"all": scrape_all_products}


if __name__ == "__main__":
    logger.debug(json.dumps(dict(os.environ), indent=2))

    configs = read_json(config.BASE_DIR / "config.json")
    parser = argparse.ArgumentParser(prog=PR_NAME, description=PR_DESC)
    for args, kwargs in CL_ARGS:
        logger.debug(args, kwargs)
        parser.add_argument(*args, **kwargs)
    args = parser.parse_args()
    kwargs = vars(args)
    logger.debug("Parsed args: %s", args)

    for fn in CL_MAPS:
        if getattr(args, fn):
            exec = CL_MAPS[fn]
            exec(configs)
