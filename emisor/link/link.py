# Capa de Enlace - Orquestador | Emisor
# Responsabilidad: según el algoritmo elegido, calcular la integridad
# y retornar el frame listo para enviarse (con el algoritmo indicado como prefijo).


from link.hamming import codificar_hamming
from link.crc32 import calcular_crc32

# Recibe el mensaje en bits y el algoritmo a usar.
# Retorna el frame completo con prefijo de algoritmo.
def calcular_integridad(bits_mensaje: str, algoritmo: str) -> str:
    print(f"\n[ENLACE] Calculando integridad con algoritmo: {algoritmo.upper()}")

    if algoritmo == "hamming":
        frame = codificar_hamming(bits_mensaje)

    elif algoritmo == "crc32":
        frame = calcular_crc32(bits_mensaje)

    else:
        raise ValueError(f"Algoritmo desconocido: '{algoritmo}'. Use 'hamming' o 'crc32'.")

    trama_final = f"{algoritmo}|{frame}"
    print(f"[ENLACE] Trama lista para transmisión: {algoritmo}|[{len(frame)} bits]")
    return trama_final