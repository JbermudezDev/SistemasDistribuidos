import zmq
import json
from datetime import datetime

class ProxyFog:
    def __init__(self, subscribe_address, publish_calidad_address, publish_aspersor_address, cloud_address):
        self.context = zmq.Context()
        self.subscribe_socket = self.context.socket(zmq.SUB)
        self.subscribe_socket.connect(subscribe_address)
        self.subscribe_socket.setsockopt_string(zmq.SUBSCRIBE, '')
        
        self.publish_socket_calidad = self.context.socket(zmq.PUB)
        self.publish_socket_calidad.bind(publish_calidad_address)
        
        self.publish_socket_aspersor = self.context.socket(zmq.PUB)
        self.publish_socket_aspersor.bind(publish_aspersor_address)
        
        self.cloud_socket = self.context.socket(zmq.PUB)
        self.cloud_socket.bind(cloud_address)
        
        self.humedades = []

    def iniciar(self):
        print("Proxy de Fog Computing iniciado y esperando datos...")
        while True:
            try:
                mensaje_json = self.subscribe_socket.recv_json()
                self.procesar_mensaje(mensaje_json)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e}")
            except Exception as e:
                print(f"Error al recibir mensaje: {e}")

    def procesar_mensaje(self, mensaje_json):
        if self.validar_muestra(mensaje_json):
            if mensaje_json['tipo'] == 'Humedad':
                self.procesar_humedad(mensaje_json)
            elif mensaje_json['tipo'] == 'Humo' and mensaje_json['valor']:
                self.enviar_alerta_calidad(f"Sensor de Humo {mensaje_json['sensor_id']} detectó humo.")

    def validar_muestra(self, dato):
        return dato.get('valor') is not None

    def procesar_humedad(self, dato):
        self.humedades.append(dato['valor'])
        if len(self.humedades) == 10:
            promedio_hum = sum(self.humedades) / len(self.humedades)
            self.humedades.pop(0)
            if not (70 <= promedio_hum <= 100):
                self.enviar_alerta_calidad(f"Humedad fuera de rango: {promedio_hum}%")
            self.enviar_humedad_a_cloud(promedio_hum)

    def procesar_humo(self, dato):
        if dato['valor']:
            mensaje_alerta = f"Alerta de humo detectada por el sensor {dato['sensor_id']}"
            self.enviar_alerta_calidad(mensaje_alerta)
            self.enviar_alerta_aspersor(mensaje_alerta)

    def enviar_alerta_calidad(self, mensaje):
        try:
            alerta = {
                'alerta': mensaje,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.publish_socket_calidad.send_string(json.dumps(alerta))
            print(f"Alerta enviada: {mensaje}")
        except Exception as e:
            print(f"Error al enviar alerta: {e}")

    def enviar_alerta_aspersor(self, mensaje):
        try:
            self.publish_socket_aspersor.send_string(mensaje)
            print(f"Alerta enviada al aspersor: {mensaje}")
        except Exception as e:
            print(f"Error al enviar alerta al aspersor: {e}")

    def enviar_humedad_a_cloud(self, humedad):
        try:
            mensaje = {
                'tipo': 'humedad',
                'valor': humedad,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.cloud_socket.send_string(json.dumps(mensaje))
            print(f"Humedad enviada al cloud: {humedad}")
        except Exception as e:
            print(f"Error al enviar humedad: {e}")

def main():
    SUBSCRIBE_ADDRESS = "tcp://localhost:5555"
    PUBLISH_CALIDAD_ADDRESS = "tcp://*:5556"
    PUBLISH_ASPERSOR_ADDRESS = "tcp://*:5558"
    CLOUD_ADDRESS = "tcp://*:5557"
    
    proxy = ProxyFog(SUBSCRIBE_ADDRESS, PUBLISH_CALIDAD_ADDRESS, PUBLISH_ASPERSOR_ADDRESS, CLOUD_ADDRESS)
    proxy.iniciar()

if __name__ == "__main__":
    main()
