import socket
import threading

class Receptor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.fragmentos_recibidos = []
        self.replicas_generadas = []
        self.server_socket = None

    def iniciar(self):
        # Crear un socket TCP/IP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Enlazar el socket al host y puerto especificados
        self.server_socket.bind((self.host, self.port))
        
        # Escuchar conexiones entrantes
        self.server_socket.listen(5)
        
        print(f"Receptor en {self.host}:{self.port} listo para recibir fragmentos.")

        while True:
            # Aceptar una conexión entrante
            client_socket, client_address = self.server_socket.accept()
            print(f"Conexión entrante desde {client_address}")

            # Iniciar un hilo para manejar la recepción de fragmentos
            thread = threading.Thread(target=self.recibir_fragmento, args=(client_socket,))
            thread.start()

    def recibir_fragmento(self, client_socket):
        fragmento = client_socket.recv(1024).decode()
        # Almacenar el fragmento recibido
        self.fragmentos_recibidos.append(fragmento)
        print(f"Fragmento recibido en {self.host}:{self.port}: {fragmento}")

        # Decidir si generar una réplica
        if len(self.fragmentos_recibidos) < 2:
            replica = f"Réplica de {fragmento}"
            self.replicas_generadas.append(replica)
            print(f"Réplica generada en {self.host}:{self.port}: {replica}")

        # Cerrar la conexión con el cliente
        client_socket.close()

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar el receptor con la dirección IP y el puerto deseados
    receptor1 = Receptor("127.0.0.1", 5001)
    receptor2 = Receptor("127.0.0.1", 5002)
    receptor3 = Receptor("127.0.0.1", 5003)

    # Iniciar los receptores en hilos separados
    thread1 = threading.Thread(target=receptor1.iniciar)
    thread2 = threading.Thread(target=receptor2.iniciar)
    thread3 = threading.Thread(target=receptor3.iniciar)

    thread1.start()
    thread2.start()
    thread3.start()
