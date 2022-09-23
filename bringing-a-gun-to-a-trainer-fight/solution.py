from math import ceil


debug = True

def solution(dims, yourPos, trainPos, dist):
    # create virtual room mirrored both horizontally and vertically
    # this could carry on unlimited in all directions but is limited by the maximum dist

    # extend your and trainer position virtually
    # do this multiple times until there are no more new virtual points that have short enough distances
    dimsH = [0,dims[0]]
    dimsV = [0,dims[1]]

    # trainer
    trainPosTot, trainDistTot = virtualize(yourPos, trainPos, dimsH, dimsV, dist)
    if debug:
        print "all virtual trainers within reach:"
        for idx in range(len(trainPosTot)):
            print idx, trainPosTot[idx], trainDistTot[idx]
    
    # you
    yourPosTot, yourDistTot = virtualize(yourPos, yourPos, dimsH, dimsV, dist)
    if debug:
        print "all yourselves within reach:"
        for idx in range(len(yourPosTot)):
            print idx, yourPosTot[idx], yourDistTot[idx]

def virtualize(origPos, objPos, dimsH, dimsV, maxDist):
    # Create virtual representations of the object, by repeating indefinitely in
    # horizontal and vertical directions using
    #   x = x0 + k (H1-H0), k = -inf..inf
    #   y = y0 + l (V1-V0), l = -inf..inf
    #   x = x0 - 2(x0-H0) + k (H1-H0), k = -inf..inf
    #   y = y0 - 2(y0-V0) + l (V1-V0), l = -inf..inf
    # This is limited only by the max range
    if debug:
        print "let's find the virtual points for", objPos

    dH = dimsH[1]-dimsH[0]
    dV = dimsV[1]-dimsV[0]

    if debug:
        print "dH =", dH, ", dV =", dV

    # create list that we can append to
    objPosTot = []

    # Append with all H translated poitions
    nH = maxDist/dH/2+2 # will always contain the valid points, +2 just in case
    for idH in range(nH):
        objPosExt = [objPos[0]+2*idH*dH, objPos[1]]
        objPosTot.append(objPosExt)
        # if debug:
        #     print "add", objPosExt
        objPosExt = [objPos[0]-2*idH*dH, objPos[1]]
        objPosTot.append(objPosExt)
        # if debug:
        #     print "add", objPosExt

    # Append with all V translated positions
    nV = maxDist/dV/2+2 # will always contain the valid points, +2 just in case
    nTot = len(objPosTot)
    for idx in range(nTot):
        for idV in range(nV):
            objPosExt = [objPosTot[idx][0], objPosTot[idx][1]+2*idV*dV]
            objPosTot.append(objPosExt)
            # if debug:
                # print "add", objPosExt
            objPosExt = [objPosTot[idx][0], objPosTot[idx][1]-2*idV*dV]
            objPosTot.append(objPosExt)
            # if debug:
                # print "add", objPosExt

    # Append with translation corresponding to mirror in H
    nTot = len(objPosTot)
    for idx in range(nTot):
        objPosExt = [objPosTot[idx][0] - 2*(objPos[0]-dimsH[0]),
                    objPosTot[idx][1]]
        objPosTot.append(objPosExt)

    # Append with translation corresponding to mirror in V
    nTot = len(objPosTot)
    for idx in range(nTot):
        objPosExt = [objPosTot[idx][0],
                    objPosTot[idx][1] - 2*(objPos[1]-dimsV[0])]
        objPosTot.append(objPosExt)
    
    # only retain non-duplicates within distance
    objOut = []
    distOut = []

    for objPosLoc in objPosTot:
        distLoc = euclidDist(objPosLoc, origPos)
        if not objPosLoc in objOut and distLoc <= maxDist:
            objOut.append(objPosLoc)
            distOut.append(distLoc)
    

    sortKeysDist = sorted(range(len(distOut)), key = lambda i: distOut[i])
    objOutSort = [objOut[key] for key in sortKeysDist]

    return objOutSort, sorted(distOut)


def euclidDist(X,Y):
    import math
    # if debug:
        # print "distance between", X, "and", Y, "=", math.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    return math.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)

def virtualizeWalls(dims):
    delta = dims[1]-dims[0]
    dims[0] -= delta
    dims[1] += delta


if __name__ == "__main__":
    dims = [4,3]
    yourPos = [1,1]
    trainerPos = [3,2]
    # dist = 4
    dims = [3,2]
    yourPos = [1,1]
    trainerPos = [2,1]
    dist = 4
    print dims, yourPos, trainerPos, dist
    print(solution(dims, yourPos, trainerPos, dist))
    print ""