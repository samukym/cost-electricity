from dataclasses import dataclass


@dataclass(frozen=True)
class PowerMeasurementVO:
    timestamp: int
    value: int
    measure = "kW"
