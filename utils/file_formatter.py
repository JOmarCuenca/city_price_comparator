import models.city_cost as costs
from datetime import datetime
import statistics
import csv

from loguru import logger


def filename_formatter(city_1: str, city_2: str) -> str:
    return f"{city_1}_vs_{city_2}_{datetime.now().strftime('%Y_%m')}.csv"


def generate_cost_comparison_strings(city_1: str, city_2: str, compared_costs: list[costs.CostComparison]) -> list[str]:
    rows = [
        [
            "Cost Name",
            city_1.replace('-', ' ').capitalize(),
            city_2.replace('-', ' ').capitalize(),
            "Percentage Difference",
        ]
    ]

    for cost in compared_costs:
        rows.append([
            cost.cost_name,
            f"$ {cost.base_cost.cost:.2f}",
            f"$ {cost.comparison_cost.cost:.2f}",
            cost.percentage_comparison,
        ])

    rows.append(
        [
            '',
            '',
            '',
            f"{statistics.mean([cost.comparison for cost in compared_costs]):.5f}%",
        ]
    )

    return rows


def save_cost_comparisons(city_1: str, city_2: str, results: list[costs.CostComparison]) -> None:
    name = "dumps/results/" + filename_formatter(city_1, city_2)

    logger.info(f"Saving results in {name}")

    with open(name, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(generate_cost_comparison_strings(
            city_1, city_2, results))
