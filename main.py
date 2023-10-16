from utils.cost_getter import get_city_costs
from loguru import logger
from datetime import datetime
from models.args import Args

now = datetime.now().strftime("%Y-%m-%d")

logger.add(f"logs/log_{now}.log")

args = Args.parseArgs()

main_city = get_city_costs(args.main_city)

compared_cities = [get_city_costs(city) for city in args.compared_cities]


