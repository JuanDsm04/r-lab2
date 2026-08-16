# Capa de Presentación | Emisor
# Responsabilidad: codificar cada carácter del mensaje en su representación ASCII binaria de 8 bits.


# Convierte cada carácter del mensaje en 8 bits ASCII binario.
# Retorna un string de bits concatenados.
def codificar_mensaje(mensaje: str) -> str:
    bits = ""
    for caracter in mensaje:
        codigo_ascii = ord(caracter)
        bits_char = format(codigo_ascii, '08b')  # siempre 8 bits, con padding de ceros
        bits += bits_char

    print(f"[PRESENTACION] Mensaje codificado ({len(bits)} bits): {bits}")
    return bits