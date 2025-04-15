import argparse
import importlib
import json
import logging
import os

# from types import ModuleType

from price_scraper import config
from price_scraper import repository

from price_scraper.utils import requests
from price_scraper.utils.io import read_json

# services are dynamically imported by importlib.import_module
from price_scraper import services  # noqa: F401

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

logger = logging.getLogger(__package__)
logger.setLevel(LOG_LEVEL)

PR_NAME = "price_scraper"
PR_DESC = "Scrape pre-configured websites for product prices"
CL_ARGS = (  # https://docs.python.org/3/library/argparse.html
    (
        ("-i", "--config-json-path"),
        dict(help="Products configuration input JSON absolute file path", default=None),
    ),
)


def run_config(cfg):
    cfg = config.Config(
        product_name=cfg["name"],
        product_short_name=cfg["short_name"],
        product_type=cfg["product_type"],
        jobs=list(
            map(
                lambda job: config.Job(**job),
                filter(lambda x: x["is_active"] is True, cfg["jobs"]),
            )
        ),
    )

    for job in cfg.jobs:
        if not job.is_active:
            continue

        SERVICE = None
        html_text = None
        url = "{protocol}{host}{port}/{prefix}".format(**job.asdict())

        if job.protocol == "https://":
            response = requests.get(url, headers=job.headers)
            if not response.ok:
                continue
            logger.info("GET %s - %s", response.status_code, url)

            try:
                module_name = "price_scraper.services." + job.service
                SERVICE = importlib.import_module(module_name)
            except ImportError:
                logger.error("Module '%s' not found. Was it created?", module_name)
                raise

            html_text = response.text

        product = SERVICE.apply(
            html_text,
            name=cfg.product_name,
            short_name=cfg.product_short_name,
            source=job.host,
            product_type=cfg.product_type,
        )
        if not product:
            logger.error("No product found in response")
            continue


if __name__ == "__main__":
    logger.debug(json.dumps(dict(os.environ), indent=2))

    parser = argparse.ArgumentParser(prog=PR_NAME, description=PR_DESC)
    for args, kwargs in CL_ARGS:
        parser.add_argument(*args, **kwargs)

    args = parser.parse_args()
    kwargs = vars(args)
    logger.debug("Parsed args, kwargs: %s, %s", args, json.dumps(kwargs, indent=2))

    cfg = read_json(args.config_json_path)
    total_records = len(repository.Product.list())
    for cfg in cfg["products"]:
        run_config(cfg)
        updated_records = len(repository.Product.list()) - total_records
        logger.info("Updated records: %s", updated_records)
