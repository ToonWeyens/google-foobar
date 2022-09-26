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
    yourData = virtualize(yourPos, trainPos, dimsH, dimsV, dist, objDataExtra=yourData)
    if debug:
        print "all virtual trainers within reach:"
        printObjData(trainData)
    
    
    # Find all feasible directions:
    #   - If direction already exists and is shorter, don't add this one
    #   - If you kill any version of yourself in a shorter distance, don't add this one
    # trainDir, trainDist = calcValidDir(trainPosTot, yourPos, trainDistTot)
    # if debug:
    #     print "Direction of all virtual trainers:"
    #     for idx in range(len(trainDir)):
    #         print idx, trainDir[idx], trainDist[idx]
        

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

    if debug:
        print "dH =", dH, ", dV =", dV

    # create list that we can append to
    objData = []
    objData.append([])
    objData.append([])
    objData.append([])
    objData[0].append(tuple(objPos))
    objData[1].append(euclidDist(objPos, origPos))
    objData[2].append(calcValidDir(objPos, origPos))

    # Append with all H translated poitions
    nH = int(ceil((origPos[0] + maxDist) / dH))+1
    if debug:
        print "horizontal copies of box:", nH
    for idH in range(1,nH): # origin already potentially included
        print ">>!>!>idH", idH
        for pmOne in range(-1,2,2):
            objPosExt = (objPos[0]+pmOne*2*idH*dH, objPos[1])
            print ">>!>!>objPosExt", objPosExt
            appendIfValid(objPosExt, origPos, maxDist, objData, objDataExtra)
    if debug:
        print ">>> after H translations"
        printObjData(objData)

    # Append with all V translated positions
    nV = int(ceil((origPos[1] + maxDist) / dV))+1
    if debug:
        print "vertical copies of box:", nV
    nTot = len(objData)
    for idx in range(nTot):
        for idV in range(nV):
            for pmOne in range(-1,2,2):
                objPosExt = (objPos[0], objPos[1]+2*idV*dV)
                appendIfValid(objPosExt, origPos, maxDist, objData, objDataExtra)
    if debug:
        print ">>> after V translations"
        printObjData(objData)

    # Append with translation corresponding to mirror in H
    nTot = len(objData)
    if debug:
        print "H mirror translations:", nTot
    for idx in range(nTot):
        if debug:
            print idx, "/", nTot-1
            printObjData(objData)
        objPosExt = (objData[0][idx][0] - 2*(objPos[0]-dimsH[0]),
                    objData[0][idx][1])
        appendIfValid(objPosExt, origPos, maxDist, objData, objDataExtra)

    # Append with translation corresponding to mirror in V
    nTot = len(objData)
    if debug:
        print "V mirror translations:", nTot
    for idx in range(nTot):
        objPosExt = (objData[0][idx][0],
                    objData[0][idx][1] - 2*(objPos[1]-dimsV[0]))
        appendIfValid(objPosExt, origPos, maxDist, objData, objDataExtra)

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
    distLoc = euclidDist(objPos, origPos)
    if debug:
        print "trying distLoc", distLoc
    if distLoc <= maxDist:
        if debug:
            print "within distance <=", maxDist
        if not objPos in objData[0]:
            if debug:
                print "not already existing"
            dirLoc = calcValidDir(objPos, origPos)
            if debug:
                print "trying direction", dirLoc
            if not dirLoc is None:
                if debug:
                    print "nonzero"
                if not dirLoc in objData[1]:
                    if debug:
                        print "not already existing"
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
    assert solution([3, 4], [1, 2], [2, 1], 7) == 10