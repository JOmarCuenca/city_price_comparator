import models.city_cost as costs
from datetime import datetime
from utils.cost_comparator import generate_cost_comparison_strings


def filename_formatter(city_1: costs.CityCostData, city_2: costs.CityCostData):
    """Formats the filename of the cost comparison.

    Args:
        city_1 (CityCostData): The first city to compare.
        city_2 (CityCostData): The second city to compare.

    Returns:
        str: The formatted filename.
    """
    return f"dumps/results/{city_1.name}_vs_{city_2.name}_{datetime.now().strftime('%Y_%m')}.txt"


def save_cost_comparisons(file_name: str, results: list[costs.CostComparison]) -> None:
    """Saves the results of the cost comparison to a file.

    Args:
        results (list[models.cost.CostComparison]): The results of the cost comparison.
    """
    with open(file_name, "w") as f:
        f.write("\n".join(generate_cost_comparison_strings(results)))
