// Capa de Transmisión | Receptor
// Responsabilidad: escuchar en el puerto 55432 y recibir la trama enviada por el emisor.
// El receptor actúa como servidor TCP: permanece escuchando indefinidamente,
// procesando cada mensaje que llega.

package transmission

import (
	"fmt"
	"io"
	"net"
)

const Puerto = "55432"

// RecibirInformacion inicia el servidor TCP y retorna la trama recibida.
// Bloquea hasta recibir una conexión entrante.
// Retorna la trama completa como string (formato "algoritmo|bits").
func RecibirInformacion(listener net.Listener) (string, error) {
	fmt.Println("[TRANSMISION] Esperando conexión del emisor...")

	conn, err := listener.Accept()
	if err != nil {
		return "", fmt.Errorf("error aceptando conexión: %w", err)
	}
	defer conn.Close()

	fmt.Printf("[TRANSMISION] Conexión recibida desde: %s\n", conn.RemoteAddr())

	// Leer todos los bytes enviados
	datos, err := io.ReadAll(conn)
	if err != nil {
		return "", fmt.Errorf("error leyendo datos: %w", err)
	}

	trama := string(datos)
	fmt.Printf("[TRANSMISION] Trama recibida (%d bytes).\n", len(datos))

	return trama, nil
}

// IniciarServidor crea el listener TCP en el puerto definido.
// Retorna el listener para reutilizarlo entre mensajes.
func IniciarServidor() (net.Listener, error) {
	listener, err := net.Listen("tcp", ":"+Puerto)
	if err != nil {
		return nil, fmt.Errorf("error iniciando servidor en puerto %s: %w", Puerto, err)
	}
	fmt.Printf("[TRANSMISION] Servidor escuchando en puerto %s...\n", Puerto)
	return listener, nil
}
