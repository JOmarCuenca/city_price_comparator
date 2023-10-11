from dataclasses import dataclass


@dataclass
class Cost:
    name: str
    cost: float

    @property
    def pretty_cost(self):
        return f"{self.cost:,}"
