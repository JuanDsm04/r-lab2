# Capa de Ruido | Emisor
# Responsabilidad: simular interferencias en el canal aplicando errores aleatorios
# bit a bit a la trama (incluyendo los bits de redundancia).


import random

# Recibe la trama completa con formato "algoritmo|bits".
# Aplica ruido solo a la parte de bits (no al prefijo).
# Retorna la trama con los bits modificados según la tasa de error.
def aplicar_ruido(trama: str, tasa_error: float) -> str:
    if tasa_error == 0.0:
        print("[RUIDO] Tasa de error = 0. No se aplica ruido.")
        return trama

    # Separar prefijo de bits
    separador = trama.index("|")
    prefijo = trama[:separador + 1] # "algoritmo|"
    bits = trama[separador + 1:] # los bits de la trama

    bits_alterados = list(bits)
    errores_introducidos = 0
    posiciones_error = []

    for i, bit in enumerate(bits_alterados):
        if random.random() < tasa_error:
            # Invertir el bit
            bits_alterados[i] = '1' if bit == '0' else '0'
            errores_introducidos += 1
            posiciones_error.append(i + 1)  # base 1 para legibilidad

    bits_resultado = "".join(bits_alterados)

    if errores_introducidos > 0:
        print(f"[RUIDO] Se introdujeron {errores_introducidos} error(es) en posicion(es): {posiciones_error}")
    else:
        print(f"[RUIDO] Tasa={tasa_error}. No se introdujeron errores esta vez.")

    return prefijo + bits_resultado