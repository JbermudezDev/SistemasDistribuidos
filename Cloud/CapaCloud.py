import zmq
import json
from datetime import datetime

class CloudComputing:
    def __init__(self, subscribe_address_proxy, publish_address_calidad):
        self.context = zmq.Context()
        self.subscribe_socket_proxy = self.context.socket(zmq.SUB)
        self.subscribe_socket_proxy.connect(subscribe_address_proxy)
        self.subscribe_socket_proxy.setsockopt_string(zmq.SUBSCRIBE, '')

        self.publish_socket_calidad = self.context.socket(zmq.PUB)
        self.publish_socket_calidad.bind(publish_address_calidad)

    def iniciar(self):
        print("Cloud Computing iniciado y esperando datos del Proxy...")
        while True:
            try:
                mensaje_json = self.subscribe_socket_proxy.recv_json()
                self.procesar_mensaje(mensaje_json)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e}")
            except Exception as e:
                print(f"Error al recibir mensaje: {e}")

    def procesar_mensaje(self, mensaje_json):
        if mensaje_json.get('tipo') == 'humedad':
            humedad = mensaje_json.get('valor')
            if humedad is not None:
                self.calcular_humedad(humedad)

    def calcular_humedad(self, humedad):
        if humedad < 70:  # Límite de humedad
            self.enviar_alerta_calidad(f"Humedad baja detectada: {humedad}%")

    def enviar_alerta_calidad(self, mensaje):
        try:
            alerta = {
                'alerta': mensaje,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.publish_socket_calidad.send_string(json.dumps(alerta))
            print(f"Alerta enviada al sistema de calidad: {mensaje}")
        except Exception as e:
            print(f"Error al enviar alerta de calidad: {e}")

def main():
    SUBSCRIBE_ADDRESS_PROXY = "tcp://localhost:5557"
    PUBLISH_CALIDAD_ADDRESS = "tcp://*:5559"
    
    cloud = CloudComputing(SUBSCRIBE_ADDRESS_PROXY, PUBLISH_CALIDAD_ADDRESS)
    cloud.iniciar()

if __name__ == "__main__":
    main()
