import base64
import os
import json
import sys

class server:

    def __init__(self, fileName, ext, nFragments):
        self.fileName = fileName
        self.ext = ext
        self.nFragments = nFragments

    def organizador(self,fragmentsDict):
        registro = {}
        for i in range(self.nFragments):
            registro[i] = str(fragmentsDict[i])

        with open("Fragments/"+"registro.json", "w") as json_file:
            json.dump(registro, json_file)

    def Fragmentador(self):
        file = open("Files/"+self.fileName+self.ext, "rb")
        encodedString = base64.b64encode(file.read())
        lenFragments = len(encodedString) // self.nFragments
        i = 0
        fragments = {}
        while i < self.nFragments:
            if i == self.nFragments - 1:
                subs = encodedString[lenFragments * i:]
            else:
                subs = encodedString[lenFragments * i: lenFragments * (i + 1)]
            fragments[i] = subs
            i += 1

        print(fragments)
        self.organizador(fragments)
        return fragments    

    def Reconstructor(self, resultdict):
        reconstructed = b''
        for i in range(self.nFragments):
            reconstructed += resultdict[i]
        reconstructed = base64.b64decode(reconstructed)
        return reconstructed

def main():
    if len(sys.argv)!=3:
        print(f"Uso: {sys.argv[0]} <fileName.extension> <number of fragments> ")
        sys.exit(1)

    fullName = sys.argv[1]
    nFragments = int(sys.argv[2])
    fileName, ext = os.path.splitext(fullName)

    serverInit = server(fileName, ext, nFragments)
    resultdict = serverInit.Fragmentador()
    
    #Reconstruct the file
    res = serverInit.Reconstructor(resultdict)
    rdn = "Reconstructed_"+fileName+ext
    with open("RecontructedFiles/"+rdn, "wb") as f:
        f.write(res)

    print("Reconstructed document saved as '"+rdn+"'")

if __name__ == '__main__':
    main()