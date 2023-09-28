
def defineSocketNum(nfragments):# Get the number of elements from the user
    num_elements = nfragments
    RECEPTORS = []
    # Generate the elements and add them to the list
    for i in range(num_elements):
        element = ("127.0.0.1", 5001 + i)
        RECEPTORS.append(element)

    # Print the list
    return RECEPTORS



#RECEPTORS = [("127.0.0.1", 5001), ("127.0.0.1", 5002), ("127.0.0.1", 5003)]
