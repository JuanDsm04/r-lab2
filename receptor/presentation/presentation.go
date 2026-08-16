// Capa de Presentación | Receptor
// Responsabilidad: convertir los bits ASCII binarios de vuelta al texto original.
// Cada grupo de 8 bits representa un carácter ASCII.

package presentation

import (
	"fmt"
	"strconv"
	"strings"
)

// DecodificarMensaje convierte una cadena de bits ASCII binarios al texto original.
// Retorna el mensaje decodificado o un error si los bits están corruptos.
func DecodificarMensaje(bits string) (string, error) {
	if len(bits)%8 != 0 {
		return "", fmt.Errorf(
			"longitud de bits inválida: %d bits (no es múltiplo de 8). El mensaje está corrompido",
			len(bits),
		)
	}

	var sb strings.Builder
	numCaracteres := len(bits) / 8

	for i := 0; i < numCaracteres; i++ {
		grupoBits := bits[i*8 : (i+1)*8]

		// Convertir 8 bits a valor entero
		valor, err := strconv.ParseInt(grupoBits, 2, 64)
		if err != nil {
			return "", fmt.Errorf("error decodificando grupo de bits %q en posición %d: %w", grupoBits, i, err)
		}

		// Verificar que sea un carácter ASCII válido (0-127)
		if valor < 0 || valor > 127 {
			return "", fmt.Errorf("valor ASCII inválido %d en posición %d (grupo: %s)", valor, i, grupoBits)
		}

		sb.WriteRune(rune(valor))
	}

	mensaje := sb.String()
	fmt.Printf("[PRESENTACION] Mensaje decodificado (%d caracteres): %q\n", numCaracteres, mensaje)
	return mensaje, nil
}
