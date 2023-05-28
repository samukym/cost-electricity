import pytest
from consume.infrastructure.data_sources.file_system.power_measurements_file_repository import (
    PowerMeasurementsFileRepository
)


def test_is_reading_from_file_ok():
    powerMeasurements = PowerMeasurementsFileRepository(
        "../backend/test/infrastructure/data_sources/file_system/power_measurements_file_repository/test_measurements.json"
    ).getMeasurementsBySensor("test_sensor_id")
    assert powerMeasurements.sensorId == "test_sensor_id"
