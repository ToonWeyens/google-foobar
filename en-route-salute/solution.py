debug = False

# 1. identify each left and each right going person
# 2. for each person identify the number of people still to meet
# 3. count thesen numbers up
def solution(x):
    lp = '<'
    rp = '>'
    hw = '-'

    # parse the string
    lpPos = []
    rpPos = []
    for idx in range(len(x)):
        e = x[idx]
        if e == lp:
            lpPos.append(idx)
        elif e == rp:
            rpPos.append(idx)
        elif e == hw:
            pass
        else:
            return False

    if debug:
        print('position of left-going people', lpPos)
        print('position of right-going people', rpPos)

    # find out how many right-going people the left-goers find and vice versa
    lpNC = [] # n. collisions each left goer encounters
    rpNC = [] 
    for lp in lpPos:
        lpNC.append(0)
        for rp in rpPos:
            if rp < lp:
                lpNC[-1] += 1
    for rp in rpPos:
        rpNC.append(0)
        for lp in lpPos:
            if lp > rp:
                rpNC[-1] += 1
    if debug:
        for idx in range(len(lpNC)):
            print('    collisions for left-goer', lpPos[idx], ":", lpNC[idx])
        for idx in range(len(rpNC)):
            print('    collisions for left-goer', rpPos[idx], ":", rpNC[idx])

    # sum it all up
    return sum(rpNC)+sum(lpNC)

if __name__ == "__main__":
    x = "<<>><"
    print(x)
    print(solution(x))
    print('')

    x = ">----<"
    print(x)
    print(solution(x))
    print('')