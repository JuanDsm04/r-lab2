# EMISOR

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from application.app import solicitar_mensaje
from presentation.presentation import codificar_mensaje
from link.link import calcular_integridad
from noise.noise import aplicar_ruido
from transmission.transmission import enviar_informacion


def main():
    print()

    # Capa de Aplicación
    mensaje, algoritmo, tasa_error = solicitar_mensaje()

    # Capa de Presentación
    print("[PRESENTACION] Codificando mensaje a ASCII binario...")
    bits_mensaje = codificar_mensaje(mensaje)

    # Capa de Enlace
    trama = calcular_integridad(bits_mensaje, algoritmo)

    # Capa de Ruido
    print(f"\n[RUIDO] Aplicando ruido con tasa de error = {tasa_error}...")
    trama_con_ruido = aplicar_ruido(trama, tasa_error)

    # Capa de Transmisión
    enviar_informacion(trama_con_ruido)

    print("\n[EMISOR] Transmisión completada.\n")

if __name__ == "__main__":
    main()
