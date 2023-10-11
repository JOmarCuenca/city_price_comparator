from utils.cost_getter import get_city_costs

from loguru import logger

costs = get_city_costs("mexico-city")

logger.debug(f"costs: {costs}")