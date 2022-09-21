debug = True

def solution(dims, yourPos, trainPos, dist):
    # create virtual room mirrored both horizontally and vertically
    # this means that the trainer position leads to additional 8, for
    # a total of 9
    trainPos = [trainPos]*1
    yourPos = [yourPos]*1

    # extend your and trainer position virtually
    # do this multiple times until there are no more new virtual points that have short enough distances

    # trainer
    dimsH = [0,dims[0]]
    dimsV = [0,dims[1]]
    while True:
        nPosBefore = len(trainPos)
        virtualize_all4(dimsH, dimsV, trainPos, dist, yourPos[0])
        nPosAfter = len(trainPos)
        if nPosAfter == nPosBefore:
            break
        else:
            # put walls further
            virtualizeWalls(dimsH)
            virtualizeWalls(dimsV)
    if debug:
        print "virtual realm for trainers has been extended to width", dimsH, "height", dimsV
        print "all virtual trainers within reach:"
        print trainPos

    # you
    dimsH = [0,dims[0]]
    dimsV = [0,dims[1]]
    while True:
        nPosBefore = len(yourPos)
        virtualize_all4(dimsH, dimsV, yourPos, dist, yourPos[0])
        nPosAfter = len(yourPos)
        if nPosAfter == nPosBefore:
            break
        else:
            # put walls further
            virtualizeWalls(dimsH)
            virtualizeWalls(dimsV)
    if debug:
        print "virtual realm for yourself has been extended to width", dimsH, "height", dimsV
        print "all virtual yourselves within reach:"
        print yourPos

# calculate all 4 virtualizations for the box
# See inputs to virtualize for explanations
def virtualize_all4(dimsH, dimsV, objPos, dist, yourPos):
    # miror horizontally
    virtualize(dimsH[0], 'H', objPos, dist, yourPos)
    virtualize(dimsH[1], 'H', objPos, dist, yourPos)

    # miror vertically
    virtualize(dimsV[0], 'V', objPos, dist, yourPos)
    virtualize(dimsV[1], 'V', objPos, dist, yourPos)
        
# Create the virtual alternate of reflections 
# Input:
#   - wallPos: position of wall
#   - dim: 'H' if wall is is vertical (!), so wallPos refers to the horizontal direction, and vice versa for 'V'
#   - objPos: (array of) object positions to be virtualized
#   - maxDist: whether there is a maximum distance from origin for positions to be added
#   - origin: origin from which to calculate maximum distance
# Note: there is no output, but original wallPos will have been extended by mirroring with respect to wall
def virtualize(wallPos, dim, objPos, maxDist, origin):
    debug = False

    nObjPos = len(objPos)

    if debug:
        print "object positions: ", objPos
        print "to be reflected wrt wall at", dim, "=", wallPos
    for tp in objPos[0:nObjPos]: # need to limit as object increases in size
        tpExt = mirror(wallPos, dim, tp)
        dist = euclidDist(tpExt, origin)
        if debug:
            print "for", tp, ": distance", dist, ", max:", maxDist
        if dist <= maxDist:
            if debug:
                print "-> extend to", tpExt
            objPos.append(tpExt)
    if debug:
        print "extended object positions", objPos
    return

def mirror(wallPos, dim, objPos):
    debug = False

    import copy

    # if debug:
    #     print "mirror", objPos, "along wall with", dim, "=", wallPos
    reflPos = copy.copy(objPos)
    if dim == 'H':
        reflPos[0] += (wallPos-objPos[0])*2
    elif dim == 'V':
        reflPos[1] += (wallPos-objPos[1])*2
    else:
        reflPos = None
    if debug:
        print 'reflecting object', objPos, dim, 'over', wallPos, 'results in', reflPos
    return reflPos

def euclidDist(X,Y):
    import math
    return math.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)

def virtualizeWalls(dims):
    delta = dims[1]-dims[0]
    dims[0] -= delta
    dims[1] += delta


if __name__ == "__main__":
    dims = [4,3]
    yourPos = [2,1]
    trainerPos = [2,1]
    dist = 15
    print dims, yourPos, trainerPos, dist
    print(solution(dims, yourPos, trainerPos, dist))
    print ""
