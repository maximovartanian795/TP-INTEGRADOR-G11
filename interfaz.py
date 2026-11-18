import customtkinter as ctk
from comunicacion import ComunicacionArduino
from seguridad import ControlSeguridad
from imagenes import cargar_imagen
from configuracion import TITULO_VENTANA, TAMANO_VENTANA


class Aplicacion:

    def __init__(self):
        # 1. Crear y configurar ventana principal
        self.ventana = ctk.CTk()
        self.ventana.title(TITULO_VENTANA)
        self.ventana.geometry(TAMANO_VENTANA)
        self.ventana.resizable(False, False)

        self.ventana_abierta = None

        # 2. Instanciar comunicación con Arduino
        self.comunicacion = ComunicacionArduino()

        # 3. Crear todos los widgets de la interfaz
        self.crear_interfaz()

        # 4. Instanciar control de seguridad
        self.seguridad = ControlSeguridad(
            ventana=self.ventana,
            obtener_combinacion=self.obtener_combinacion,
            mostrar_resultado=self.mostrar_resultado,
            mostrar_bloqueo=self.mostrar_bloqueo,
            abrir_boveda=self.abrir_boveda
        )

        # Eventos
        self.ventana.bind("<Return>", lambda evento: self.comprobar())
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar_programa)

    def crear_interfaz(self):
        # Título principal
        self.titulo = ctk.CTkLabel(
            self.ventana,
            text="CAJA FUERTE",
            font=("Arial", 30, "bold")
        )
        self.titulo.pack(pady=(8, 3))

        # Imagen de bóveda cerrada
        self.imagen_cerrada = cargar_imagen("boveda_cerrada", (560, 420))

        if self.imagen_cerrada is not None:
            self.etiqueta_imagen = ctk.CTkLabel(
                self.ventana,
                image=self.imagen_cerrada,
                text=""
            )
        else:
            self.etiqueta_imagen = ctk.CTkLabel(
                self.ventana,
                text="No se pudo cargar la bóveda cerrada",
                font=("Arial", 14),
                text_color="red"
            )
        self.etiqueta_imagen.pack(pady=2)

        # Contenedor (Frame) para los 3 displays digitales
        self.frame_displays = ctk.CTkFrame(self.ventana, fg_color="transparent")
        self.frame_displays.pack(pady=5)

        self.displays = []
        for i in range(3):
            display = ctk.CTkLabel(
                self.frame_displays,
                text="0",
                font=("Arial", 60, "bold"),
                text_color="#00FF80",
                fg_color="#101820",
                corner_radius=10,
                width=110,
                height=85
            )
            display.grid(row=0, column=i, padx=12, pady=3)
            self.displays.append(display)

        # Estado de conexión Arduino
        self.estado = ctk.CTkLabel(
            self.ventana,
            text="Buscando Arduino...",
            font=("Arial", 13),
            text_color="orange"
        )
        self.estado.pack(pady=2)

        # Mensaje de resultado
        self.resultado = ctk.CTkLabel(
            self.ventana,
            text="Ingrese la combinación",
            font=("Arial", 16)
        )
        self.resultado.pack(pady=2)

        # Contador de bloqueo
        self.bloqueo_label = ctk.CTkLabel(
            self.ventana,
            text="",
            font=("Arial", 17, "bold"),
            text_color="red"
        )
        self.bloqueo_label.pack(pady=2)

        # Botón Acceder
        self.boton = ctk.CTkButton(
            self.ventana,
            text="ACCEDER",
            font=("Arial", 18, "bold"),
            width=200,
            height=42,
            corner_radius=22,
            command=self.comprobar
        )
        self.boton.pack(pady=5)

    def obtener_combinacion(self):
        codigo = ""
        for display in self.displays:
            codigo += display.cget("text")
        return codigo

    def mostrar_resultado(self, texto, color):
        self.resultado.configure(text=texto, text_color=color)

    def mostrar_bloqueo(self, texto):
        self.bloqueo_label.configure(text=texto)

    def comprobar(self):
        self.seguridad.comprobar_combinacion()

    def abrir_boveda(self):
        if self.ventana_abierta is not None and self.ventana_abierta.winfo_exists():
            self.ventana_abierta.lift()
            return

        self.ventana_abierta = ctk.CTkToplevel(self.ventana)
        self.ventana_abierta.title("Bóveda abierta")
        self.ventana_abierta.geometry("900x720")
        self.ventana_abierta.resizable(False, False)

        titulo_abierta = ctk.CTkLabel(
            self.ventana_abierta,
            text="¡ACCESO PERMITIDO!",
            font=("Arial", 25, "bold"),
            text_color="#00FF80"
        )
        titulo_abierta.pack(pady=(8, 3))

        self.imagen_abierta = cargar_imagen("boveda_abierta", (840, 630))

        if self.imagen_abierta is not None:
            etiqueta_abierta = ctk.CTkLabel(
                self.ventana_abierta,
                image=self.imagen_abierta,
                text=""
            )
            etiqueta_abierta.pack(pady=2)
        else:
            etiqueta_abierta = ctk.CTkLabel(
                self.ventana_abierta,
                text="No se pudo cargar la bóveda abierta",
                text_color="red"
            )
            etiqueta_abierta.pack(pady=30)

        self.ventana_abierta.protocol("WM_DELETE_WINDOW", self.cerrar_boveda)

    def cerrar_boveda(self):
        if self.ventana_abierta is not None:
            self.ventana_abierta.destroy()
            self.ventana_abierta = None

    def actualizar_interfaz(self):
        mensajes = self.comunicacion.obtener_datos()

        for msg in mensajes:
            tipo = msg["tipo"]
            valor = msg["valor"]

            if tipo == "datos":
                for i in range(3):
                    self.displays[i].configure(text=str(valor[i]))

            elif tipo == "conectado":
                self.estado.configure(
                    text=f"Arduino conectado ({valor})",
                    text_color="#00FF80"
                )

            elif tipo == "estado":
                self.estado.configure(text=valor, text_color="orange")

            elif tipo == "error":
                self.estado.configure(text="Arduino desconectado", text_color="red")
                print("Error serial:", valor)

        self.ventana.after(50, self.actualizar_interfaz)

    def iniciar(self):
        self.comunicacion.iniciar()
        self.actualizar_interfaz()
        self.ventana.mainloop()

    def cerrar_programa(self):
        self.comunicacion.cerrar()
        self.ventana.destroy()