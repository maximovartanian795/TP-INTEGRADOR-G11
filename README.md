# TP-INTEGRADOR-G11
Nombre del proyecto e integrantes: Caja Fuerte Digital — Joaquín Madero, Máximo Vartanián y Benjamín Pagliettini   


De qué se trata (idea, cómo se juega, reglas, cómo se gana y cómo se pierde): Adivinar el código secreto de 3 dígitos (0–9) moviendo tres potenciómetros y confirmando con el botón "Acceder" en Tkinter; se gana abriendo la caja y viendo la recompensa si acertás en hasta 3 intentos, y se pierde la ronda si fallás los 3 intentos, activando un bloqueo de 30 segundos antes de volver a tener 3 intentos.


Componentes usados y pines: Arduino Mega, protoboard (5V y GND), tres potenciómetros en A0, A1 y A2, y cables jumper.   


Cómo funciona la comunicación (Arduino ↔ Python): Unidireccional por puerto serie usando pyserial; el Arduino mapea cada potenciómetro del 0 al 9 cuando queda quieto 0,5 segundos y manda esos valores a Python, mientras que Python no le manda nada al Arduino y maneja todo en la ventana de Tkinter.


Cómo ejecutarlo: Instalar pyserial, cargar el .ino en el Arduino Mega desde el Arduino IDE (cerrando el Monitor Serie antes de correr Python) y ejecutar el script .py. 

Cambios respecto al anteproyecto y por qué: Botón "Acceder" en Tkinter en vez de pulsador físico (más dinámico), clave fija predefinida en vez de aleatoria, sin LEDs verde y rojo (redundantes con la interfaz), y sí se hicieron los 3 intentos, el bloqueo de 30 segundos y la estabilización de 0,5 s.
