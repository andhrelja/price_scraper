"""HTML - <script type="application/ld+json">
==========================================
"""

import logging
from typing import Iterable
from bs4 import BeautifulSoup, NavigableString

from price_scraper import models
from price_scraper.utils import requests


logger = logging.getLogger(__name__)


def _rename_title(title: str) -> str:
    title = title.replace(" ", "_")
    title = title.replace(":", "")
    return title.strip().lower()


def _filter_empty_children(soup: BeautifulSoup) -> list[BeautifulSoup]:
    children = getattr(soup, "children", [])
    return list(filter(lambda x: not isinstance(x, NavigableString), children))


def parse_urls(soup: BeautifulSoup) -> list:
    divs = soup.find_all("div", class_="content_titlebar_left")
    return [div.a["href"] for div in divs]


def parse_item_details(soup: BeautifulSoup) -> dict:
    item_details = soup.find("div", class_="items_more_details")
    if item_details is None:
        logger.warning("Item details not found")
        return {}
    titles = [item.text.strip() for item in item_details.find_all("dt", class_="title")]
    values = [item.text.strip() for item in item_details.find_all("dd", class_="value")]
    return dict(zip(map(_rename_title, titles), values))


def parse_description(soup: BeautifulSoup) -> str:
    item_description = soup.find("div", class_="listings_more_description")
    if item_description is None:
        logger.warning("Item description not found")
        return ""
    description = item_description.find("div", class_="pages_content")
    return description.text.strip()


def parse_extras(soup: BeautifulSoup) -> dict[str, list[str]]:
    extras = {}
    item_extras = soup.find("div", class_="items_more_attributes")
    for child in _filter_empty_children(item_extras):
        title = _rename_title(
            child.find("span", class_="items_more_attributes_group_title").text
        )
        extras[title] = {}
        for child in _filter_empty_children(child.find("ul")):
            spans = child.find_all("span")
            subtitle = spans[0].text
            if len(spans) > 1:
                extras[title][subtitle] = spans[1].text.strip()
            else:
                extras[title][subtitle] = ""
    return extras


def html_parser(html_text: str, features="html.parser") -> Iterable:
    soup = BeautifulSoup(html_text, features)
    urls = parse_urls(soup)
    real_estates = []

    for url in urls:
        logger.info("GET %s", url)
        response = requests.get(url)
        if response.status_code != 200:
            logger.warning("Failed to fetch %s with response:\n%s", url, response.text)
            continue

        soup = BeautifulSoup(response.text, features)
        item_details = parse_item_details(soup)
        item_description = parse_description(soup)
        item_extras = parse_extras(soup)

        real_estates.append(
            dict(
                name=f"{item_details.get("lokacija", "")}, {item_details.get("tip_stana", "")}, {item_details.get("površina")}, {item_details.get("cijena", "")}",
                url=url,
                description=item_description,
                type=item_details.get("tip_stana"),
                type_extended="\n".join(
                    map(" ".join, item_extras.get("svojstva_nekretnine", {}).items())
                ),
                location=item_details.get("lokacija"),
                price=item_details.get("cijena"),
                square_m=item_details.get("površina"),
                square_property_m=item_details.get("površina_okućnice"),
                wood_shed="\n".join(
                    list(
                        filter(
                            lambda x: x == "Drvarnica",
                            item_extras.get("oprema_nekretnine", {}).keys(),
                        )
                    )
                    + list(
                        filter(
                            lambda x: x == "Skladišni prostor",
                            item_extras.get("oprema_nekretnine", {}).keys(),
                        )
                    )
                ),
                garage=item_extras.get("garage"),
                parking="\n".join(
                    map(" ".join, item_extras.get("parking", {}).items())
                ),
                balcony=item_extras.get("oprema_nekretnine", {}).get(
                    "Površina balkona", None
                ),
            )
        )
    return real_estates


def apply(html_text: str, **kwargs) -> None:
    parsed = html_parser(html_text)
    estates = []
    for estate in parsed:
        estates.append(models.RealEstate(**estate, **kwargs))
    return estates
