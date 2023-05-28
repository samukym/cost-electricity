from abc import ABC, abstractmethod
from typing import List
from consume.domain.value_objects.sensor_measurement_vo import SensorMeasurementsVO

class IPowerMeasurementsRepository(ABC):
    abstractmethod
    def getMeasurementsBySensor(self, sensorId: str) -> SensorMeasurementsVO:
        pass
    
    abstractmethod
    def getSensors(self) -> List[str]:
        pass
