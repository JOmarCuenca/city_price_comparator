from bs4 import BeautifulSoup
import requests
import pickle
import os.path
import re
from models.cost import Cost
from utils import cost_comparator
from loguru import logger
from datetime import datetime
from utils import ENV_VALUES

from models.city_cost import CityCostData

CURRENCY_REGEX = re.compile(r"(?:[\d,]+)(?:\.\d+)?")


def format_url(city: str, currency: str | None) -> str:
    if currency is None:
        return f"https://www.expatistan.com/cost-of-living/{city.lower()}"
    else:
        return f"https://www.expatistan.com/cost-of-living/{city.lower()}?currency={currency.upper()}"


def get_city_cost_from_file(filepath: str) -> CityCostData | None:
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            city_cost: CityCostData = pickle.load(f)

        logger.debug(f"loaded {len(city_cost.costs)} costs from pickle file")

        if not ((datetime.now() - city_cost.creation_date).days > ENV_VALUES.cost_lifetime):
            logger.debug(
                f"costs from pickle file are still valid")
            return city_cost

        else:
            logger.debug(
                f"costs from pickle file are not valid anymore")


def get_city_costs_from_web(city: str) -> CityCostData:
    url = format_url(city, ENV_VALUES.currency)
    logger.debug(f"Getting costs from {url}")

    html_doc = requests.get(url).text

    soup = BeautifulSoup(html_doc, 'html.parser')

    city_expenses = soup.find("table", class_="comparison single-city")

    city_expenses_rows = city_expenses.find_all("a", class_="downlighted")
    city_prices_rows = city_expenses.find_all("td", class_="price city-1")

    assert (len(city_expenses_rows) == len(cost_comparator.COST_TAGS))

    if len(city_prices_rows) != len(cost_comparator.COST_TAGS):
        city_prices_rows = city_prices_rows[1::2]

    assert (len(city_expenses_rows) == len(city_prices_rows))

    combinacions = zip(city_expenses_rows, city_prices_rows)
    assert (len(city_expenses_rows) == len(cost_comparator.COST_TAGS))

    city_cost = CityCostData(ENV_VALUES.currency, [])

    for expense, (_, price) in zip(cost_comparator.COST_TAGS, combinacions):
        price_string = price.text.strip()
        price = re.findall(CURRENCY_REGEX, price_string)[
            0].replace(",", "")
        city_cost.costs.append(Cost(expense, float(price)))

    return city_cost


@logger.catch(reraise=True)
def get_city_costs(city: str) -> CityCostData:
    pickle_file = f"data/cities/{city}.pkl"

    city_cost = get_city_cost_from_file(pickle_file)

    if city_cost is not None:
        return city_cost

    city_cost = get_city_costs_from_web(city)

    with open(pickle_file, "wb") as f:
        pickle.dump(city_cost, f)

    logger.debug(
        f"saved {len(city_cost.costs)} costs to pickle file from url")

    return city_cost
