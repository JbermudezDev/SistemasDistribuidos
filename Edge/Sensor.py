import zmq
import threading
import random
import time
import json

class Sensor(threading.Thread):
    def __init__(self, id_sensor, fog_address, tipo, config_path, intervalo):
        super().__init__()
        self.id_sensor = id_sensor
        self.fog_address = fog_address
        self.tipo = tipo
        self.intervalo = intervalo
        self.config = self.cargar_configuracion(config_path)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)  # Usando PUB para publicar mensajes
        self.socket.connect(fog_address)
        self.limite_inferior = self.config['limite_inferior']
        self.limite_superior = self.config['limite_superior']

    def cargar_configuracion(self, config_path):
        with open(config_path, 'r') as file:
            return json.load(file)

    def run(self):
        while True:
            valor = self.generar_muestra()
            self.enviar_muestra(valor)
            time.sleep(self.intervalo)

    def generar_muestra(self):
        rnd = random.random()
        if rnd < self.config['probabilidad_correcto']:
            return self.generar_valor_correcto()
        elif rnd < self.config['probabilidad_correcto'] + self.config['probabilidad_fuera_de_rango']:
            return self.generar_valor_fuera_de_rango()
        else:
            return self.generar_valor_erroneo()

    def enviar_muestra(self, valor):
        mensaje = {
            'id_sensor': self.id_sensor,
            'tipo': self.tipo,
            'valor': valor,
            'timestamp': time.time()
        }
        # Agregar una alerta si el valor está fuera de rango
        if valor > self.limite_superior or valor < self.limite_inferior:
            mensaje['alerta'] = f"Valor fuera de rango: {valor}"
        self.socket.send_string(f"{self.tipo} {json.dumps(mensaje)}")
        print(f"Sensor {self.id_sensor} de {self.tipo} envió: {json.dumps(mensaje)}")

    def generar_valor_correcto(self):
        raise NotImplementedError

    def generar_valor_fuera_de_rango(self):
        raise NotImplementedError

    def generar_valor_erroneo(self):
        raise NotImplementedError
