from Sensor import Sensor
import zmq
import random
import time

class SensorDeHumo(Sensor):
    def __init__(self, fog_address):
        self.context = zmq.Context()
        self.fog_socket = self.context.socket(zmq.PUB)
        self.fog_socket.connect(fog_address)  # Cambiado de bind a connect

    def iniciar(self):
        while True:
            humo = random.choice([True, False])
            mensaje = {
                'tipo': 'Humo',
                'valor': humo,
                'sensor_id': random.randint(1, 20)
            }
            self.fog_socket.send_json(mensaje)
            time.sleep(1)  # enviar un mensaje cada segundo

def main():
    FOG_ADDRESS = "tcp://localhost:5555"  # Asegúrate de que esta dirección coincide con la de ProxyFog
    sensor = SensorDeHumo(FOG_ADDRESS)
    sensor.iniciar()

if __name__ == "__main__":
    main()