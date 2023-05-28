from dataclasses import dataclass
from typing import List
from consume.domain.value_objects.power_measurements_vo import PowerMeasurementVO


@dataclass(frozen=True)
class SensorMeasurementsVO:
    sensorId: str
    measurements: List[PowerMeasurementVO]
