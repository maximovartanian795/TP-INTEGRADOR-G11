import customtkinter as ctk
import interfaz


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = interfaz.Aplicacion()
    app.iniciar()


if __name__ == "__main__":
    main()