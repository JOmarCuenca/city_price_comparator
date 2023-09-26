from cost_downloader import load_city_costs

from loguru import logger

costs = load_city_costs("mexico-city")

logger.debug(f"costs: {costs}")