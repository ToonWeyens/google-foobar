debug = False

def solution(M,F):
    n = 0
    M = int(M)
    F = int(F)

    while True:
        # make sure M >= F
        if F > M:
            if debug:
                print 'swapping'
            M, F = F, M

        if debug:
            print 'M=', M, 'F=', F

        if F == 0:
            return "impossible"
        elif F == 1:
            n += M-F
            M = 1
            return str(n)
        elif F == 2 and M%2 == 0:
            # This implies M is even, and since M >= F with F = 2, M = 2, 4, ...
            return 'impossible'
        elif F == 2 and M%2 != 0:
            # This implies M is odd, and since M >= F with F = 2, M >= 3, 5, ...
            n += M/F
            n += 1 # to reduce F in next step
            return str(n)
        else:
            # count how many times F divides M
            # Note: In Python 2, this rounds down automatically
            nDiv = M/F
            M -= F*nDiv
            n += nDiv



if __name__ == "__main__":
    x = [2,1]
    print(x)
    print(solution(*x))
    print('')

    x = [4,7]
    print(x)
    print(solution(*x))
    print('')

    x = [5,5]
    print(x)
    print(solution(*x))
    print('')

    x = [6,6]
    print(x)
    print(solution(*x))
    print('')