from consume.domain.value_objects.cost_slot_vo import CostSlotVO
from consume.domain.value_objects.power_measurements_vo import PowerMeasurementVO
from consume.domain.value_objects.sensor_measurement_vo import SensorMeasurementsVO
import pytest
from unittest.mock import patch
from unittest.mock import Mock
from datetime import datetime
from consume.domain.services.cost_service import CostService
from consume.infrastructure.data_sources.file_system.power_measurements_file_repository import (
    PowerMeasurementsFileRepository,
)
from consume.infrastructure.data_sources.apis.electricity_prices_awattar_repository import (
    ElectricityPriceAwattarRepository,
)
from consume.domain.value_objects.electricity_price_slot_vo import (
    ElectricityPriceSlotVO,
)


def test_consume_cost_should_return_cost_over_time_as_the_sum_of_all_power_measurements():
    # Arrange
    ## Test data
    priceFirstHour = 57.94
    priceSecondHour = 47.94
    startFirstHour = int(datetime(year=2022, month=5, day=6, hour=9, minute=0, second=0).timestamp())
    startSecondHour = int(datetime(year=2022, month=5, day=6, hour=10, minute=0, second=0).timestamp())
    electricityPrices = [
        ElectricityPriceSlotVO(
            startFirstHour,
            startSecondHour,
            priceFirstHour,
        ),
        ElectricityPriceSlotVO(
            startSecondHour,
            int(datetime(year=2022, month=5, day=6, hour=11, minute=0, second=0).timestamp()),
            priceSecondHour,
        ),
    ]
    firstHourPowerMeasurements = [200, 180]
    secondHourPowerMeasurements = [250, 200]
    kWMeasures = firstHourPowerMeasurements + secondHourPowerMeasurements
    timestampsMeasures = [
        "2022-05-06T09:19:19.749",
        "2022-05-06T09:55:00.445",
        "2022-05-06T10:20:00.445",
        "2022-05-06T10:50:00.445"
    ]
    sensorId = "test_sensor_id"
    powerMeasurements = SensorMeasurementsVO(
        sensorId=sensorId,
        measurements=[
            PowerMeasurementVO(
                int(datetime.fromisoformat(timestampsMeasures[i]).timestamp()),
                kWMeasures[i]    
            ) 
            for i in range(len(kWMeasures))
        ],
    )
    kWToMWCoef = 1000
    ## Mocking
    electricityPriceAwattarRepositoryMock = Mock(spec=ElectricityPriceAwattarRepository)
    powerMeasurementsFileRepositoryMock = Mock(spec=PowerMeasurementsFileRepository)
    electricityPriceAwattarRepositoryMock.getPricesBetween.return_value = electricityPrices
    powerMeasurementsFileRepositoryMock.getMeasurementsBySensor.return_value = powerMeasurements
    # Act
    cost = CostService(
        electricityPriceAwattarRepositoryMock, 
        powerMeasurementsFileRepositoryMock
    ).getConsumeCostBetween(
        "test_sensor_id",
        startTime=int(datetime(year=2022, month=5, day=6, hour=9, minute=10, second=0).timestamp()),
        endTime=int(datetime(year=2022, month=5, day=6, hour=9, minute=15, second=0).timestamp())
    )
    
    costFirstHour = priceFirstHour * sum(firstHourPowerMeasurements) / kWToMWCoef
    costSecondHour = priceSecondHour * sum(secondHourPowerMeasurements) / kWToMWCoef
    # Assert
    assert cost == [
        CostSlotVO(startFirstHour, costFirstHour),
        CostSlotVO(startSecondHour, costSecondHour),
    ]

def test_consume_cost_should_return_error_404__if_there_is_no_measurements():
    pass

def test_consume_cost_should_return_error_404_if_sensor_does_not_exist():
    pass

def test_consume_cost_should_return_error_500_id_dates_are_invalid():
    pass
