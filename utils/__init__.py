from dotenv import load_dotenv, dotenv_values
from loguru import logger
from models.env_values import EnvValues

logger.debug("Loading environment variables...")

# Load environment variables from .env file
logger.debug(f"Loaded {load_dotenv()} environment variables")

try:
    ENV_VALUES = EnvValues(**dotenv_values())
except:
    logger.exception("Error while loading environment variables")
    raise
