
import math
"""
COMPUTATION FUNCTIONS

Starting from a 3D configurations,
the computation goes to a 1D problem.

For each line of each slice of the cube, compute the number
of infected on a specific day.

Some optimizations are made to avoid line/slice who are already totally infected.
"""
def suit(x,day,size):
    nDay = size-x
    if(day>nDay or day <=0):
        return 0
    elif(day==1):
        return 1
    elif day-1<=x:
        return 2
    else:
        return 1

def suit2d(ySource, x,y,day,size):
    return suit(x,day-abs(ySource-y), size)

def suit3d(zSource,ySource,xStart,z,day,size):
    sliceDay = day-abs(zSource-z)
    out = 0
    maxDay = (size - ySource) + (size -xStart)

    minBottom = ySource
    if(sliceDay>=maxDay):
        minBottom = ySource + (maxDay-sliceDay)

    for i in range(minBottom,size):
        out += suit2d(ySource, xStart,i, day-abs(zSource-z), size)

    for i in range(0,minBottom):
        out += suit2d(ySource, xStart, i, day-abs(zSource-z), size)

    return out

"""
PROBLEM SOLUTION PART
"""

def compute3d(xStart, yStart, zStart, day, size):
    """
    Return how many cases appear during a specific day
    """
    out = 0
    maxDay = (size - yStart) + (size -xStart) + (size - zStart)
    minBottom = zStart
    if(day>=maxDay):
        minBottom = zStart + (maxDay-day)

    for i in range(minBottom,size):
        out += suit3d(zStart, yStart,xStart, i, day, size)

    for i in range(0,minBottom):
        out += suit3d(zStart, yStart,xStart, i, day, size)
    return out

def getProgression(x,y,z, size):
    """
    Return how the viruses progress depending on the first infected position
    """
    day = 1
    addedPerDay = [compute3d(x, y, z, day, size)]
    while True:
        day += 1
        tmp = compute3d(x, y, z, day, size)
        if(tmp>0):
            addedPerDay.append(tmp)
        else:
            break
    return addedPerDay

def getTranslation(size):
    """
    Depending on the initial size of the cube
    Yield all possible distinct translation.

    Each distinct translation yield a distinct contamination sequence.

    """
    for i in range(0,size+1):
        for j in range(0,i+1):
            for k in range(0,j+1):
                yield [i,j,k]

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

def main():
    size = 5 # <------- Change the cube size here
    sequences = [] 
    translations = []
    for [pX,pY,pZ] in getTranslation(int(math.ceil(size/2))):
        addedPerDay = getProgression(pX,pY,pZ,size)
        sequences.append(addedPerDay)
        translations.append([pX,pY,pZ])
    for i in range(len(sequences)):
        fancyPrint(sequences[i],translations[i],size)
    print("Total groups : "+str(len(sequences)))


if __name__ == "__main__":
    main()