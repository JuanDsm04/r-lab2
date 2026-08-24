// Capa de Enlace - Orquestador | Receptor
// Responsabilidad: parsear la trama recibida, identificar el algoritmo
// y delegar la verificación/corrección al módulo correspondiente.

package link

import (
	"fmt"
	"strings"
)

// ResultadoEnlace contiene el resultado del procesamiento de la capa de enlace.
type ResultadoEnlace struct {
	BitsMensaje string
	HayError    bool
	MensajeError string
}

// VerificarIntegridad parsea la trama, detecta el algoritmo y verifica/corrige el frame.
// Retorna un ResultadoEnlace con los bits del mensaje o la descripción del error.
func VerificarIntegridad(trama string) ResultadoEnlace {
	fmt.Printf("\n[ENLACE] Procesando trama recibida...\n")

	// Parsear el formato "algoritmo|bits"
	partes := strings.SplitN(trama, "|", 2)
	if len(partes) != 2 {
		return ResultadoEnlace{
			HayError:     true,
			MensajeError: fmt.Sprintf("formato de trama inválido: se esperaba 'algoritmo|bits', se recibió: %q", trama),
		}
	}

	algoritmo := strings.TrimSpace(partes[0])
	frame := strings.TrimSpace(partes[1])

	fmt.Printf("[ENLACE] Algoritmo detectado: %s\n", strings.ToUpper(algoritmo))
	fmt.Printf("[ENLACE] Frame a procesar: %d bits\n", len(frame))

	switch algoritmo {
	case "hamming":
		bits, err := DecodificarHamming(frame)
		if err != nil {
			return ResultadoEnlace{
				HayError:     true,
				MensajeError: fmt.Sprintf("Hamming: %v", err),
			}
		}
		return ResultadoEnlace{BitsMensaje: bits, HayError: false}

	case "crc32":
		bits, err := VerificarCRC32(frame)
		if err != nil {
			return ResultadoEnlace{
				HayError:     true,
				MensajeError: fmt.Sprintf("CRC-32: %v", err),
			}
		}
		return ResultadoEnlace{BitsMensaje: bits, HayError: false}

	default:
		return ResultadoEnlace{
			HayError:     true,
			MensajeError: fmt.Sprintf("algoritmo desconocido: %q. Se esperaba 'hamming' o 'crc32'", algoritmo),
		}
	}
}
