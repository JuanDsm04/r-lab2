# Capa de Enlace - CRC-32 | Emisor
# Responsabilidad: calcular el CRC-32 del mensaje y concatenarlo al frame.

# Proceso (división binaria por XOR):
#   1. Agregar 32 ceros al final del mensaje
#   2. Alinear el polinomio al bit más significativo del mensaje
#   3. Realizar XOR y avanzar al siguiente '1' hasta que queden solo 32 bits
#   4. El remainder de 32 bits es el CRC
#   5. Concatenar el CRC al mensaje original


# Polinomio estándar CRC-32
POLINOMIO_CRC32 = "100000100110000010001110110110111"

# Recibe el mensaje en bits y retorna el frame completo: mensaje_original + 32 bits de CRC.
def calcular_crc32(bits_mensaje: str) -> str:
    # Validar que el mensaje tenga al menos 32 bits; si no, agregar padding
    if len(bits_mensaje) < 32:
        padding = 32 - len(bits_mensaje)
        bits_mensaje = ('0' * padding) + bits_mensaje
        print(f"[ENLACE-CRC32] Mensaje menor a 32 bits, se agregaron {padding} bits de padding")

    # Paso 1: agregar 32 ceros al final
    dividendo = bits_mensaje + ('0' * 32)

    print(f"[ENLACE-CRC32] Mensaje ({len(bits_mensaje)} bits) + 32 ceros = {len(dividendo)} bits")

    # Paso 2 y 3: división binaria por XOR
    remainder = _division_binaria_xor(dividendo, POLINOMIO_CRC32)

    remainder = remainder.zfill(32)

    print(f"[ENLACE-CRC32] CRC-32 calculado: {remainder}")

    # Paso 5: frame = mensaje original + CRC
    frame = bits_mensaje + remainder
    print(f"[ENLACE-CRC32] Frame final ({len(frame)} bits): {frame}")
    return frame

# Realiza la división binaria por XOR y retorna el remainder final.
def _division_binaria_xor(dividendo: str, divisor: str) -> str:
    len_divisor = len(divisor)
    resultado = list(dividendo)

    for i in range(len(dividendo) - len_divisor + 1):
        # Solo se opera si el bit actual es '1'
        if resultado[i] == '1':
            for j in range(len_divisor):
                # XOR bit a bit
                resultado[i + j] = '0' if resultado[i + j] == divisor[j] else '1'

    remainder = "".join(resultado[-(len_divisor - 1):])
    return remainder
