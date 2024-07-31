from SensorDeHumedad import SensorDeHumedad
from SensorDeTemperatura import SensorDeTemperatura
from SensorDeHumo import SensorDeHumo
import os

def iniciar_sensores(fog_address, calidad_edge_address, actuador_address, cloud_address, config_path):
    sensores = []

    # Iniciar sensores de temperatura
    for i in range(10):
        sensor = SensorDeTemperatura(i, fog_address, "Temperatura", config_path, 6)
        sensor.start()
        sensores.append(sensor)

    # Iniciar sensores de humedad
    for i in range(10, 20):
        sensor = SensorDeHumedad(i, fog_address, "Humedad", config_path, 5)
        sensor.start()
        sensores.append(sensor)

    # Iniciar sensores de humo
    for i in range(20, 30):
        sensor = SensorDeHumo(i, fog_address, calidad_edge_address, actuador_address, cloud_address, "Humo", config_path, 3)
        sensor.start()
        sensores.append(sensor)

    for sensor in sensores:
        sensor.join()

if __name__ == "__main__":
    FOG_ADDRESS = "tcp://localhost:5555"
    CALIDAD_EDGE_ADDRESS = "tcp://localhost:5558"
    ACTUADOR_ADDRESS = "tcp://localhost:5560"
    CLOUD_ADDRESS = "tcp://localhost:5562"
    CONFIG_PATH = os.path.abspath("config_path.json")
    iniciar_sensores(FOG_ADDRESS, CALIDAD_EDGE_ADDRESS, ACTUADOR_ADDRESS, CLOUD_ADDRESS, CONFIG_PATH)





