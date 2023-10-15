from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class EnvValues:
    currency: str
    """Currency to use to make comparisons"""
    cost_lifetime: int
    """Amount of days to keep cached costs"""
