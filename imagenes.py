import customtkinter as ctk
from PIL import Image
from configuracion import CARPETA_IMAGENES


def cargar_imagen(nombre_archivo, tamano):
    """Busca una imagen en la carpeta 'imagenes' y la prepara para CustomTkinter."""
    extensiones = [".png", ".jpg", ".jpeg", ".webp"]

    for ext in extensiones:
        ruta_completa = CARPETA_IMAGENES / (nombre_archivo + ext)

        if ruta_completa.exists():
            try:
                imagen_pil = Image.open(ruta_completa)
                imagen_ctk = ctk.CTkImage(
                    light_image=imagen_pil,
                    dark_image=imagen_pil,
                    size=tamano
                )
                return imagen_ctk
            except Exception as error:
                print(f"Error al abrir la imagen {nombre_archivo}: {error}")
                return None

    return None