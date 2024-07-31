import zmq
import json

class SistemaCalidadEdge:
    def __init__(self, subscribe_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(subscribe_address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')

    def iniciar(self):
        print("Sistema de Calidad Edge iniciado y esperando alertas...")
        while True:
            try:
                alerta = self.socket.recv_string()
                alerta_json = json.loads(alerta)
                print(f"ALERTA: {alerta_json['alerta']} - Timestamp: {alerta_json['timestamp']}")
            except Exception as e:
                print(f"Error en Sistema de Calidad Edge: {e}")

def main():
    SUBSCRIBE_ADDRESS = "tcp://localhost:5556"
    sistema = SistemaCalidadEdge(SUBSCRIBE_ADDRESS)
    sistema.iniciar()

if __name__ == "__main__":
    main()
