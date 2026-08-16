# Capa de Enlace - Hamming SEC (Single Error Correction) | Emisor
# Responsabilidad: calcular los bits de paridad e insertarlos en las posiciones correctas.

# Funcionamiento:
#   - Los bits de paridad se ubican en posiciones que son potencias de 2: 1, 2, 4, 8, 16...
#   - Cada bit de paridad cubre las posiciones cuya representación binaria tiene un 1
#     en el bit correspondiente a esa potencia.
#   - El valor de cada bit de paridad es el XOR de todos los bits que cubre.
#   - Se debe cumplir: m + r + 1 <= 2^r
#     donde m = bits de datos, r = bits de paridad


# Calcula el número mínimo de bits de paridad r necesarios para un mensaje de m bits de datos, cumpliendo m + r + 1 <= 2^r.
def _calcular_r(m: int) -> int:
    r = 1
    while (m + r + 1) > (2 ** r):
        r += 1
    return r

# Recibe el mensaje en bits (string de '0' y '1') y retorna el frame Hamming con los bits de paridad insertados.
# Proceso:
#   1. Calcular r (bits de paridad necesarios)
#   2. Construir el frame con posiciones reservadas para paridad (valor inicial 0)
#   3. Insertar los bits de datos en las posiciones que NO son potencia de 2
#   4. Calcular el valor de cada bit de paridad mediante XOR
def codificar_hamming(bits_mensaje: str) -> str:
    m = len(bits_mensaje)
    r = _calcular_r(m)
    n = m + r # longitud total del frame

    print(f"[ENLACE-HAMMING] Bits de datos: {m}, Bits de paridad: {r}, Frame total: {n} bits")

    # Construir frame como lista; índice 0 no se usa (Hamming usa base 1)
    frame = [0] * (n + 1)

    # Insertar bits de datos en posiciones que NO son potencia de 2
    indice_dato = 0
    for pos in range(1, n + 1):
        if not _es_potencia_de_2(pos):
            frame[pos] = int(bits_mensaje[indice_dato])
            indice_dato += 1

    # Calcular el valor de cada bit de paridad
    for i in range(r):
        pos_paridad = 2 ** i
        xor_acumulado = 0
        for pos in range(1, n + 1):
            if pos & pos_paridad:
                xor_acumulado ^= frame[pos]
        frame[pos_paridad] = xor_acumulado

    # Convertir frame (sin el índice 0) a string de bits
    resultado = "".join(str(frame[i]) for i in range(1, n + 1))
    print(f"[ENLACE-HAMMING] Frame codificado: {resultado}")
    return resultado

# Retorna True si n es una potencia de 2
def _es_potencia_de_2(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0