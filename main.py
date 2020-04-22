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
    nDay = size-x
    if(day > nDay or day <= 0):
        return 0
    elif(day == 1):
        return 1
    elif day-1 <= x:
        return 2
    else:
        return 1


def suit2d(yStart, xStart, y, day, size):
    return suit(xStart, day-abs(yStart-y), size)


# Some memoization function
mem = {}


def sliceMem(x, y, day, val):
    if(not(x in mem.keys())):
        mem[x] = {}
    if(not(y in mem[x].keys())):
        mem[x][y] = {}
    if(not(day in mem[x][y].keys())):
        mem[x][y][day] = val


def getSliceMem(x, y, day):
    try:
        return mem[x][y][day]
    except:
        return None


def resetSliceMem():
    mem = {}


def suit3d(zSource, ySource, xStart, z, day, size):
    sliceDay = day-abs(zSource-z)

    # Get the memoize value if ones exist
    memTmp = getSliceMem(xStart, ySource, sliceDay)
    if(memTmp != None):
        return memTmp

    out = 0
    maxDay = (size - ySource) + (size - xStart)
    lineMaxDay = size - xStart
    lenghtY = (size - ySource)

    _max = int(sliceDay if sliceDay <= lenghtY else lenghtY)
    _min = int(0 if sliceDay <= lenghtY else sliceDay - lenghtY)

    for i in range(ySource + _min, ySource+_max):
        out += suit2d(ySource, xStart, i, day-abs(zSource-z), size)

    _max = sliceDay if sliceDay <= ySource else ySource
    _min = int(0 if sliceDay <= lenghtY else sliceDay - lenghtY - 1)
    for i in range(ySource - _max, ySource - _min):
        out += suit2d(ySource, xStart, i, day-abs(zSource-z), size)

    sliceMem(xStart, ySource, day, out)
    return out


"""
PROBLEM SOLUTION PART
"""


def compute3d(xStart, yStart, zStart, day, size):
    # Convert position into their symetrical version
    # in order to be compatible with the algorithm
    middle = int(math.ceil(size/2))
    if(xStart > middle):
        xStart = xStart - middle
    if(yStart > middle):
        yStart = yStart - middle
    if(zStart > middle):
        zStart = zStart - middle

    """
    Return how many cases appear during a specific day
    """
    out = 0

    lenghtZ = (size - zStart)
    maxDay = (size - zStart) + (size - xStart)
    _max = int(day if day <= lenghtZ else lenghtZ)
    _min = int(0 if day <= maxDay else day - maxDay)

    for i in range(zStart+_min, zStart + _max):
        out += suit3d(zStart, yStart, xStart, i, day, size)

    _min = _min if _min <= zStart else zStart
    _max = int(day if day <= zStart else zStart)
    for i in range(zStart - _max, zStart - _min):
        out += suit3d(zStart, yStart, xStart, i, day, size)
    return out


def getProgression(x, y, z, size):
    """
    Return how the viruses progress depending on the first infected position
    """
    day = 1
    addedPerDay = [compute3d(x, y, z, day, size)]
    while True:
        day += 1
        tmp = compute3d(x, y, z, day, size)
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
    sequences = []
    translations = []
    for [pX, pY, pZ] in getTranslation(size):
        # Empty the function cache
        resetSliceMem()
        addedPerDay = getProgression(pX, pY, pZ, size)
        sequences.append(addedPerDay)
        translations.append([pX, pY, pZ])
    for i in range(len(sequences)):
        fancyPrint(sequences[i], translations[i], size)
    print("Total groups : "+str(len(sequences)))


if __name__ == "__main__":
    main()
