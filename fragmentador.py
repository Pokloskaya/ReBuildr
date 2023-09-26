import base64
import os
import json

filename = "testfile.txt"
name, ext = os.path.splitext(filename)
nfragments = int(input("Ingrese el numero de fragmentos que espera obtener del archivo "))

def organizador(fragments):
    registro = {}
    for i in range(nfragments):
        registro[i] = str(fragments[i])

    with open("registro.json", "w") as json_file:
        json.dump(registro, json_file)


def Fragmentador(filename, nfragments):
    file = open(filename, "rb")
    encodedString = base64.b64encode(file.read())
    lenFragments = len(encodedString) // nfragments
    i = 0
    fragments = {}
    while i < nfragments:
        if i == nfragments - 1:
            subs = encodedString[lenFragments * i:]
        else:
            subs = encodedString[lenFragments * i: lenFragments * (i + 1)]
        fragments[i] = subs
        i += 1
    organizador(fragments)
    return fragments

resultdict = Fragmentador(filename, nfragments)


def Reconstructor(resultdict):
    reconstructed = b''
    for i in range(nfragments):
        reconstructed += resultdict[i]
    reconstructed = base64.b64decode(reconstructed)
    return reconstructed

res = Reconstructor(resultdict)
rdn = "Reconstructed_"+name+ext
with open(rdn, "wb") as f:
    f.write(res)

print("Reconstructed document saved as '"+rdn+"'")