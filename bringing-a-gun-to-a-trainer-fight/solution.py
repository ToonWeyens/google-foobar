from math import ceil, sqrt


debug = True
# debug = False

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
    
    # find all valid trainer directions, i.e. thoe that are not blocked by yourself
    nValidDir = 0
    for idx in range(len(trainDir)):
        trainDirLoc = trainDir[idx]
        trainDistLoc = trainDist[idx]
        if debug:
            print idx, "What would happen if we shot", trainDirLoc, "for distance of", trainDistLoc
        if trainDirLoc in yourDir:
            blockIdx = yourDir.index(trainDirLoc)
            yourDirBlock = yourDir[blockIdx]
            yourDistBlock = yourDist[blockIdx]
            if debug:
                print "You have a reflection at distance", yourDistBlock
            if yourDistBlock <= trainDistLoc:
                if debug:
                    print "!! therefore you would shoot yourself"
                continue
            else:
                if debug:
                    print "but it's far enough"
        
        # if you got here, you've not shot yourself
        nValidDir += 1

    if debug:
        print "number of valid directions:", nValidDir

    return nValidDir

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
        # if debug:
            # print "checking if we can add", dirLoc, "with distance", distLoc, "to direction list"

        # reduce to having gcd = 1
        if abs(dirLoc[0]) > 0 and abs(dirLoc[1]) > 0:
            gcd = abs(fractions.gcd(dirLoc[0],dirLoc[1]))
        elif dirLoc[0] == 0 and dirLoc[1] != 0:
            gcd = abs(dirLoc[1])
        elif dirLoc[0] != 0 and dirLoc[1] == 0:
            gcd = abs(dirLoc[0])
        else:
            if debug:
                print dirLoc
            raise ValueError('Direction cannot be [0,0]')
        
        if gcd != 1:
            # if debug:
                # print "gcd[",dirLoc[0],",",dirLoc[1],"] =", gcd
            # from https://stackoverflow.com/a/8244949/3229162
            dirLoc[:] = [x / gcd for x in dirLoc]
        
        # add if not yet in list
        if not dirLoc in objDir:
            # if  debug:
                # print "adding", dirLoc
            objDir.append(dirLoc)
        else:
            # if debug:
                # print "deleting element", idx, "from dist"
            indToRemove.append(idx)
        
    # if debug:
        # print "deleting elements from dist", indToRemove
    for idx in reversed(indToRemove):
        del dist[idx]
    
    if debug:
        print "from", len(objPos), ", added", len(objDir), "directions"

    assert len(objDir) == len(dist), "lengths of direction and distance different"

    return objDir, dist

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
    nH = int(ceil((origPos[0] + maxDist) / dH))+1
    if debug:
        print "horizontal copies of box:", nH
    for idH in range(nH):
        if debug:
            print "idH=", idH,"/",nH-1
        objPosExt = [objPos[0]+2*idH*dH, objPos[1]]
        objPosTot.append(objPosExt)
        # if debug:
        #     print "add", objPosExt
        objPosExt = [objPos[0]-2*idH*dH, objPos[1]]
        objPosTot.append(objPosExt)
        # if debug:
        #     print "add", objPosExt

    # Append with all V translated positions
    nV = int(ceil((origPos[1] + maxDist) / dV))+1
    if debug:
        print "vertical copies of box:", nV
    nTot = len(objPosTot)
    for idx in range(nTot):
        for idV in range(nV):
            if debug:
                print "idV=", idV,"/",nV-1
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
        if debug:
            print "idx=", idx,"/",nTot-1
        objPosExt = [objPosTot[idx][0] - 2*(objPos[0]-dimsH[0]),
                    objPosTot[idx][1]]
        objPosTot.append(objPosExt)

    # Append with translation corresponding to mirror in V
    nTot = len(objPosTot)
    for idx in range(nTot):
        if debug:
            print "idx=", idx,"/",nTot-1
        objPosExt = [objPosTot[idx][0],
                    objPosTot[idx][1] - 2*(objPos[1]-dimsV[0])]
        objPosTot.append(objPosExt)
        !!!!!!!!!!! BETTER TO ONLY APPEND IF NOT YET IN THERE !!!!!!!!1
    
    # only retain non-duplicates within distance
    objOut = []
    distOut = []

    for idx in range(len(objPosTot)):
        if debug:
            print "idx=", idx,"/",len(objPosTot)-1
        objPosLoc = objPosTot[idx]
        distLoc = euclidDist(objPosLoc, origPos)
        if not objPosLoc in objOut and distLoc <= maxDist:
            objOut.append(objPosLoc)
            distOut.append(distLoc)
    

    sortKeysDist = sorted(range(len(distOut)), key = lambda i: distOut[i])
    objOutSort = [objOut[key] for key in sortKeysDist]

    return objOutSort, sorted(distOut)


def euclidDist(X,Y):
    # if debug:
        # print "distance between", X, "and", Y, "=", sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    return sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)

if __name__ == "__main__":
    print "1"
    sol =  solution([3, 2], [1, 1], [2, 1], 4)
    print "solution =", sol
    assert sol == 7

    print "2"
    assert solution([2, 5], [1, 2], [1, 4], 11) == 27
    print "3"
    assert solution([23, 10], [6, 4], [3, 2], 23) == 8
    print "4"
    assert solution([1250, 1250], [1000, 1000], [500, 400], 10000) == 196
    print "5"
    assert solution([300, 275], [150, 150], [180, 100], 500) == 9
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
