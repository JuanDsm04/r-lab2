import csv
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR = os.path.dirname(os.path.abspath(__file__))
CSV_ENTRADA = os.path.join(DIR, "resultados.csv")

SUPERFICIE = "#fcfcfb"
TINTA = "#0b0b0b"
TINTA_SUAVE = "#52514e"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]
ESTADO = {"correcto": "#0ca30c", "detectado": "#fab219", "no_detectado": "#d03b3b"}
ETIQUETA = {
    "correcto": "Entregado correctamente",
    "detectado": "Error detectado (descartado)",
    "no_detectado": "Error NO detectado",
}


def cargar():
    with open(CSV_ENTRADA, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def estilo_ejes(ax):
    ax.set_facecolor(SUPERFICIE)
    ax.grid(axis="y", color="#e4e3df", linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color("#d5d4cf")
    ax.tick_params(colors=TINTA_SUAVE, labelsize=9)


def guardar(fig, nombre):
    ruta = os.path.join(DIR, nombre)
    fig.savefig(ruta, dpi=150, bbox_inches="tight", facecolor=SUPERFICIE)
    plt.close(fig)
    print(f"  {ruta}")


# Gráfica 1: tasa de entrega correcta vs tasa de error, una faceta por algoritmo
# y una línea por tamaño de mensaje.
def grafica_exito(filas, algoritmos, tamanos, tasas):
    conteo = defaultdict(lambda: [0, 0])  # (algoritmo, tamaño, tasa) -> [correctos, total]
    for f in filas:
        clave = (f["algoritmo"], int(f["caracteres"]), float(f["tasa_error"]))
        conteo[clave][0] += f["resultado"] == "correcto"
        conteo[clave][1] += 1

    fig, ejes = plt.subplots(1, len(algoritmos), figsize=(11, 4.2), sharey=True)
    fig.patch.set_facecolor(SUPERFICIE)
    x = range(len(tasas))

    for ax, algoritmo in zip(ejes, algoritmos):
        estilo_ejes(ax)
        for i, tamano in enumerate(tamanos):
            y = [100 * conteo[(algoritmo, tamano, t)][0] / conteo[(algoritmo, tamano, t)][1] for t in tasas]
            ax.plot(x, y, color=SERIES[i], linewidth=2, marker="o", markersize=5,
                    label=f"{tamano} caracteres")
            ax.annotate(f"{y[-1]:.0f}%", (x[-1], y[-1]), xytext=(6, 0),
                        textcoords="offset points", color=TINTA_SUAVE, fontsize=8, va="center")
        ax.set_xticks(list(x))
        ax.set_xticklabels([str(t) for t in tasas], rotation=45)
        ax.set_title(algoritmo.upper(), color=TINTA, fontsize=11, pad=10)
        ax.set_xlabel("Tasa de error (errores por bit)", color=TINTA_SUAVE, fontsize=9)

    ejes[0].set_ylabel("Mensajes entregados correctamente (%)", color=TINTA_SUAVE, fontsize=9)
    ejes[0].set_ylim(-4, 108)
    ejes[-1].legend(frameon=False, fontsize=9, labelcolor=TINTA_SUAVE)
    fig.suptitle("Efectividad por algoritmo, tamaño de mensaje y tasa de error",
                 color=TINTA, fontsize=13, x=0.5, y=1.02)
    guardar(fig, "grafica_exito.png")


# Gráfica 2: desglose del resultado de cada envío (correcto / detectado / no detectado).
def grafica_desglose(filas, algoritmos, tasas):
    conteo = defaultdict(lambda: defaultdict(int))
    total = defaultdict(int)
    for f in filas:
        clave = (f["algoritmo"], float(f["tasa_error"]))
        conteo[clave][f["resultado"]] += 1
        total[clave] += 1

    fig, ejes = plt.subplots(1, len(algoritmos), figsize=(11, 4.2), sharey=True)
    fig.patch.set_facecolor(SUPERFICIE)
    x = list(range(len(tasas)))

    for ax, algoritmo in zip(ejes, algoritmos):
        estilo_ejes(ax)
        base = [0.0] * len(tasas)
        for resultado, color in ESTADO.items():
            alturas = [100 * conteo[(algoritmo, t)][resultado] / total[(algoritmo, t)] for t in tasas]
            ax.bar(x, alturas, bottom=base, color=color, width=0.65,
                   edgecolor=SUPERFICIE, linewidth=2, label=ETIQUETA[resultado])
            base = [b + a for b, a in zip(base, alturas)]
        ax.set_xticks(x)
        ax.set_xticklabels([str(t) for t in tasas], rotation=45)
        ax.set_title(algoritmo.upper(), color=TINTA, fontsize=11, pad=10)
        ax.set_xlabel("Tasa de error (errores por bit)", color=TINTA_SUAVE, fontsize=9)

    ejes[0].set_ylabel("Porcentaje de envíos (%)", color=TINTA_SUAVE, fontsize=9)
    ejes[-1].legend(frameon=False, fontsize=9, labelcolor=TINTA_SUAVE,
                    loc="lower left", bbox_to_anchor=(0, -0.45), ncol=3)
    fig.suptitle("Desglose de resultados en el receptor", color=TINTA, fontsize=13, x=0.5, y=1.02)
    guardar(fig, "grafica_desglose.png")


# Gráfica 3: overhead (bits de redundancia respecto a los bits de datos).
def grafica_overhead(filas, algoritmos, tamanos):
    overhead = {}
    bits_datos = {}
    for f in filas:
        overhead[(f["algoritmo"], int(f["caracteres"]))] = 100 * float(f["overhead"])
        bits_datos[int(f["caracteres"])] = int(f["bits_datos"])

    fig, ax = plt.subplots(figsize=(7, 4.2))
    fig.patch.set_facecolor(SUPERFICIE)
    estilo_ejes(ax)

    ancho = 0.36
    for i, algoritmo in enumerate(algoritmos):
        x = [j + (i - 0.5) * ancho for j in range(len(tamanos))]
        y = [overhead[(algoritmo, t)] for t in tamanos]
        ax.bar(x, y, width=ancho - 0.02, color=SERIES[i], label=algoritmo.upper())
        for xi, yi in zip(x, y):
            ax.annotate(f"{yi:.1f}%", (xi, yi), xytext=(0, 4), textcoords="offset points",
                        ha="center", color=TINTA_SUAVE, fontsize=8)

    ax.set_xticks(range(len(tamanos)))
    ax.set_xticklabels([f"{t} chars\n({bits_datos[t]} bits)" for t in tamanos])
    ax.set_xlabel("Tamaño del mensaje", color=TINTA_SUAVE, fontsize=9)
    ax.set_ylabel("Overhead: bits de redundancia / bits de datos (%)", color=TINTA_SUAVE, fontsize=9)
    ax.legend(frameon=False, fontsize=9, labelcolor=TINTA_SUAVE)
    ax.set_title("Costo de redundancia por algoritmo", color=TINTA, fontsize=13, pad=12)
    guardar(fig, "grafica_overhead.png")


def main():
    filas = cargar()
    algoritmos = sorted({f["algoritmo"] for f in filas})
    tamanos = sorted({int(f["caracteres"]) for f in filas})
    tasas = sorted({float(f["tasa_error"]) for f in filas})

    print("Gráficas generadas:")
    grafica_exito(filas, algoritmos, tamanos, tasas)
    grafica_desglose(filas, algoritmos, tasas)
    grafica_overhead(filas, algoritmos, tamanos)


if __name__ == "__main__":
    main()
