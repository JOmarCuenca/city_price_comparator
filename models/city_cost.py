from dataclasses import dataclass
from models.cost import Cost
from datetime import datetime


@dataclass(frozen=True, eq=True)
class CityCostData:
    name: str
    currency: str | None
    costs: list[Cost]
    creation_date: datetime = datetime.now()


@dataclass(frozen=True, eq=True)
class CostComparison:
    cost_name: str
    base_cost: Cost
    comparison_cost: Cost

    @property
    def comparison(self) -> float:
        return (1 - self.comparison_cost.cost / self.base_cost.cost) * 100

    @property
    def percentage_comparison(self) -> str:
        return f"{self.comparison:.3f}%"
    
    def cost_comparison(self) -> str:
        return f"{self.cost_name}: {self.percentage_comparison}"
