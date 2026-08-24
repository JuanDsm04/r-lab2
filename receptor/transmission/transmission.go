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

// RecibirInformacion espera una conexión entrante y retorna la trama recibida
// (formato "algoritmo|bits") junto con la conexión, que queda abierta para
// poder responderle al emisor. Quien la recibe es responsable de cerrarla.
func RecibirInformacion(listener net.Listener) (string, net.Conn, error) {
	fmt.Println("[TRANSMISION] Esperando conexión del emisor...")

	conn, err := listener.Accept()
	if err != nil {
		return "", nil, fmt.Errorf("error aceptando conexión: %w", err)
	}

	fmt.Printf("[TRANSMISION] Conexión recibida desde: %s\n", conn.RemoteAddr())

	// Leer todos los bytes enviados
	datos, err := io.ReadAll(conn)
	if err != nil {
		conn.Close()
		return "", nil, fmt.Errorf("error leyendo datos: %w", err)
	}

	trama := string(datos)
	fmt.Printf("[TRANSMISION] Trama recibida (%d bytes).\n", len(datos))

	return trama, conn, nil
}

// EnviarRespuesta devuelve al emisor el veredicto del procesamiento:
// "OK|mensaje" si la trama se recuperó, "ERR|motivo" si no fue posible.
func EnviarRespuesta(conn net.Conn, respuesta string) {
	if _, err := conn.Write([]byte(respuesta)); err != nil {
		fmt.Printf("[TRANSMISION] Error enviando respuesta al emisor: %v\n", err)
	}
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
