import serial
import serial.tools.list_ports
import threading
import queue
import time
from configuracion import PUERTO_ARDUINO, VELOCIDAD


class ComunicacionArduino:

    def __init__(self):
        self.cola_mensajes = queue.Queue()
        self.activo = False
        self.hilo = None
        self.arduino = None

    def detectar_puerto(self):
        if PUERTO_ARDUINO is not None:
            return PUERTO_ARDUINO

        puertos = list(serial.tools.list_ports.comports())

        if len(puertos) == 0:
            raise serial.SerialException("No se detectaron puertos seriales.")

        palabras_clave = ["arduino", "ch340", "usb serial", "ttyacm", "ttyusb"]

        for puerto in puertos:
            descripcion = (puerto.description + " " + puerto.device).lower()
            for palabra in palabras_clave:
                if palabra in descripcion:
                    return puerto.device

        if len(puertos) == 1:
            return puertos[0].device

        raise serial.SerialException("No se pudo identificar el Arduino automáticamente.")

    def iniciar(self):
        self.activo = True
        self.hilo = threading.Thread(target=self.leer_serial, daemon=True)
        self.hilo.start()

    def leer_serial(self):
        try:
            puerto = self.detectar_puerto()
            self.cola_mensajes.put({"tipo": "estado", "valor": f"Conectando a {puerto}..."})

            self.arduino = serial.Serial(puerto, VELOCIDAD, timeout=1)
            time.sleep(2)  # Espera a que Arduino se reinicie al abrir el puerto

            self.cola_mensajes.put({"tipo": "conectado", "valor": puerto})

            while self.activo:
                linea = self.arduino.readline().decode("utf-8", errors="ignore").strip()

                if linea != "":
                    try:
                        partes = linea.split(",")

                        if len(partes) == 3:
                            numeros = []
                            valido = True

                            for parte in partes:
                                num = int(parte)
                                if 0 <= num <= 9:
                                    numeros.append(num)
                                else:
                                    valido = False

                            if valido:
                                self.cola_mensajes.put({"tipo": "datos", "valor": numeros})

                    except ValueError:
                        # Si llega una línea corrupta o con letras, la ignoramos sin romper el programa
                        pass

        except (serial.SerialException, OSError) as error:
            self.cola_mensajes.put({"tipo": "error", "valor": str(error)})

        finally:
            if self.arduino is not None and self.arduino.is_open:
                self.arduino.close()

    def obtener_datos(self):
        mensajes = []
        while not self.cola_mensajes.empty():
            mensajes.append(self.cola_mensajes.get())
        return mensajes

    def cerrar(self):
        self.activo = False
        if self.hilo is not None:
            self.hilo.join(timeout=2)