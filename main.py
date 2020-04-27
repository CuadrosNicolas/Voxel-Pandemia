import math
import json


"""
COMPUTATION FUNCTIONS

Starting from a 3D configurations,
the computation goes to a 1D problem.

For each line of each slice of the cube, compute the number
of infected on a specific day.

Some optimizations are made to avoid line/slice who are already totally infected.
"""


def suit(x, day, size):
    """
    Compute the number of infected during a specific day on a line
    with a starting offset
    :param x: starting offset
    :param day: day to compute
    :param size: lenght of the line
    """
    # Number of day requiered to infect all the line
    nDay = size-x
    # Negative, 0 day or above the nDay return 0 new cases
    if(day > nDay or day <= 0):
        return 0
    # On day 1 only 1 infected appear
    elif(day == 1):
        return 1
    # If it has not reach one end of the line
    # 2 cases appears
    elif day-1 <= x:
        return 2
    # Else only one case can appear
    else:
        return 1


# Some memoization functions
mem = {}


def sliceMem(day, val):
    mem[day] = val


def getSliceMem(day):
    try:
        return mem[day]
    except:
        return None


def resetSliceMem():
    global mem
    mem = {}


def suit2d(yStart, xStart, day, size):
    """
    Compute the number of infected during a specific day on a grid
    with a starting offset
    :param xStart: x starting offset
    :param yStart: y starting offset
    :param day: day to compute
    :param size: size of the grid
    """
    # Verify if has not already been compute.
    memTmp = getSliceMem(day)
    if(memTmp != None):
        return memTmp

    out = 0
    maxDay = (size - yStart) 

    if day <= maxDay:
        out += suit(xStart, day, size)
    _max = day if day <= maxDay else maxDay
    _min = 1 if day - maxDay < 2 else day - maxDay 
    for i in range(_min,_max):
        localLineDay = day-abs(i)
        tmp = suit(xStart,localLineDay, size)
        if(yStart - i>=0):
            tmp *= 2
        out += tmp        


    sliceMem(day, out)

    return out


def suit3d(zStart, yStart, xStart, day, size):
    """
    Compute the number of infected during a specific day in a cube
    with a starting offset
    :param xStart: x starting offset
    :param yStart: y starting offset
    :param zStart: z starting offset
    :param day: day to compute
    :param size: size of the grid
    """
    out = 0

    lenghtZ = (size - zStart)
    # Max day for a slice
    maxDay = (size - yStart) + (size - xStart) - 1

    if day <= maxDay:
        out += suit2d(yStart, xStart, day, size)
        
    _max = day if day <= lenghtZ else lenghtZ
    _min = 1 if day - maxDay < 2 else day - maxDay
    for i in range(_min,_max):
        localSliceDay = day-abs(i)
        tmp = suit2d(yStart, xStart, localSliceDay, size)
        if(zStart - i>=0):
            tmp *= 2
        out += tmp        



    return out


def symetricalCoordinates(xStart, yStart, zStart, size):
    # Convert position into their symetrical version
    # in order to be compatible with the algorithm
    middle = int(math.ceil(size/2))
    TmpMiddle = middle
    if(size % 2 == 0):
        middle += 1
    if(xStart >= middle):
        xStart = xStart - middle
    if(yStart >= middle):
        yStart = yStart - middle
    if(zStart >= middle):
        zStart = zStart - middle
    return [xStart, yStart, zStart]


def getProgression(x, y, z, size):
    """
    Return how the viruses progress depending on the first infected position
    """
    # Empty the function cache
    resetSliceMem()
    day = 1
    addedPerDay = [1]
    [x, y, z] = symetricalCoordinates(x, y, z, size)
    while True:
        day += 1
        tmp = suit3d(z, y, x, day, size)
        if(tmp > 0):
            addedPerDay.append(tmp)
        else:
            break
    return addedPerDay


def getTranslation(size_base):
    """
    Depending on the initial size of the cube
    Yield all possible distinct translation.

    Each distinct translation yield a distinct contamination sequence.

    """
    # Avoid extreme cases with only one possiblity
    if(size_base <= 2):
        yield [0, 0, 0]
    else:
        size = int(math.ceil(size_base/2))
        for i in range(0, size):
            for j in range(0, i+1):
                for k in range(0, j+1):
                    yield [i, j, k]


def fancyPrint(sequence, translations, size):
    print("Sequence : "+str(sequence))
    print("Translation : "+str(translations))
    print("".ljust(
        len("| Jour | Total | Contamination | Pourcentage de contamination |"), "-"))
    print("| Jour | Total | Contamination | Pourcentage de contamination |")
    print("".ljust(
        len("| Jour | Total | Contamination | Pourcentage de contamination |"), "-"))
    contaTotal = 0
    for i in range(len(sequence)):
        jour = str(i+1)
        contaTotal += sequence[i]
        contaCeJour = sequence[i]
        pourcentage = round((float(contaTotal)/float(size**3))*100, 2)
        out = "| "+str(jour).ljust(len("Jour "), " ")+"| "
        out += str(contaTotal).ljust(len("Total "), " ")+"| "
        out += str(contaCeJour).ljust(len("Contamination "), " ")+"| "
        out += (str(pourcentage) +
                "%").ljust(len("Pourcentage de contamination "), " ")+"| "
        print(out)
        print("".ljust(
            len("| Jour | Total | Contamination | Pourcentage de contamination |"), "-"))
    print("")


def main():
    config = None
    with open('config.json') as json_file:
        config = json.load(json_file)
    size = config["cubeSize"]
    limitOne = config["limitOne"]
    sequences = []
    translations = []
    data = []
    for [pX, pY, pZ] in getTranslation(size):
        addedPerDay = getProgression(pX, pY, pZ, size)
        sequences.append(addedPerDay)
        translations.append([pX, pY, pZ])
        data.append([addedPerDay, [pX, pY, pZ]])
        if(limitOne):
            break
    for i in range(len(sequences)):
        fancyPrint(sequences[i], translations[i], size)
    print("Total groups : "+str(len(sequences)))


if __name__ == "__main__":
    main()
