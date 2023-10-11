from dataclasses import dataclass
from models.cost import Cost


@dataclass
class CityCostData:
    currency: str | None
    costs: list[Cost]


@dataclass
class CostComparison:
    cost_name: str
    currency_rate: float
    base_cost: Cost
    comparison_cost: Cost

    @property
    def localized_compared_cost(self) -> float:
        return self.comparison_cost.cost * self.currency_rate

    @property
    def comparison(self) -> float:
        return (1 - self.localized_compared_cost / self.base_cost.cost) * 100

    @property
    def percentage_comparison(self) -> str:
        return f"{self.comparison:.3f}%"
    
    def cost_comparison(self) -> str:
        return f"{self.cost_name}: {self.percentage_comparison}"
