import zmq
import json

class SistemaDeCalidadCloud:
    def __init__(self, subscribe_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(subscribe_address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def iniciar(self):
        print("Sistema de Calidad Cloud iniciado y esperando alertas...")
        while True:
            try:
                alerta = self.socket.recv_string()
                alerta_json = json.loads(alerta)
                self.procesar_alerta(alerta_json)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e}")
            except Exception as e:
                print(f"Error en Sistema de Calidad Cloud: {e}")

    def procesar_alerta(self, alerta_json):
        print(f"ALERTA: {alerta_json['alerta']} - Timestamp: {alerta_json['timestamp']}")

def main():
    SUBSCRIBE_ADDRESS = "tcp://localhost:5556"  # Dirección de publicación del sistema de calidad
    sistema = SistemaDeCalidadCloud(SUBSCRIBE_ADDRESS)
    sistema.iniciar()

if __name__ == "__main__":
    main()
