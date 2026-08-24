import contextlib
import csv
import io
import os
import random
import string
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "emisor"))

from presentation.presentation import codificar_mensaje
from link.link import calcular_integridad
from noise.noise import aplicar_ruido
from transmission.transmission import enviar_informacion

ALGORITMOS = ["hamming", "crc32"]
TAMANOS = [4, 16, 64]                                        # caracteres por mensaje
TASAS = [0.0, 0.0005, 0.001, 0.005, 0.01, 0.02, 0.05]        # errores por bit transmitido
REPETICIONES = 100

ALFABETO = string.ascii_letters + string.digits + " .,"
CSV_SALIDA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados.csv")


# Las capas del emisor imprimen su traza; en las pruebas se descarta.
@contextlib.contextmanager
def silencio():
    with contextlib.redirect_stdout(io.StringIO()):
        yield


def mensaje_aleatorio(n_caracteres: int) -> str:
    return "".join(random.choice(ALFABETO) for _ in range(n_caracteres))


# Ejecuta un envío completo y clasifica el resultado en:
#   correcto      -> el receptor entregó el mensaje original
#   detectado     -> el receptor reportó error y descartó la trama
#   no_detectado  -> el receptor entregó un mensaje distinto sin darse cuenta
def ejecutar_envio(mensaje: str, algoritmo: str, tasa_error: float) -> dict:
    with silencio():
        bits = codificar_mensaje(mensaje)
        trama = calcular_integridad(bits, algoritmo)
        trama_ruido = aplicar_ruido(trama, tasa_error)
        respuesta = enviar_informacion(trama_ruido)

    frame = trama.split("|", 1)[1]
    errores = sum(1 for a, b in zip(trama, trama_ruido) if a != b)

    if respuesta.startswith("OK|"):
        resultado = "correcto" if respuesta[3:] == mensaje else "no_detectado"
    else:
        resultado = "detectado"

    return {
        "algoritmo": algoritmo,
        "caracteres": len(mensaje),
        "bits_datos": len(bits),
        "bits_trama": len(frame),
        "overhead": round((len(frame) - len(bits)) / len(bits), 4),
        "tasa_error": tasa_error,
        "errores_introducidos": errores,
        "resultado": resultado,
    }


def main():
    repeticiones = int(sys.argv[1]) if len(sys.argv) > 1 else REPETICIONES
    total = len(ALGORITMOS) * len(TAMANOS) * len(TASAS) * repeticiones

    print(f"Ejecutando {total} envíos ({repeticiones} repeticiones por combinación)...\n")
    random.seed(42)

    filas = []
    completados = 0

    for algoritmo in ALGORITMOS:
        for tamano in TAMANOS:
            for tasa in TASAS:
                conteo = {"correcto": 0, "detectado": 0, "no_detectado": 0}
                for _ in range(repeticiones):
                    fila = ejecutar_envio(mensaje_aleatorio(tamano), algoritmo, tasa)
                    filas.append(fila)
                    conteo[fila["resultado"]] += 1
                    completados += 1

                print(
                    f"[{completados:>6}/{total}] {algoritmo:<8} {tamano:>3} chars  "
                    f"tasa={tasa:<7} -> correcto={conteo['correcto']:>4} "
                    f"detectado={conteo['detectado']:>4} no_detectado={conteo['no_detectado']:>4}"
                )

    with open(CSV_SALIDA, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
        escritor.writeheader()
        escritor.writerows(filas)

    print(f"\nResultados guardados en: {CSV_SALIDA}")
    print("Genere las gráficas con: python pruebas/graficas.py")


if __name__ == "__main__":
    try:
        main()
    except ConnectionRefusedError:
        print("\n[!] No hay receptor escuchando. Inicie primero:")
        print("    cd receptor && go run main.go > /dev/null")
        sys.exit(1)
