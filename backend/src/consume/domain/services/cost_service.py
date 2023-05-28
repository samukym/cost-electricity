from consume.domain.errors.NoMeasurementsError import NoMeasurementsError
from consume.domain.repositories.i_electricity_prices_repository import (
    IElectricityPricesRepository,
)
from consume.domain.repositories.i_power_measurements_repository import (
    IPowerMeasurementsRepository,
)
from typing import List
from consume.domain.value_objects.cost_slot_vo import CostSlotVO
from consume.domain.value_objects.electricity_price_slot_vo import (
    ElectricityPriceSlotVO,
)
from consume.domain.value_objects.power_measurements_vo import PowerMeasurementVO
from functools import reduce
from consume.domain.value_objects.sensor_measurement_vo import SensorMeasurementsVO

from utils.datetime import UtilsDateTime

class CostService:
    def __init__(
        self,
        electricityPricesRepository: IElectricityPricesRepository,
        powerMeasurementsRepository: IPowerMeasurementsRepository,
    ):
        self.electricityPricesRepository = electricityPricesRepository
        self.powerMeasurementsRepository = powerMeasurementsRepository

    def getConsumeCostBetween(
        self, sensorId: str, startTime: int | None, endTime: int | None
    )-> List[CostSlotVO]:
        powerMeasurements = self.powerMeasurementsRepository.getMeasurementsBySensor(sensorId)
        if len(powerMeasurements.measurements) == 0:
            raise NoMeasurementsError
        startTime = startTime or powerMeasurements.measurements[0].timestamp
        endTime = endTime or powerMeasurements.measurements[-1].timestamp
        electricityPrices = self.electricityPricesRepository.getPricesBetween(startTime, endTime)
        
        measurementsInRoundHours: List[PowerMeasurementVO] = [
            PowerMeasurementVO(UtilsDateTime().timestampToRoundHour(measurement.timestamp), measurement.value)
            for measurement in powerMeasurements.measurements
        ]
        totalPowerPerHour: List[PowerMeasurementVO] = [
            powerByHour
            for powerByHour in reduce(self._sumPowerByHour, measurementsInRoundHours, [])
        ]
        costPerHour = [
            self._calculateCostAtHour(powerAtHour, electricityPrices)
            for powerAtHour in totalPowerPerHour
        ]
        
        return costPerHour

    def _calculateCostAtHour(
        self, powerAtHour: PowerMeasurementVO, electricityPrices: List[ElectricityPriceSlotVO]
        ) -> CostSlotVO:
        priceAtHour = self._getElectricityPriceAtHour(powerAtHour.timestamp, electricityPrices)
        totalKWAtHour = powerAtHour.value
        totalMwAtHour = totalKWAtHour / 1000
        cost = totalMwAtHour * priceAtHour
        return CostSlotVO(powerAtHour.timestamp, cost)
        
    def _getElectricityPriceAtHour(
        self, measurementTimestamp: int, prices: List[ElectricityPriceSlotVO]
    ) -> float:
        timestampAtHour = UtilsDateTime().timestampToRoundHour(measurementTimestamp)
        priceAtHour = next(
            filter(lambda slot: slot.startTimestamp == timestampAtHour, prices)
        )
        return priceAtHour.price
        
    def _sumPowerByHour(
        self, accPowerMeasurement: List[PowerMeasurementVO], currentMeasurement: PowerMeasurementVO
    ) -> List:
        measurementIndex = self._findMeasurementIndexByTime(accPowerMeasurement, currentMeasurement.timestamp)
        if measurementIndex < 0:
            accPowerMeasurement.append(PowerMeasurementVO(currentMeasurement.timestamp, currentMeasurement.value))
        else:
            accPowerMeasurement[measurementIndex] = PowerMeasurementVO(
                currentMeasurement.timestamp,
                accPowerMeasurement[measurementIndex].value + currentMeasurement.value,
            )
        return accPowerMeasurement
    
    def _findMeasurementIndexByTime(self, measurements: List[PowerMeasurementVO], timestamp: int) -> int:
        return next(
            (
                index
                for index, measurement in enumerate(measurements) if measurement.timestamp == timestamp
            ), 
            -1
        )