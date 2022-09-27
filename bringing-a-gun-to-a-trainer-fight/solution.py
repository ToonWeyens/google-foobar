from math import ceil, sqrt
import numpy as np

# debug = True
debug = False

if debug:
    nZeroDist = 0

def solution(dims, yourPos, trainPos, dist):
    # debug = False
    # create virtual room mirrored both horizontally and vertically
    # this could carry on unlimited in all directions but is limited by the maximum dist

    # extend your and trainer position virtually
    # do this multiple times until there are no more new virtual points that have short enough distances
    dimsH = [0,dims[0]]
    dimsV = [0,dims[1]]

    # you
    yourData = virtualize("Y", yourPos, yourPos, dimsH, dimsV, dist)
    if debug:
        print "all virtual yourselves within reach:"
        printObjData(yourData)

    # trainers
    trainData = virtualize("T", yourPos, trainPos, dimsH, dimsV, dist)
    if debug:
        print "all virtual trainers within reach:"
        printObjData(trainData)

    # shortest distance for angles
    dirs = catalogDirsForShortestDist(yourData, trainData)
    nValidDirs = 0
    for dir, label in dirs.items():
        if label == "T":
            nValidDirs += 1
            if debug:
                print label, dir
        
    return nValidDirs

def virtualize(label, origPos, objPos, dimsH, dimsV, maxDist):
    # Create virtual representations of the object, by repeating indefinitely in
    # horizontal and vertical directions using
    #   x = x0 + k (H1-H0), k = -inf..inf
    #   y = y0 + l (V1-V0), l = -inf..inf
    #   x = x0 - 2(x0-H0) + k (H1-H0), k = -inf..inf
    #   y = y0 - 2(y0-V0) + l (V1-V0), l = -inf..inf
    # This is limited only by the max range
    # Optionally, you can add pre-existing objData as objDataExtr for it to be incluced in the append if valid
    # debug = False

    global nZeroDist
    nZeroDist = 0

    if debug:
        print "let's find the virtual points for", objPos

    dH = dimsH[1]-dimsH[0]
    dV = dimsV[1]-dimsV[0]
    dObjPos = [objPos[0]-dimsH[0], objPos[1]-dimsH[0]]

    if debug:
        print "dH =", dH, ", dV =", dV
        print "dObjPos =", dObjPos

    # create list that we can append to
    objData = []
    objData.append([])
    objData.append([])
    objData.append([])
    objData.append([])

    # see how many double boxes are necessary
    maxDist2 = (maxDist+2*np.sqrt(dH**2+dV**2))**2 # make the box a bit bigger to capture also virtual positions
    mMax = calcHRange(origPos, maxDist2, [0], dH, dV)
    if debug:
        print "horizontal range:"
        for m in mMax:
            print "0/0:", -m, "...", m, " x dH"
    mRange = range(-mMax[0],mMax[0]+1)
    nMax4Range = calcVRange(origPos, maxDist2, mRange, dH, dV)
    if debug:
        print "vertical range:"
        for m, nMax in zip(mRange, nMax4Range):
            print m, "/", mMax[0], ":", -nMax, "...", nMax, " x dV"

    mRange = range(-mMax[0],mMax[0]+1)
    for m, nMax in zip(mRange, nMax4Range):
        nRange = range(-nMax, nMax+1)
        for n in nRange:
            objPosExtBase = (objPos[0]+2*m*dH, objPos[1]+2*n*dV)
            for idx in range(0,2):
                for idy in range(0,2):
                    # try the original and all possible reflections
                    objPosExt = (objPosExtBase[0] - 2*idx*dObjPos[0],
                        objPosExtBase[1] - 2*idy*dObjPos[1])
                    distLoc = euclidDist(objPosExt, origPos)
                    if distLoc <= maxDist:
                        objData[0].append(objPosExt)
                        objData[1].append(distLoc)
                        objData[2].append(calcValidDir(objPosExt, origPos))
                        objData[3].append(label)

    return objData

def catalogDirsForShortestDist(yourData, trainData):
    # combine yourselves and trainers
    data = []
    for idx in range(4):
        data.append([])
        data[idx] += yourData[idx]+trainData[idx]

    # sort by distance so that we can avoid to compare all elements for distance
    data = sortByDist(data)

    if debug:
        print "consolidated and sorted:"
        printObjData(data)

    dirs = {}
    for dir, label in zip(data[2], data[3]):
        if dir not in dirs:
            dirs[dir] = label

    return dirs

def sortByDist(objData):
    idxSrt = np.argsort(objData[1])
    objData = [list(np.array(x)[idxSrt]) for x in objData]
    return objData

def calcHRange(origPos, dist2, n, dH, dV):
    # Note: n is an array
    denom = np.array(n)*2*dV
    denom += origPos[1] # y
    mAbs = np.sqrt(dist2-np.power(denom, 2))
    mAbs = (mAbs - origPos[0])/(2*dH)

    mAbsInt = np.floor(mAbs).astype(int)
    
    return mAbsInt

def calcVRange(origPos, dist2, m, dH, dV):
    # Note: m is an array
    denom = np.array(m)*2*dH
    denom += origPos[0] # y
    nAbs = np.sqrt(dist2-np.power(denom, 2))
    nAbs = (nAbs - origPos[1])/(2*dV)

    nAbsInt = np.floor(nAbs).astype(int)

    return nAbsInt

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
            print "nZeroDist", nZeroDist
            assert nZeroDist <= 2, "You can maximum have 2 zero distances"
        return
    
    if gcd != 1:
        # if debug:
            # print "gcd[",dirLoc[0],",",dirLoc[1],"] =", gcd
        # from https://stackoverflow.com/a/8244949/3229162
        dirLoc[:] = [x / gcd for x in dirLoc]

    return tuple(dirLoc)

def printObjData(objData):
    # debug = False
    if debug:
        nIdx = len(objData[0])
        for idx in range(nIdx):
            print objData[3][idx], "-o", idx, "/", nIdx-1, ": pos",\
                objData[0][idx], ", dist", objData[1][idx], ", dir", objData[2][idx]

if __name__ == "__main__":
    print "1"
    sol =  solution([3, 2], [1, 1], [2, 1], 4)
    print "solution =", sol
    assert sol == 7

    print "2"
    sol =  solution([2, 5], [1, 2], [1, 4], 11)
    assert sol == 27

    print "3"
    sol = solution([23, 10], [6, 4], [3, 2], 23)
    assert sol == 8

    print "4"
    sol = solution([1250, 1250], [1000, 1000], [500, 400], 10000)
    assert sol == 196

    print "5"
    sol = solution([300, 275], [150, 150], [180, 100], 500)
    assert sol == 9

    print "6"
    sol = solution([3, 2], [1, 1], [2, 1], 7) 
    assert sol == 19

    print "7"
    sol = solution([2, 3], [1, 1], [1, 2], 4)
    assert sol == 7

    print "8"
    sol = solution([3, 4], [1, 2], [2, 1], 7)
    assert sol == 10

    print "9"
    sol = solution([4, 4], [2, 2], [3, 1], 6)
    assert sol == 7

    print "10"
    sol = solution([3, 4], [1, 1], [2, 2], 500)
    print "solution =", sol
    assert sol == 54239
    # assert sol == 54243

    print "11"
    sol = solution([10, 10], [4, 4], [3, 3], 5000)
    print "solution =", sol
    assert sol == 739323
