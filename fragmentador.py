import base64
filename = "testdoc.docx"
nfragments = int(input("Ingrese el numero de fragmentos que espera obtener del archivo "))


def Fragmentador(filename, nfragments):
    file = open(filename, "rb")
    #print(file.read())
    encodedString = base64.b64encode(file.read())
    lenFragments = len(encodedString) // nfragments
    i=0
    fragments = {}
    while i < nfragments:
        if i == nfragments-1:
            subs = encodedString[lenFragments*i:]    
        else:
            subs = encodedString[lenFragments*i:lenFragments*(i+1)]
        fragments[i] = subs
        
        i+=1
    
    return fragments


resultdict = Fragmentador(filename, nfragments)
print(resultdict)
