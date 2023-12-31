import base64
import os
import json
import sys
import threading
import distribuidor as dist
import constants
import receptor as recep
import shutil
import time
RED = "\033[91m"
RESET = "\033[0m"

class Main:
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
            valuesRegistry = fragments_dict[i].split(b" ")
            registro[i] = ["Sockets_Fragments/", str(valuesRegistry[1])+".json"]

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

        self.organizar_fragmentos(self.fragments)

    def enviar_fragmentos(self, receptores):
        distribuidor = dist.Distribuidor(self.fragments, receptores)
        distribuidor.enviar_fragmentos()

    def recibir_fragmentos(self, host, port):
        # Pasa la instancia del servidor como tercer argumento
        receptor = recep.Receptor(host, port, self)
        receptor.iniciar()

    def Reconstructor(self):
        reconstructed = {}
        time.sleep(5)
        for i in range(self.nFragments):
            with open("Sockets_Fragments/"+str(i)+".json", "r") as fragmentJson:
                data =json.load(fragmentJson)
                reconstructed[i]=data[str(i)]
        reconstructedString = ''  
        for i in range(self.nFragments):
            reconstructedString += reconstructed[i]
        reconstructedString = base64.b64decode(reconstructedString)        
        rdn = "Reconstructed_"+self.fileName.split('/')[-1]+self.ext
        with open("ReconstructedFiles/"+rdn, "wb") as f:
            f.write(reconstructedString)
        print("Reconstructed document saved as '"+rdn+"'")
        return reconstructed
    
    def resetFolder(self):
        shutil.rmtree("Sockets_Fragments/")
        os.makedirs("Sockets_Fragments/")


def main():
    if len(sys.argv) != 3:
        print(
            f"{RED}Syntax command error{RESET}: {sys.argv[0]} <path/fileName.extension> <number of fragments> ")
        sys.exit(1)
    elif not os.path.exists(sys.argv[1]):
        print(
            f"{RED}Path for file doesn't exist:{RESET} {sys.argv[0]} <path/fileName.extension> incorrect")
        sys.exit(1)
    try:
       fullName = sys.argv[1]
       nFragments = int(sys.argv[2])
       fileName, ext = os.path.splitext(fullName)
    except ValueError:
        print(f"{RED}Type of argument error:{RESET} <number of fragments> must be an integer")
        sys.exit(1)

    
    server_instance = Main(fileName, ext, nFragments)
    server_instance.resetFolder()
    res = server_instance.fragmentar_archivo()

    receptores = constants.defineSocketNum(nFragments)
    print(receptores)

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
    time.sleep(1)
    server_instance.Reconstructor()
    # Esperar a que todos los hilos de receptores terminen
    # for thread in threads:
    #   thread.join()
    # Reconstruir el archivo después de que todos los hilos de los receptores hayan terminado



if __name__ == '__main__':
    main()
