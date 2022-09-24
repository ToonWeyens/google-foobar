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
    
    # Find all feasible directions:
    #   - If direction already exists and is shorter, don't add this one
    #   - If you kill any version of yourself in a shorter distance, don't add this one
    trainDir, trainDist = calcValidDir(trainPosTot, yourPos, trainDistTot)
    if debug:
        print "Direction of all virtual trainers:"
        for idx in range(len(trainDir)):
            print idx, trainDir[idx], trainDist[idx]
        
    yourDir, yourDist = calcValidDir(yourPosTot[1:], yourPos, yourDistTot[1:])
    if debug:
        print "Direction of all virtual yourselves:"
        for idx in range(len(yourDir)):
            print idx, yourDir[idx], yourDist[idx]

def calcValidDir(objPos, origPos, dist):
    # Calculate direction between objPos and origPos
    # Express these as 2D vectors making sure the GCD is 1
    # Also only maintain distinct values, no duplciates
    import fractions
    assert len(objPos) == len(dist), "lengths of positions and distance different"

    objDir = []
    indToRemove = []

    idx = 0
    for idx in range(len(objPos)):
        objPosLoc = objPos[idx]
        distLoc = dist[idx]

        dirLoc = [objPosLoc[0]-origPos[0], objPosLoc[1]-origPos[1]]
        if debug:
            print "checking if we can add", dirLoc, "with distance", distLoc, "to direction list"

        # reduce to having gcd = 1
        if abs(dirLoc[0]) > 0 and abs(dirLoc[1]) > 0:
            gcd = abs(fractions.gcd(dirLoc[0],dirLoc[1]))
        elif dirLoc[0] == 0 and dirLoc[1] != 0:
            gcd = abs(dirLoc[1])
        elif dirLoc[0] != 0 and dirLoc[1] == 0:
            gcd = abs(dirLoc[0])
        else:
            print dirLoc
            raise ValueError('Direction cannot be [0,0]')
        
        if gcd != 1:
            # if debug:
                # print "gcd[",dirLoc[0],",",dirLoc[1],"] =", gcd
            # from https://stackoverflow.com/a/8244949/3229162
            dirLoc[:] = [x / gcd for x in dirLoc]
        
        # add if not yet in list
        if not dirLoc in objDir:
            if  debug:
                print "adding", dirLoc
            objDir.append(dirLoc)
        else:
            print "deleting element", idx, "from dist"
            indToRemove.append(idx)
        
    if debug:
        print "deleteing elements from dist", indToRemove
    for idx in reversed(indToRemove):
        del dist[idx]
    
    if debug:
        print "from", len(objPos), ", added", len(objDir), "directions"

    assert len(objDir) == len(dist), "lengths of direction and distance different"

    return objDir, dist

def virtualize(oos, objPos, dimsH, dimsV, maxDist):
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
        distLoc = euclidDist(objPosLoc, yourPos)
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

def isParallel(X,Y):
    if Y[0]//X[0] == Y[1]//X[1] and \
        X[0]//Y[0] == X[1]//Y[1] and \
        Y[0]%X[0] == 0 and \
        Y[1]%X[1] == 0:
        return True

if __name__ == "__main__":
    dims = [4,3]
    yourPos = [1,1]
    trainerPos = [3,2]
    dist = 8
    # dims = [3,2]
    # yourPos = [1,1]
    # trainerPos = [2,1]
    # dist = 4
    print dims, yourPos, trainerPos, dist
    print(solution(dims, yourPos, trainerPos, dist))
    print ""