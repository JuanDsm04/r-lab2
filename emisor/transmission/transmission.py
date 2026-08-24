# Capa de Transmisión | Emisor
# Responsabilidad: enviar la trama al receptor a través de un socket TCP.

# El emisor actúa como cliente: se conecta al receptor (servidor) en el
# host y puerto especificados, envía la trama y cierra la conexión.


import socket

HOST_RECEPTOR = "127.0.0.1"  # localhost por defecto; se puede cambiar si el receptor está en otra máquina
PUERTO = 55432

# Envía la trama completa al receptor por TCP y espera su veredicto.
# Parámetros:
#   trama: string con formato "algoritmo|bits_de_trama"
# Retorna: la respuesta del receptor, "OK|mensaje" o "ERR|motivo"
def enviar_informacion(trama: str) -> str:
    print(f"\n[TRANSMISION] Conectando a {HOST_RECEPTOR}:{PUERTO}...")

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST_RECEPTOR, PUERTO))
            print(f"[TRANSMISION] Conexión establecida.")

            # Codificar y enviar
            trama_bytes = trama.encode('utf-8')
            s.sendall(trama_bytes)

            print(f"[TRANSMISION] Trama enviada ({len(trama_bytes)} bytes, {len(trama)} caracteres).")

            # Cerrar el sentido de escritura para que el receptor detecte el fin
            # de la trama, y quedarse a la espera de su veredicto.
            s.shutdown(socket.SHUT_WR)

            respuesta = b""
            while True:
                bloque = s.recv(4096)
                if not bloque:
                    break
                respuesta += bloque

            veredicto = respuesta.decode('utf-8')
            print(f"[TRANSMISION] Respuesta del receptor: {veredicto}")
            return veredicto

    except ConnectionRefusedError:
        print(f"[TRANSMISION] ERROR: No se pudo conectar a {HOST_RECEPTOR}:{PUERTO}.")
        print("  Asegúrese de que el receptor esté corriendo antes de enviar.")
        raise

    except Exception as e:
        print(f"[TRANSMISION] ERROR inesperado: {e}")
        raise