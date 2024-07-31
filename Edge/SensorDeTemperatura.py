import random
import zmq
import time
import json

class SensorDeTemperatura:
    def __init__(self,  publish_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(publish_address)
        

    def iniciar(self):
        while True:
            temperatura = random.uniform(11, 29.4)
            mensaje = {
                'tipo': 'Temperatura',
                'valor': temperatura,
                'sensor_id':random.randint(1, 20)   
            }
            self.socket.send_json(mensaje)
            time.sleep(1)
           
    

def main():
    PUBLISH_ADDRES = "tcp://*:5555"
    sensor = SensorDeTemperatura(PUBLISH_ADDRES)
    sensor.iniciar()

if __name__ == "__main__":
    main()
