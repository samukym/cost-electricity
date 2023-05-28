from abc import ABC, abstractmethod
from consume.domain.value_objects.electricity_price_slot_vo import ElectricityPriceSlotVO
from typing import List

class IElectricityPricesRepository(ABC):
    abstractmethod
    def getPricesBetween(self, startTime: int, endTime: int) -> List[ElectricityPriceSlotVO]:
        pass
