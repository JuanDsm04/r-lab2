// Capa de Enlace - CRC-32 | Receptor
// Responsabilidad: verificar la integridad del frame recibido mediante CRC-32.
//
// Proceso de verificación
//  1. Tomar el frame completo (mensaje original + 32 bits CRC)
//  2. Dividirlo entre el polinomio estándar usando XOR
//  3. Si el remainder es 0 → no hay errores
//     Si el remainder != 0 → se detectó un error
//  4. CRC-32 NO puede corregir errores, solo detectarlos
//  5. Si no hay error, extraer el mensaje original (frame sin los últimos 32 bits)

package link

import (
	"fmt"
	"strings"
)

// Polinomio estándar CRC-32
const polinomioCRC32 = "100000100110000010001110110110111"

// VerificarCRC32 recibe el frame completo (mensaje + 32 bits CRC).
// Retorna los bits del mensaje original (sin el CRC) y un error si se detectaron errores.
func VerificarCRC32(frame string) (string, error) {
	n := len(frame)
	fmt.Printf("[ENLACE-CRC32] Frame recibido (%d bits)\n", n)

	if n < 32 {
		return "", fmt.Errorf("frame demasiado corto (%d bits), se esperan al menos 32 bits de CRC", n)
	}

	// Verificar: dividir el frame entre el polinomio
	remainder := divisionBinariaXOR(frame, polinomioCRC32)
	// El remainder debe ser 32 bits de ceros si no hay error
	remainder = fmt.Sprintf("%032s", remainder) // padding a 32 bits

	fmt.Printf("[ENLACE-CRC32] Remainder calculado: %s\n", remainder)

	// Verificar si el remainder es todo ceros
	solosCeros := true
	for _, c := range remainder {
		if c != '0' {
			solosCeros = false
			break
		}
	}

	if !solosCeros {
		return "", fmt.Errorf("error detectado (remainder != 0). No es posible corregir con CRC-32")
	}

	fmt.Println("[ENLACE-CRC32] No se detectaron errores.")

	// Extraer solo el mensaje original (sin los últimos 32 bits de CRC)
	mensajeBits := frame[:n-32]
	fmt.Printf("[ENLACE-CRC32] Bits de mensaje extraídos (%d bits)\n", len(mensajeBits))
	return mensajeBits, nil
}

// divisionBinariaXOR realiza la división binaria por XOR.
// Retorna el remainder de la división.
func divisionBinariaXOR(dividendo, divisor string) string {
	lenDivisor := len(divisor)
	resultado := []byte(dividendo)

	for i := 0; i <= len(resultado)-lenDivisor; i++ {
		if resultado[i] == '1' {
			for j := 0; j < lenDivisor; j++ {
				if resultado[i+j] == divisor[j] {
					resultado[i+j] = '0'
				} else {
					resultado[i+j] = '1'
				}
			}
		}
	}

	remainder := string(resultado[len(resultado)-(lenDivisor-1):])
	return strings.TrimLeft(remainder, "0")
}
