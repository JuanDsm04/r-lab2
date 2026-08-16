// Capa de Enlace - Hamming SEC (Single Error Correction) | Receptor
// Responsabilidad: recibir el frame Hamming, verificar integridad y corregir
// el error si existe (máximo 1 bit).
//
// Proceso de decodificación (según módulo III del curso CC3067):
//  1. Identificar las posiciones de los bits de paridad (potencias de 2)
//  2. Recalcular el XOR de cada grupo de bits cubiertos por cada paridad
//  3. Formar el "síndrome": concatenar los resultados (en orden inverso de potencia)
//  4. Si el síndrome es 0 → no hay error
//     Si el síndrome != 0 → indica la posición del bit erróneo (en base 1)
//  5. Corregir el bit en esa posición
//  6. Extraer solo los bits de datos (los que NO están en posiciones potencia de 2)

package link

import (
	"fmt"
	"math/bits"
	"strconv"
	"strings"
)

// DecodificarHamming recibe el frame Hamming como string de bits.
// Retorna los bits de datos originales (sin bits de paridad) y un error si no pudo corregir.
func DecodificarHamming(frame string) (string, error) {
	n := len(frame)
	fmt.Printf("[ENLACE-HAMMING] Frame recibido (%d bits): %s\n", n, frame)

	// Convertir el frame a slice de enteros (base 1: frame[0] no se usa)
	frameBits := make([]int, n+1)
	for i := 0; i < n; i++ {
		if frame[i] == '1' {
			frameBits[i+1] = 1
		} else {
			frameBits[i+1] = 0
		}
	}

	// Calcular cuántos bits de paridad tiene este frame
	r := calcularR(n)

	// Recalcular cada bit de paridad y construir el síndrome
	sindrome := 0
	for i := 0; i < r; i++ {
		posParidad := 1 << i // 1, 2, 4, 8...
		xorAcumulado := 0
		for pos := 1; pos <= n; pos++ {
			if pos&posParidad != 0 {
				xorAcumulado ^= frameBits[pos]
			}
		}
		// El bit i del síndrome corresponde a la paridad de posición 2^i
		if xorAcumulado != 0 {
			sindrome |= posParidad
		}
	}

	fmt.Printf("[ENLACE-HAMMING] Síndrome calculado: %d\n", sindrome)

	if sindrome != 0 {
		// El síndrome indica la posición del bit erróneo (base 1)
		posError := sindrome
		if posError > n {
			return "", fmt.Errorf("error en posición %d, fuera del rango del frame (%d bits). No se puede corregir", posError, n)
		}
		fmt.Printf("[ENLACE-HAMMING] Error detectado en posición %d. Corrigiendo...\n", posError)
		// Invertir el bit erróneo
		frameBits[posError] ^= 1
		fmt.Printf("[ENLACE-HAMMING] Bit corregido en posición %d.\n", posError)
	} else {
		fmt.Println("[ENLACE-HAMMING] No se detectaron errores.")
	}

	// Extraer solo los bits de datos (posiciones que NO son potencia de 2)
	var datosBits strings.Builder
	for pos := 1; pos <= n; pos++ {
		if !esPotenciaDe2(pos) {
			datosBits.WriteString(strconv.Itoa(frameBits[pos]))
		}
	}

	resultado := datosBits.String()
	fmt.Printf("[ENLACE-HAMMING] Bits de datos extraídos (%d bits): %s\n", len(resultado), resultado)
	return resultado, nil
}

// calcularR determina cuántos bits de paridad tiene un frame de longitud n.
// Busca r tal que 2^r >= n + 1 (propiedad de Hamming).
func calcularR(n int) int {
	r := 0
	for (1 << r) <= n {
		r++
	}
	// Retornamos el número de bits de paridad contando las potencias de 2 <= n
	count := 0
	for i := 0; (1 << i) <= n; i++ {
		count++
	}
	return count
}

// esPotenciaDe2 retorna true si n es una potencia de 2.
func esPotenciaDe2(n int) bool {
	return n > 0 && bits.OnesCount(uint(n)) == 1
}
