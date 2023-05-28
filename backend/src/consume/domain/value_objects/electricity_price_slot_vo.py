from dataclasses import dataclass


@dataclass(frozen=True)
class ElectricityPriceSlotVO:
    startTimestamp: int
    endTimestamp: int
    price: float
