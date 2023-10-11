from dataclasses import dataclass
from models.cost import Cost


@dataclass
class CityCostData:
    currency: str | None
    costs: list[Cost]
