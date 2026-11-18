from pathlib import Path

# Rutas de carpetas
CARPETA_BASE = Path(__file__).resolve().parent
CARPETA_IMAGENES = CARPETA_BASE / "imagenes"

# Configuración de conexión Serial (Arduino)
PUERTO_ARDUINO = "/dev/ttyACM0"  # Si es None, lo busca automáticamente (ej. "COM3")
VELOCIDAD = 9600

# Configuración de seguridad
COMBINACION_CORRECTA = "010"
INTENTOS_MAXIMOS = 3
DURACION_BLOQUEO = 30  # En segundos

# Configuración de la ventana principal
TITULO_VENTANA = "Caja fuerte"
TAMANO_VENTANA = "800x760"