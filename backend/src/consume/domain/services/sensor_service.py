from typing import List
from consume.domain.repositories.i_power_measurements_repository import IPowerMeasurementsRepository


class SensorService:
    def __init__(self, powerMeasurementsRepository: IPowerMeasurementsRepository):
        self.powerMeasurementsRepository = powerMeasurementsRepository
        
    def getSensors(self) -> List[str]:
        return self.powerMeasurementsRepository.getSensors()