from datetime import datetime
import requests
from consume.domain.repositories.i_electricity_prices_repository import IElectricityPricesRepository
from consume.domain.value_objects.electricity_price_slot_vo import ElectricityPriceSlotVO
from typing import List

from utils.datetime import UtilsDateTime  


class ElectricityPriceAwattarRepository(IElectricityPricesRepository):
    apiBaseUrl = "https://api.awattar.de/v1/marketdata" 
    
    def getPricesBetween(self, startTime: int, endTime: int) -> List[ElectricityPriceSlotVO]:
        startTime, endTime = self._normalizeHours(startTime, endTime)
        return self._fetchElectricityPrices(startTime, endTime)
    
    def _normalizeHours(self, startTime: int, endTime: int):
        starTimeRoundHour = UtilsDateTime().timestampToRoundHour(startTime)
        datetimeEndTime = datetime.fromtimestamp(endTime)
        datetimeEndTimeNextHour = int(datetimeEndTime.replace(hour=datetimeEndTime.hour + 1).timestamp())
        endTimeRoundToNextHour = UtilsDateTime().timestampToRoundHour(datetimeEndTimeNextHour)
        return (starTimeRoundHour, endTimeRoundToNextHour)
    
    def _fetchElectricityPrices(self, startTimestamp: int, endTimestamp: int) -> List[ElectricityPriceSlotVO]:
        url = f"{self.apiBaseUrl}?start={startTimestamp * 1000}&end={endTimestamp * 1000}"
        response = requests.get(url)
        if response.status_code >= 300:
            raise Exception(f"Failed to fetch electricity prices. Status code: {response.status_code}")
        data = response.json()
        price_slots = []
        for slot_data in data['data']:
            price_slots.append(
                ElectricityPriceSlotVO(
                    startTimestamp=slot_data["start_timestamp"] / 1000,
                    endTimestamp=slot_data["end_timestamp"] / 1000,
                    price=slot_data["marketprice"],
                )
            )
        return price_slots
            