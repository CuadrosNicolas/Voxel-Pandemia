
import math

def nbDay(x,size):
    return size-x

def suit(x,day,size):
    nDay = nbDay(x,size)
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
    out = 0
    for i in range(0,size):
        out += suit2d(ySource, xStart, i, day-abs(zSource-z), size)
    return out

def compute3d(xStart, yStart, zStart, day, size):
    out = 0
    for i in range(0,size):
        out += suit3d(zStart, yStart,xStart, i, day, size)
    return out

def getProgression(x,y,z, size):
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

def main():

    #print(getProgression(0,0,0,5))

    #Size of the initial cube
    size = 3
    pZ = 0
    pZmax = math.ceil(size/2)    
    while(pZ<math.ceil(size/2)):

        pXMax = math.ceil(size/2)
        pX = 0

        while(pX<math.ceil(size/2)):
            pY = math.ceil(size/2) - pXMax

            while(pY < math.ceil(size/2)):

                addedPerDay = [compute3d(pX, pY, pZ, 1, size)]
                day = 2

                while True:
                    tmp = compute3d(pX, pY, pZ, day, size)
                    if(tmp>0):
                        day +=1
                        addedPerDay.append(tmp)
                    else:
                        break

                print("Total infection : ",sum(addedPerDay), " in ",day-1, "days")
                print("Translation : ",pX, " ",pY, " ",pZ)
                print(addedPerDay)

                pY+=1
            pX +=1
            pXMax -=1
        pZ+=1
        pZmax -=1
    out = []
  

if __name__ == "__main__": 
    main() 