debug = True

def solution(dims, yourPos, trainPos, dist):
    # create virtual room mirrored both horizontally and vertically
    # this could carry on unlimited in all directions but is limited by the maximum dist

    # extend your and trainer position virtually
    # do this multiple times until there are no more new virtual points that have short enough distances
    dimsH = [0,dims[0]]
    dimsV = [0,dims[1]]

    # trainer
    trainPosTot = virtualize(yourPos, trainPos, dimsH, dimsV, dist)
    if debug:
        print "all virtual trainers within reach:"
        print trainPosTot
    
    # you
    yourPosTot = virtualize(yourPos, yourPos, dimsH, dimsV, dist)
    if debug:
        print "all yourselves within reach:"
        print yourPosTot

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

    kdx = 0
    while True: # horizontal loop
        ldx = 0
        nAddH = 0

        if debug:
            print "iterating horizontally with kdx=", kdx
        
        while True: # vertical loop
            nAddV = 0
            
            if debug:
                print "iterating vertically with ldx=", ldx

            # try adding point
            objPosVirt = [
                objPos[0]+kdx*dH,
                objPos[1]+ldx*dV]
            if debug:
                print "potential virtual point", objPosVirt
            if euclidDist(origPos, objPosVirt) <= maxDist:
                nAddV += 1
                objPosTot.append(objPosVirt)
                if debug:
                    print "> Appended"
            
            # try adding mirror point
            objPosVirt = [
                # objPos[0]-2*(objPos[0]-dimsH[0])+kdx*dH,
                # objPos[1]-2*(objPos[1]-dimsV[0])+ldx*dV]
                2*dimsH[0]-objPos[0]+kdx*dH,
                2*dimsV[0]-objPos[1]+ldx*dV]
            if debug:
                print "potential virtual mirror point", objPosVirt
            if euclidDist(origPos, objPosVirt) <= maxDist:
                nAddV += 1
                objPosTot.append(objPosVirt)
                if debug:
                    print "> Appended"
            
            if debug:
                print "nAddV", nAddV
            # programPause = raw_input("Press the <ENTER> key to continue...")

            # count up all the vertical increases to find total for this horizontal step
            nAddH += nAddV
            # if this round produced nothing new, break as we'll only go farther away
            if nAddV == 0:
                if debug:
                    print "break V"
                break

            ldx += 1

        # if this round produced nothing new, break as we'll only go farther away
        if nAddH == 0:
            if debug:
                print "break H"
            break

        kdx += 1

    return objPosTot


def euclidDist(X,Y):
    import math
    if debug:
        print "distance between", X, "and", Y, "=", math.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)
    return math.sqrt((X[0]-Y[0])**2+(X[1]-Y[1])**2)

def virtualizeWalls(dims):
    delta = dims[1]-dims[0]
    dims[0] -= delta
    dims[1] += delta


if __name__ == "__main__":
    dims = [4,3]
    yourPos = [1,1]
    trainerPos = [3,2]
    dist = 6
    print dims, yourPos, trainerPos, dist
    print(solution(dims, yourPos, trainerPos, dist))
    print ""