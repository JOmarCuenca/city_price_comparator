from bs4 import BeautifulSoup
import requests
import pickle
import os.path
import re
from models.cost import Cost
from utils import cost_comparator
from loguru import logger

from models.city_cost import CityCostData

CURRENCY_REGEX = re.compile(r"(?:[\d,]+)(?:\.\d+)?")

@logger.catch(reraise=True)
def get_city_costs(city: str) -> CityCostData:
    city = city.lower()
    pickle_file = f"data/cities/{city}.pkl"
    url = f"https://www.expatistan.com/cost-of-living/{city}"

    city_cost = CityCostData(None, [])

    if os.path.exists(pickle_file):
        with open(pickle_file, "rb") as f:
            city_cost: CityCostData = pickle.load(f)

        logger.debug(f"loaded {len(city_cost.costs)} costs from pickle file")

    else:
        html_doc = requests.get(url).text

        soup = BeautifulSoup(html_doc, 'html.parser')

        city_expenses = soup.find("table", class_="comparison single-city")

        city_expenses_rows = city_expenses.find_all("a", class_="downlighted")
        city_prices_rows = city_expenses.find_all("td", class_="price city-1")

        # print(f"costos {len(city_expenses_rows)}")
        # print(f"precios {len(city_prices_rows)}")

        assert (len(city_expenses_rows) == len(city_prices_rows))
        combinacions = zip(city_expenses_rows, city_prices_rows)
        assert (len(city_expenses_rows) == len(cost_comparator.COST_TAGS))

        city_cost.costs = []

        for expense, (_, price) in zip(cost_comparator.COST_TAGS, combinacions):
            price_string = price.text.strip()
            if city_cost.currency is None:
                city_cost.currency = re.findall(
                    r"\w+", price_string)[0].upper()
            price = re.findall(CURRENCY_REGEX, price_string)[
                0].replace(",", "")
            city_cost.costs.append(Cost(expense, float(price)))

        with open(pickle_file, "wb") as f:
            pickle.dump(city_cost, f)

        logger.debug(
            f"saved {len(city_cost.costs)} costs to pickle file from url")

    return city_cost
