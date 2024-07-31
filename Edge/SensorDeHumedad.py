import zmq
import time
import random
import json

class SensorHumedad:
    def __init__(self, publish_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(publish_address)

    def iniciar(self):
        while True:
            humedad = random.uniform(0, 100)
            mensaje = {
                'tipo': 'Humedad',
                'valor': humedad,
                'sensor_id': random.randint(1, 20)
            }
            self.socket.send_json(mensaje)
            time.sleep(1)  # enviar un mensaje cada segundo

def main():
    PUBLISH_ADDRESS = "tcp://*:5555"
    sensor = SensorHumedad(PUBLISH_ADDRESS)
    sensor.iniciar()

if __name__ == "__main__":
    main()
