from configuracion import COMBINACION_CORRECTA, INTENTOS_MAXIMOS, DURACION_BLOQUEO


class ControlSeguridad:

    def __init__(self, ventana, obtener_combinacion, mostrar_resultado, mostrar_bloqueo, abrir_boveda):
        self.ventana = ventana
        self.obtener_combinacion = obtener_combinacion
        self.mostrar_resultado = mostrar_resultado
        self.mostrar_bloqueo = mostrar_bloqueo
        self.abrir_boveda = abrir_boveda

        self.intentos_fallidos = 0
        self.bloqueado = False
        self.segundos_restantes = 0
        self.id_temporizador = None

    def comprobar_combinacion(self):
        if self.bloqueado:
            self.mostrar_resultado(
                "Todavía no es posible ingresar el código. Espere a que termine el bloqueo.",
                "red"
            )
            return

        combinacion_ingresada = self.obtener_combinacion()

        if combinacion_ingresada == COMBINACION_CORRECTA:
            self.intentos_fallidos = 0
            self.mostrar_resultado("¡COMBINACIÓN CORRECTA!", "#00FF80")
            self.abrir_boveda()
        else:
            self.intentos_fallidos += 1

            if self.intentos_fallidos >= INTENTOS_MAXIMOS:
                self.iniciar_bloqueo()
            else:
                self.mostrar_resultado("COMBINACIÓN INCORRECTA", "red")

    def iniciar_bloqueo(self):
        self.bloqueado = True
        self.intentos_fallidos = 0
        self.segundos_restantes = DURACION_BLOQUEO

        self.mostrar_resultado("DEMASIADOS INTENTOS INCORRECTOS", "red")
        self.cuenta_regresiva()

    def cuenta_regresiva(self):
        if not self.bloqueado:
            return

        if self.segundos_restantes <= 0:
            self.finalizar_bloqueo()
            return

        self.mostrar_bloqueo(f"TIEMPO DE BLOQUEO: {self.segundos_restantes} segundos")
        self.segundos_restantes -= 1

        self.id_temporizador = self.ventana.after(1000, self.cuenta_regresiva)

    def finalizar_bloqueo(self):
        self.bloqueado = False
        self.intentos_fallidos = 0

        if self.id_temporizador is not None:
            self.ventana.after_cancel(self.id_temporizador)
            self.id_temporizador = None

        self.mostrar_bloqueo("")
        self.mostrar_resultado("Ingrese la combinación", "white")