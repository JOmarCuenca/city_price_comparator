from dotenv import load_dotenv, dotenv_values
from loguru import logger
from models.env_values import EnvValues

logger.debug("Loading environment variables...")

# Load environment variables from .env file
logger.debug(f"Loaded {load_dotenv()} environment variables")

try:
    # Load environment variables from .env file
    values = dotenv_values()
    ENV_VALUES = EnvValues(
        values["currency"],
        int(values["cost_lifetime"])
    )
except:
    logger.exception("Error while loading environment variables")
    raise
