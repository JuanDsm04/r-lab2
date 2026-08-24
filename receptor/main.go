// RECEPTOR

package main

import (
	"fmt"
	"lab2/receptor/application"
	"lab2/receptor/link"
	"lab2/receptor/presentation"
	"lab2/receptor/transmission"
)

func main() {
	fmt.Println()
	fmt.Println("==================================================")
	fmt.Println("       RECEPTOR - Lab 2 CC3067 Redes")
	fmt.Println("==================================================")
	fmt.Println()

	// Iniciar servidor TCP (se mantiene activo entre mensajes)
	listener, err := transmission.IniciarServidor()
	if err != nil {
		fmt.Printf("[ERROR] No se pudo iniciar el servidor: %v\n", err)
		return
	}
	defer listener.Close()

	// Loop principal: procesar mensajes indefinidamente
	for {
		fmt.Println("\nEsperando nuevo mensaje...")

		// Capa de Transmisión
		trama, err := transmission.RecibirInformacion(listener)
		if err != nil {
			fmt.Printf("[TRANSMISION] Error recibiendo trama: %v\n", err)
			continue
		}

		// Capa de Enlace
		resultado := link.VerificarIntegridad(trama)

		if resultado.HayError {
			// Error irrecuperable:
			fmt.Printf("[ENLACE] Error irrecuperable: %s\n", resultado.MensajeError)
			application.MostrarMensaje("", true, resultado.MensajeError)
			continue
		}

		// Capa de Presentación
		fmt.Println("[PRESENTACION] Decodificando bits ASCII a texto...")
		mensaje, err := presentation.DecodificarMensaje(resultado.BitsMensaje)
		if err != nil {
			errMsg := fmt.Sprintf("error de presentación: %v", err)
			fmt.Printf("[PRESENTACION] %s\n", errMsg)
			application.MostrarMensaje("", true, errMsg)
			continue
		}

		// Capa de Aplicación
		application.MostrarMensaje(mensaje, false, "")
	}
}
