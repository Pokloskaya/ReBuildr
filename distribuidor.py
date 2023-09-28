import socket
import threading
import json

class Distribuidor:
    def __init__(self, fragmentos, receptores):
        self.fragmentos = fragmentos
        self.receptores = receptores

    def enviar_fragmentos(self):
        # Dividir los fragmentos en partes iguales para enviar a cada receptor
        num_receptores = len(self.receptores)
        fragmentos_por_receptor = len(self.fragmentos) // num_receptores

        for i, receptor in enumerate(self.receptores):
            inicio = i * fragmentos_por_receptor
            fin = (i + 1) * fragmentos_por_receptor if i < num_receptores - 1 else len(self.fragmentos)
            fragmentos_para_enviar = fragmentos_para_enviar = list(self.fragmentos.values())[inicio:fin]

            # Iniciar un hilo para enviar los fragmentos a este receptor
            thread = threading.Thread(target=self.enviar_a_receptor, args=(receptor, fragmentos_para_enviar))
            thread.start()

    def enviar_a_receptor(self, receptor, fragmentos_para_enviar):
        host, port = receptor

        try:
            # Crear un socket TCP/IP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Conectar con el receptor
            sock.connect((host, port))

            # Enviar los fragmentos al receptor
            for fragmento in fragmentos_para_enviar:
                sock.sendall(fragmento)
                print(f"Fragmento enviado {fragmento}")

            # Cerrar la conexión
            sock.close()

        except Exception as e:
            print(f"Error al enviar fragmentos a {host}:{port}: {str(e)}")