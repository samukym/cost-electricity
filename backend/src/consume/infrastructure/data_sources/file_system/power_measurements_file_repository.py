from datetime import datetime
from typing import List
from consume.domain.errors.NoSensorError import SensorNotFoundError
from consume.domain.repositories.i_power_measurements_repository import IPowerMeasurementsRepository
import pandas
from pandas import DataFrame
import config
from consume.domain.value_objects.power_measurements_vo import PowerMeasurementVO
from consume.domain.value_objects.sensor_measurement_vo import SensorMeasurementsVO


class PowerMeasurementsFileRepository(IPowerMeasurementsRepository):
    measurementsCollection: DataFrame

    def __init__(self, pathFile: str | None):
        self.measurementsCollection = self._loadMeasurements(pathFile or config.POWER_MEASUREMENTS_FILE)

    def getSensors(self) -> List[str]:
        ids = self.measurementsCollection["tid"]
        return [f'power_sensor_{id}' for id in range(len(ids))]
    
    def getMeasurementsBySensor(self, sensorId: str) -> SensorMeasurementsVO:
        dfSensor = self.measurementsCollection[self.measurementsCollection["tid"] == sensorId]
        if dfSensor.empty:
            raise SensorNotFoundError
        return self._getMeasurements(dfSensor)
    
    def _getMeasurements(self, sensorDf: DataFrame) -> SensorMeasurementsVO:
        powerMeasurements = []
        sensorMeasurement = sensorDf.iloc[0]
        timestamps = sensorMeasurement["timestamps"]
        values = sensorMeasurement["values"]
        for i in range(len(timestamps)):
            timestamp = int(datetime.fromisoformat(timestamps[i][:-1]).timestamp())
            powerMeasurements.append(PowerMeasurementVO(timestamp, values[i]))

        return SensorMeasurementsVO(sensorMeasurement["tid"], powerMeasurements)

    def _loadMeasurements(self, path: str) -> DataFrame:
        measurementsDf = self._readFileMeasurements(path)
        return pandas.json_normalize(measurementsDf["data"])

    def _readFileMeasurements(self, path: str) -> DataFrame:
        with open(path) as f:
            return pandas.read_json(f)
