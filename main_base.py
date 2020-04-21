import time
import math
import numpy as np
import json
"""
Straightforward solution using previous iterations to know the next one.
"""
def fancyPrint(sequence, translations,size):
    print("Sequence : "+str(sequence))
    print("Translation : "+str(translations))
    print("".ljust(len("| Jour | Total | Contamination | Pourcentage de contamination |"),"-"))
    print("| Jour | Total | Contamination | Pourcentage de contamination |")
    print("".ljust(len("| Jour | Total | Contamination | Pourcentage de contamination |"),"-"))
    contaTotal = 0
    for i in range(len(sequence)):
        jour = str(i+1)
        contaTotal += sequence[i]
        contaCeJour = sequence[i]
        pourcentage = round((float(contaTotal)/float(size**3))*100,2)
        out = "| "+str(jour).ljust(len("Jour ")," ")+"| "
        out += str(contaTotal).ljust(len("Total ")," ")+"| "
        out += str(contaCeJour).ljust(len("Contamination ")," ")+"| "
        out += (str(pourcentage)+"%").ljust(len("Pourcentage de contamination ")," ")+"| "
        print(out)
        print("".ljust(len("| Jour | Total | Contamination | Pourcentage de contamination |"),"-"))
    print("")

def getTranslation(size_base):
    """
    Depending on the initial size of the cube
    Yield all possible distinct translation.

    Each distinct translation yield a distinct contamination sequence.

    """
    #Avoid extreme cases with only one possiblity
    if(size_base<=2):
        yield [0,0,0]
    else:
        size = int(math.ceil(size_base/2))
        for i in range(0,size):
            for j in range(0,i+1):
                for k in range(0,j+1):
                    yield [i,j,k]

def main():

    config = None
    with open('config.json') as json_file:
        config = json.load(json_file)
    size = config["cubeSize"]

    def validPlace(x,y,k):
        return x>=0 and x<size and y>=0 and y<size and k>=0 and k<size
    def testCasesOf(i,j,k):
        return [
                [i + 1,j,k] ,
                [i - 1,j,k],
                [i, j + 1, k ],
                [i, j - 1, k ],
                [i,j,k-1],
                [i,j,k+1]
            ]

    sequences = [] 
    translations = []
    for [pX,pY,pZ] in getTranslation(size):
        translations.append([pX,pY,pZ])
        testCases = [[pX,pY,pZ]]
        arr = np.full([size,size,size],0)
        arr[pX][pY][pZ] = 1
        day = 1
        sequences.append([1])
        while len(testCases):
            day+=1
            nextTestCases = []
            contaminated = 0
            for [x,y,z] in testCases:
                for [i,j,k] in testCasesOf(x,y,z):
                    if(validPlace(i,j,k) 
                    and not(arr[i][j][k])):
                        contaminated += 1
                        arr[i][j][k] = 1
                        nextTestCases.append([i,j,k])
            sequences[-1].append(contaminated)
            testCases = np.copy(nextTestCases)
            if(not(len(testCases))):
                sequences[-1].pop()
    for i in range(len(sequences)):
        fancyPrint(sequences[i],translations[i],size)
    print("Total groups : "+str(len(sequences)))
if __name__ == "__main__": 
    main() 