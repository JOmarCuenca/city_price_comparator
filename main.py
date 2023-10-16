from datetime import datetime

from loguru import logger
from tqdm import tqdm

now = datetime.now().strftime("%Y-%m-%d")

logger.add(f"logs/log_{now}.log")

from models.args import Args
from utils.cost_comparator import compare_cost
from utils.cost_getter import get_city_costs
from utils.file_formatter import save_cost_comparisons

args = Args.parseArgs()

logger.info("Comparing cities costs...")

main_city = get_city_costs(args.main_city)

for city in tqdm(args.compared_cities):
    if main_city.name == city:
        logger.warning("Omiting comparing to the same city.")
        continue

    logger.debug(f"Getting costs for {city}...")
    city_costs = get_city_costs(city)
    logger.debug(f"Costs for {city} have been retrieved.")

    logger.debug(f"Comparing costs for {city}...")
    compared_costs = compare_cost(main_city, city_costs)
    logger.debug(f"Costs {main_city.name} vs {city} have been compared.")

    logger.debug(f"Saving costs for {city}...")
    
    save_cost_comparisons(main_city.name, city, compared_costs)


logger.info("All costs have been compared.")
