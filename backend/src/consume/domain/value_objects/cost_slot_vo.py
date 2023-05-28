from dataclasses import dataclass


@dataclass(frozen=True)
class CostSlotVO:
    timestamp: int
    cost: int
    currencty = "EUR"
