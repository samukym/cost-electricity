from flask import Flask, jsonify, request
from consume.domain.errors.NoMeasurementsError import NoMeasurementsError
from consume.domain.errors.NoSensorError import SensorNotFoundError
from consume.domain.services.cost_service import CostService
from consume.domain.services.sensor_service import SensorService
from consume.infrastructure.data_sources.apis.electricity_prices_awattar_repository import ElectricityPriceAwattarRepository
from consume.infrastructure.data_sources.file_system.power_measurements_file_repository import PowerMeasurementsFileRepository
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/sensors/<sensorId>", methods=["GET"])
def getSensor(sensorId):
    try:
        start = int(request.args.get('start', 0)) or None
        end = int(request.args.get('end', 0)) or None
        consumeCost = CostService(
            ElectricityPriceAwattarRepository(), PowerMeasurementsFileRepository(None)
        ).getConsumeCostBetween(sensorId, start, end)
        return jsonify(consumeCost)
    except SensorNotFoundError:
        return jsonify({'error': 'Sensor not found'}), 404
    except NoMeasurementsError:
        return jsonify({'error': 'Measurements not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@app.route("/sensors", methods=["GET"])
def getSensors():
    try:
        sensors = SensorService(PowerMeasurementsFileRepository(None)).getSensors()
        return jsonify(sensors)
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500



if __name__ == "__main__":
    app.run(debug=True)