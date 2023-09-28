import socket
import threading
import json

class Receptor:
    def __init__(self, host, port, server):
        self.host = host
        self.port = port
        self.fragmentos = []  # Lista para almacenar fragmentos recibidos
        self.server = server
        self.fileName = server.fileName
        self.ext = server.ext
        self.should_stop = False  # Variable de control para detener el bucle

    def iniciar(self):
        # Crear un socket TCP/IP
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Enlazar el socket al host y puerto especificados
        self.server_socket.bind((self.host, self.port))

        # Escuchar conexiones entrantes
        self.server_socket.listen(5)

        print(
            f"Receptor en {self.host}:{self.port} listo para recibir fragmentos.")

        while not self.should_stop:
            # Aceptar una conexión entrante
            client_socket, client_address = self.server_socket.accept()
            print(f"Conexión entrante desde {client_address}")

            # Iniciar un hilo para manejar la recepción de fragmentos
            thread = threading.Thread(
                target=self.recibir_fragmento, args=(client_socket,))
            thread.start()

        # Cerrar el socket del servidor cuando termine la recepción de fragmentos
        self.server_socket.close()

    def recibir_fragmento(self, client):
        # Almacenar el fragmento recibido como bytes en la lista de fragmentos
        data= client.recv(1000000)
        fragmento= str(data.decode("utf-8"))
        #print(f"Fragmento recibido: {fragmento}")
        elementos= fragmento.split(' ')
        newJson = {elementos[1]:elementos[2]}
        with open("Sockets_Fragments/" + elementos[1]+".json", "w") as json_file:
            json.dump(newJson, json_file)
        self.should_stop = True
