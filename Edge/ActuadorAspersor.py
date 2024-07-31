import zmq

class ActuadorAspersor:
    def __init__(self, pull_address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(pull_address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
        self.activado = False

    def escuchar_sensores(self):
        print("Actuador Aspersor esperando señales de los sensores de humo...")
        while True:
            try:
                mensaje = self.socket.recv_string()
                print(f"Señal recibida: {mensaje}. Activando aspersor...")
                self.activar_aspersor(mensaje)
            except Exception as e:
                print(f"Error al recibir la señal: {e}")

    def activar_aspersor(self, mensaje):
        self.activado = True
        print("Aspersor activado.")

def main():
    PULL_ADDRESS = "tcp://localhost:5557"
    actuador = ActuadorAspersor(PULL_ADDRESS)
    actuador.escuchar_sensores()

if __name__ == "__main__":
    main()
