# Lab 2 - Redes
## Esquemas de detección y corrección de errores

## Arquitectura

```
EMISOR (Python)          Canal (con ruido)        RECEPTOR (Go)
─────────────────        ─────────────────        ─────────────────
  APLICACIÓN        →                        →      APLICACIÓN
  PRESENTACIÓN      →   bits ASCII binario   →      PRESENTACIÓN
  ENLACE            →   + bits redundancia   →      ENLACE
  RUIDO             →   (errores aleatorios) →
  TRANSMISIÓN       ──────── TCP 55432 ──────→      TRANSMISIÓN
```

## Algoritmos implementados

| Algoritmo | Tipo | Capacidad |
|---|---|---|
| Hamming SEC | Corrección | Corrige 1 bit erróneo |
| CRC-32 | Detección | Detecta errores, no corrige |

## Protocolo de trama

La trama que viaja por el socket tiene el formato:

```
ALGORITMO|BITS_CON_REDUNDANCIA
```

Ejemplos:
- `hamming|010010011000011001001`
- `crc32|01001000...10100010101110110010000011110001`

Tras procesar la trama, el receptor responde por el mismo socket con su veredicto:

```
OK|mensaje_recuperado     ← la trama se recuperó
ERR|motivo                ← error irrecuperable, trama descartada
```

---

## Requisitos

**Emisor (Python):**
- Python 3.10 o superior
- No requiere librerías externas

**Receptor (Go):**
- Go 1.22 o superior
- No requiere dependencias externas

---

## Instrucciones de uso

### 1. Iniciar el receptor (Go)

```bash
cd receptor
go run main.go
```

El receptor quedará escuchando en el puerto **55432**, esperando mensajes del emisor.

### 2. Iniciar el emisor (Python) — en otra terminal

```bash
cd emisor
python main.py
```

El emisor pedirá interactivamente:
1. **Mensaje** a enviar
2. **Algoritmo** a usar: `hamming` o `crc32`
3. **Tasa de error**: probabilidad de que cada bit sea invertido (ej: `0.01` = 1%)

---

## Estructura del proyecto

```
lab2-redes/
│
├── emisor/                          # Python — lado del emisor
│   ├── main.py                      # Entry point: orquesta todas las capas
│   ├── application/
│   │   └── app.py                   # CLI: solicita mensaje, algoritmo y tasa de error
│   ├── presentation/
│   │   └── presentation.py          # Codifica texto → bits ASCII binario (8 bits/char)
│   ├── link/
│   │   ├── link.py                  # Orquestador: selecciona algoritmo y arma la trama
│   │   ├── hamming.py               # Hamming SEC: calcula bits de paridad
│   │   └── crc32.py                 # CRC-32: calcula remainder y lo concatena
│   ├── noise/
│   │   └── noise.py                 # Aplica ruido bit a bit según tasa de error
│   └── transmission/
│       └── transmission.py          # Socket TCP cliente: envía trama y lee el veredicto
│
├── pruebas/                         # Pruebas automatizadas y gráficas
│   ├── pruebas.py                   # Batería de envíos reales → resultados.csv
│   ├── graficas.py                  # resultados.csv → gráficas PNG
│   └── requirements.txt             # matplotlib (solo para las gráficas)
│
└── receptor/                        # Go — lado del receptor
    ├── main.go                      # Entry point: loop de recepción
    ├── go.mod                       # Módulo Go
    ├── transmission/
    │   └── transmission.go          # Socket TCP servidor: escucha en puerto 55432
    ├── link/
    │   ├── link.go                  # Orquestador: parsea trama y delega al algoritmo
    │   ├── hamming.go               # Hamming SEC: detecta y corrige error de 1 bit
    │   └── crc32.go                 # CRC-32: verifica remainder
    ├── presentation/
    │   └── presentation.go          # Decodifica bits ASCII → texto
    └── application/
        └── app.go                   # Muestra el mensaje o el error al usuario
```

---

## Ejemplo de ejecución

### Emisor
```
==================================================
       EMISOR - Lab 2 CC3067 Redes
==================================================

Ingrese el mensaje a enviar: Hello

Algoritmos disponibles:
  [1] hamming  - Corrección de errores (Hamming SEC)
  [2] crc32    - Detección de errores (CRC-32)
Seleccione algoritmo (1/2 o nombre): 1

Tasa de error [0.0 - 1.0]: 0.01

[PRESENTACION] Mensaje codificado (40 bits): 0100100001100101...
[ENLACE-HAMMING] Bits de datos: 40, Bits de paridad: 6, Frame total: 46 bits
[RUIDO] Se introdujeron 1 error(es) en posicion(es): [23]
[TRANSMISION] Trama enviada.
```

### Receptor
```
[TRANSMISION] Conexión recibida desde: 127.0.0.1:XXXXX
[ENLACE] Algoritmo detectado: HAMMING
[ENLACE-HAMMING] Síndrome calculado: 23
[ENLACE-HAMMING] Error detectado en posición 23. Corrigiendo...
[PRESENTACION] Mensaje decodificado (5 caracteres): "Hello"

===================================================
  [APLICACION] Mensaje recibido exitosamente:
  "Hello"
===================================================
```

---

## Pruebas

Las pruebas envían mensajes reales por el stack completo (capas del emisor → socket → receptor
en Go) variando **algoritmo**, **tamaño del mensaje** y **tasa de error**, y clasifican la
respuesta del receptor en tres casos:

| Resultado | Significado |
|---|---|
| `correcto` | El receptor entregó exactamente el mensaje original |
| `detectado` | El receptor detectó el error y descartó la trama |
| `no_detectado` | El receptor entregó un mensaje distinto sin darse cuenta (peor caso) |

### Ejecución

```bash
pip install -r pruebas/requirements.txt

# Terminal 1
cd receptor && go run main.go > /dev/null

# Terminal 2
python pruebas/pruebas.py 100     # 100 repeticiones por combinación (4200 envíos)
python pruebas/graficas.py
```

### Configuración

Las combinaciones se definen al inicio de `pruebas/pruebas.py`:

```python
ALGORITMOS = ["hamming", "crc32"]
TAMANOS    = [4, 16, 64]                                   # caracteres por mensaje
TASAS      = [0.0, 0.0005, 0.001, 0.005, 0.01, 0.02, 0.05] # errores por bit
```

### Salidas

| Archivo | Contenido |
|---|---|
| `pruebas/resultados.csv` | Una fila por envío: algoritmo, tamaño, bits de datos, bits de trama, overhead, tasa, errores introducidos y resultado |
| `pruebas/grafica_exito.png` | % de mensajes entregados correctamente vs tasa de error, por algoritmo y tamaño |
| `pruebas/grafica_desglose.png` | Desglose correcto / detectado / no detectado por algoritmo y tasa |
| `pruebas/grafica_overhead.png` | Overhead (bits de redundancia / bits de datos) por algoritmo y tamaño |

---

## Notas técnicas

- **Hamming SEC**: puede corregir exactamente 1 bit erróneo. Si el ruido provoca 2 o más errores en el frame, la corrección será incorrecta (limitación del algoritmo).
- **CRC-32**: detecta la gran mayoría de errores pero no puede corregirlos. Si se detecta un error, se reporta y el mensaje se descarta.
- **Ruido**: se aplica a todos los bits de la trama incluyendo los bits de redundancia, tal como ocurre en un canal real.
- El receptor corre en un **loop infinito**: procesa cada mensaje que llegue sin necesidad de reiniciarse.
