import base64
import os
import json
import sys
import threading
import distribuidor as dist
import constants
import receptor as recep


class Server:
    def __init__(self, fileName, ext, nFragments):
        self.fileName = fileName
        self.ext = ext
        self.nFragments = nFragments
        self.fragmentos = []
        self.fragmentos_recibidos = []
        self.received_count = 0

    def organizar_fragmentos(self, fragments_dict):
        registro = {}
        for i in range(self.nFragments):
            registro[i] = str(fragments_dict[i])

        with open("Fragments/" + "registro.json", "w") as json_file:
            json.dump(registro, json_file)

    def fragmentar_archivo(self):
        file = open(self.fileName + self.ext, "rb")
        encoded_string = base64.b64encode(file.read())
        len_fragments = len(encoded_string) // self.nFragments
        i = 0
        self.fragments = {}
        while i < self.nFragments:
            if i == self.nFragments - 1:
                subs = encoded_string[len_fragments * i:]
            else:
                subs = encoded_string[len_fragments *
                                      i: len_fragments * (i + 1)]
            self.fragments[i] = (self.fileName + " " + str(i) + " ").encode('utf-8') + subs
            i += 1

        print(self.fragments)
        self.organizar_fragmentos(self.fragments)

    def enviar_fragmentos(self, receptores):
        distribuidor = dist.Distribuidor(self.fragments, receptores)
        distribuidor.enviar_fragmentos()

    def recibir_fragmentos(self, host, port):
        # Pasa la instancia del servidor como tercer argumento
        receptor = recep.Receptor(host, port, self)
        receptor.iniciar()

    # def reconstruir_archivo(self):
    #     reconstructed = b''

    #     # Obtén la lista de fragmentos recibidos del receptor
    #     fragmentos_recibidos = self.fragmentos_recibidos

    #     for i in range(self.nFragments):
    #         if i < len(fragmentos_recibidos):
    #             # Cambiar el índice i para obtener el fragmento recibido por el receptor
    #             fragmento_recibido = fragmentos_recibidos[i]
    #             reconstructed += base64.b64decode(fragmento_recibido)

    #     rdn = "Reconstructed_" + self.fileName + self.ext
    #     with open("ReconstructedFiles/" + rdn, "wb") as f:
    #         f.write(reconstructed)
    #     print("Documento reconstruido guardado como '" + rdn + "'")

    def Reconstructor(self):
        reconstructed = b''
        for i in range(self.nFragments):
            reconstructed += self.fragments[i]
        reconstructed = base64.b64decode(reconstructed)

        rdn = "Reconstructed_"+self.fileName.split('/')[-1]+self.ext
        with open("ReconstructedFiles/"+rdn, "wb") as f:
            f.write(reconstructed)

        print("Reconstructed document saved as '"+rdn+"'")
        return reconstructed


def main():
    if len(sys.argv) != 3:
        print(
            f"Uso: {sys.argv[0]} <fileName.extension> <number of fragments> ")
        sys.exit(1)

    fullName = sys.argv[1]
    nFragments = int(sys.argv[2])
    fileName, ext = os.path.splitext(fullName)

    server_instance = Server(fileName, ext, nFragments)
    res = server_instance.fragmentar_archivo()

    receptores = constants.RECEPTORS

    # Iniciar receptores en hilos separados
    threads = []
    for receptor in receptores:
        host, port = receptor
        thread = threading.Thread(
            target=server_instance.recibir_fragmentos, args=(host, port))
        thread.start()
        threads.append(thread)

    # Esperar a que los receptores estén listos
    input("Presiona Enter cuando los receptores estén listos para recibir fragmentos...")

    # Enviar fragmentos a los receptores
    server_instance.enviar_fragmentos(receptores)
    server_instance.Reconstructor()
    # Esperar a que todos los hilos de receptores terminen
    # for thread in threads:
    #   thread.join()
    # time.sleep(5)
    # Reconstruir el archivo después de que todos los hilos de los receptores hayan terminado


if __name__ == '__main__':
    main()
