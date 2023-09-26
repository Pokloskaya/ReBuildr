import socket
import threading

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
            fragmentos_para_enviar = self.fragmentos[inicio:fin]

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
                sock.sendall(fragmento.encode())

            # Cerrar la conexión
            sock.close()

        except Exception as e:
            print(f"Error al enviar fragmentos a {host}:{port}: {str(e)}")

# Ejemplo de uso
if __name__ == "__main__":
    # Supongamos que tenemos una lista de fragmentos y una lista de receptores
    fragmentos = ["fragmento1", "fragmento2", "fragmento3", "fragmento4", "fragmento5"]
    receptores = [("127.0.0.1", 5001), ("127.0.0.1", 5002), ("127.0.0.1", 5003)]

    distribuidor = Distribuidor(fragmentos, receptores)
    distribuidor.enviar_fragmentos()
