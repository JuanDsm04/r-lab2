# Capa de Aplicación | Emisor
# Responsabilidad: solicitar al usuario el mensaje, el algoritmo y la tasa de ruido.


# Le solicita al usuario:
# - El texto a enviar
# - El algoritmo a usar (hamming | crc32)
# - La tasa de error (errores por bit transmitido)
# Retorna: (mensaje, algoritmo, tasa_error)
def solicitar_mensaje() -> tuple[str, str, float]:
    print("=" * 50)
    print("       EMISOR - Lab 2 CC3067 Redes")
    print("=" * 50)

    # Mensaje
    mensaje = input("\nIngrese el mensaje a enviar: ").strip()
    while not mensaje:
        print("  [!] El mensaje no puede estar vacío.")
        mensaje = input("Ingrese el mensaje a enviar: ").strip()

    # Algoritmo
    print("\nAlgoritmos disponibles:")
    print("  [1] hamming  - Corrección de errores (Hamming SEC)")
    print("  [2] crc32    - Detección de errores (CRC-32)")
    algoritmo_input = input("Seleccione algoritmo (1 | 2): ").strip().lower()

    mapa = {"1": "hamming", "2": "crc32"}
    while algoritmo_input not in mapa:
        print("  [!] Opción inválida. Use 1, 2, 'hamming' o 'crc32'.")
        algoritmo_input = input("Seleccione algoritmo (1 | 2): ").strip().lower()
    algoritmo = mapa[algoritmo_input]

    # Tasa de error
    print("\nTasa de error: probabilidad de que cada bit sea invertido.")
    print("  Ejemplos: 0.01 (1 error c/100 bits), 0.001 (1 error c/1000 bits), 0 (sin ruido)")
    while True:
        tasa_input = input("Ingrese la tasa de error [0.0 - 1.0]: ").strip()
        try:
            tasa = float(tasa_input)
            if 0.0 <= tasa <= 1.0:
                break
            print("  [!] Debe ser un valor entre 0.0 y 1.0.")
        except ValueError:
            print("  [!] Ingrese un número decimal válido.")

    print("\nResumen de la configuración:")
    print(f"\n - Mensaje   : '{mensaje}'")
    print(f" - Algoritmo : {algoritmo.upper()}")
    print(f" - Tasa error: {tasa}")
    print()

    return mensaje, algoritmo, tasa
