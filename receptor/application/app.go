// Capa de Aplicación | Receptor
// Responsabilidad: mostrar el mensaje recibido al usuario final.
// Si el mensaje llegó sin errores (o fue corregido), se muestra el texto.
// Si hubo un error irrecuperable, se muestra un mensaje de error claro.

package application

import "fmt"

// MostrarMensaje imprime el mensaje recibido o el error correspondiente.
//
// Parámetros:
//  - mensaje: el texto decodificado (vacío si hay error)
//  - hayError: true si ocurrió un error irrecuperable
//  - mensajeError: descripción del error (relevante solo si hayError == true)
func MostrarMensaje(mensaje string, hayError bool, mensajeError string) {
	fmt.Println()
	fmt.Println("===================================================")
	if hayError {
		fmt.Println("[APLICACION] * ERROR DE TRANSMISIÓN *")
		fmt.Printf(" - Motivo: %s\n", mensajeError)
		fmt.Println(" - El mensaje no pudo ser recuperado.")
	} else {
		fmt.Println("[APLICACION] Mensaje recibido exitosamente:")
		fmt.Printf("%q\n", mensaje)
	}
	fmt.Println("===================================================")
	fmt.Println()
}
