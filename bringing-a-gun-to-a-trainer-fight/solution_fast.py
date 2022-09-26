from math import ceil, sqrt
import numpy as np

debug = True
# debug = False

if debug:
    nZeroDist = 0

def solution(dims, yourPos, trainPos, dist):
    # create virtual room mirrored both horizontally and vertically
    # this could carry on unlimited in all directions but is limited by the maximum dist

    # extend your and trainer position virtually
    # do this multiple times until there are no more new virtual points that have short enough distances
    dimsH = [0,dims[0]]
    dimsV = [0,dims[1]]

    # you
    yourData = virtualize(yourPos, yourPos, dimsH, dimsV, dist)
    if debug:
        print "all virtual yourselves within reach:"
        printObjData(yourData)

    # trainers
    trainData = virtualize(yourPos, trainPos, dimsH, dimsV, dist, objDataExtra=yourData)
    if debug:
        print "all virtual trainers within reach:"
        printObjData(trainData)
        
    return len(trainData[0])

def virtualize(origPos, objPos, dimsH, dimsV, maxDist, objDataExtra=None):
    # Create virtual representations of the object, by repeating indefinitely in
    # horizontal and vertical directions using
    #   x = x0 + k (H1-H0), k = -inf..inf
    #   y = y0 + l (V1-V0), l = -inf..inf
    #   x = x0 - 2(x0-H0) + k (H1-H0), k = -inf..inf
    #   y = y0 - 2(y0-V0) + l (V1-V0), l = -inf..inf
    # This is limited only by the max range
    # Optionally, you can add pre-existing objData as objDataExtr for it to be incluced in the append if valid
    if debug:
        print "let's find the virtual points for", objPos

    dH = dimsH[1]-dimsH[0]
    dV = dimsV[1]-dimsV[0]
    dObjPos = [objPos[0]-dimsH[0], objPos[1]-dimsH[1]]

    if debug:
        print "dH =", dH, ", dV =", dV

    # create list that we can append to
    objData = []
    objData.append([])
    objData.append([])
    objData.append([])

    # see how many double boxes are necessary
    nH = int(ceil((origPos[0] + maxDist) / (2*dH)))+1
    nV = int(ceil((origPos[1] + maxDist) / (2*dV)))+1
    for idH in range(-nH,nH+1):
        for idV in range(-nV,nV+1):
            objPosExt = (objPos[0]+2*idH*dH, objPos[1]+2*idV*dV)
            appendIfValid(objPosExt, origPos, maxDist, objData, objDataExtra)

    # print ">>> Resulting translations"
    # printObjData(objData)

    # Append with translation corresponding to mirror in H
    nTot = len(objData[0])
    for idx in range(nTot):
        objPosExt = (objData[0][idx][0] - 2*dObjPos[0], objData[0][idx][1])
        appendIfValid(objPosExt, origPos, maxDist, objData, objDataExtra)

    # print ">>> Resulting H mirror translatsions"
    # printObjData(objData)

    # Append with translation corresponding to mirror in V
    nTot = len(objData[0])
    for idx in range(nTot):
        objPosExt = (objData[0][idx][0], objData[0][idx][1] - 2*dObjPos[1])
        appendIfValid(objPosExt, origPos, maxDist, objData, objDataExtra)

    # print ">>> Resulting V mirror translatsions"
    # printObjData(objData)

    return objData

def appendIfValid(objPos, origPos, maxDist, objData, objDataExtra=None):
    # Check if valid:
    #   - objPos is close enough to origPos
    #   - the direction of objPos (wrt. origPos) is not already present
    # Note: Does not return value but edits objData
    #   - (x,y): position as tuple
    #   - d: distance as float
    #   - (d1,d2): direction as tuple, with gcd=1
    # Note: You can pass an extra ObjData to compare to
    # This is useful if you want to, for example, compare addiitonally to existing
    # positions of virtual selves
    debug = False

    distLoc = euclidDist(objPos, origPos)
    if debug:
        print "trying objPos", objPos, "with distance", distLoc
    if distLoc <= maxDist:
        if debug:
            print "  within distance <=", maxDist
        if not objPos in objData[0]:
            if debug:
                print "    not already existing"
            dirLoc = calcValidDir(objPos, origPos)
            if debug:
                print "      trying direction", dirLoc
            if not dirLoc is None:
                if debug:
                    print "        nonzero"
                if not dirLoc in objData[2]:
                    if debug:
                        print "          not already existing"
                    objData[0].append(objPos)
                    objData[1].append(distLoc)
                    objData[2].append(dirLoc)


def euclidDist(X,Y):
    # if debug:
        # print "distance between", X, "and", Y, "=", sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    return sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)

def calcValidDir(objPos, origPos):
    # Calculate direction between objPos and origPos
    # Express these as 2D vectors making sure the GCD is 1
    # Also only maintain distinct values, no duplciates
    import fractions
    import numpy as np
    global nZeroDist

    dirLoc = [objPos[0]-origPos[0], objPos[1]-origPos[1]]
    # if debug:
        # print "checking if we can add", dirLoc, "with distance", distLoc, "to direction list"

    # reduce to having gcd = 1
    if abs(dirLoc[0]) > 0 and abs(dirLoc[1]) > 0:
        gcd = abs(np.gcd(dirLoc[0],dirLoc[1]))
    elif dirLoc[0] == 0 and dirLoc[1] != 0:
        gcd = abs(dirLoc[1])
    elif dirLoc[0] != 0 and dirLoc[1] == 0:
        gcd = abs(dirLoc[0])
    else:
        # dirLoc is [0,0]
        if debug:
            nZeroDist += 1
            assert nZeroDist <= 2, "You can maximum have 2 zero distances"
        return
    
    if gcd != 1:
        # if debug:
            # print "gcd[",dirLoc[0],",",dirLoc[1],"] =", gcd
        # from https://stackoverflow.com/a/8244949/3229162
        dirLoc[:] = [x / gcd for x in dirLoc]

    return tuple(dirLoc)

def printObjData(objData):
    nIdx = len(objData[0])
    for idx in range(nIdx):
        print idx, "/", nIdx-1, ": pos", objData[0][idx], ", dist", objData[1][idx], ", dir", objData[2][idx]

if __name__ == "__main__":
    print "1"
    sol =  solution([3, 2], [1, 1], [2, 1], 4)
    print "solution =", sol
    assert sol == 7

    print "2"
    sol =  solution([2, 5], [1, 2], [1, 4], 11)
    assert solution(sol) == 27

    print "3"
    sol = solution([23, 10], [6, 4], [3, 2], 23)
    assert solution(sol) == 8

    print "4"
    sol = solution([1250, 1250], [1000, 1000], [500, 400], 10000)
    assert solution(sol) == 196

    print "5"
    assert solution([300, 275], [150, 150], [180, 100], 500) == 9
    assert solution(sol) == 9
    print "6"
    assert solution([3, 2], [1, 1], [2, 1], 7) == 19
    print "7"
    assert solution([2, 3], [1, 1], [1, 2], 4) == 7
    print "8"
    assert solution([3, 4], [1, 2], [2, 1], 7) == 10
    print "9"
    assert solution([4, 4], [2, 2], [3, 1], 6) == 7

    print "10"
    sol = solution([3, 4], [1, 1], [2, 2], 500)
    print "solution =", sol
    assert sol == 54243
    print "11"
    assert solution([10, 10], [4, 4], [3, 3], 5000) == 739323
    print "12"
