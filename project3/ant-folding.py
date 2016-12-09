import hpview3k
import sys
import numpy as np
import random as rnd
import math

def aco(S='hhppppphhppphppphp'):
    ants = 10 if len(S) <= 25 else 15
    alpha = 1
    beta = 2
    rho = 0.6
    theta = 0.05
    steps = 100
    n = len(S)
    pheromones = [(1.0, 1.0, 1.0) for _ in range(n)]
    # m_pheromones = [None for _ in range(n)]
    heuristics = [(1.0, 1.0, 1.0)]
    # m_heuristics = [None for _ in range(n)]
    d = {0: 'S', 1: 'L', 2: 'R'}
    lattice = [[None for _ in range(n*2)] for _ in range(n*2)]
    

    # TODO: initpos = rnd.randint(0, n - 2)
    initpos = 0  # all ants start at left-most position in sequence
    fst = S[initpos]
    snd = S[initpos + 1]

    # TODO: arbitrary positions instead of in the middle?
    lattice[n][n] = fst
    lattice[n][n+1] = snd
    # print(np.array(lattice))
    # print(lattice)

    # h = []
    # for i in range(n-1):
    #     if S[i+1] == 'p':
    #         h.append((0.0, 0.0, 0.0))
        # else:


    # for ant in range(ants):
    prevpos = (n, n)
    currpos = (n, n+1)

    for i in range(initpos, n-1):
        print(i)
        print(n, n)
        print(lattice[n][n+1])
        pid = []
        for d in range(3):
            pheromone_id = pheromones[i][d]

            # heuristic_id = []
            
            # determine where we came from










            denom_sum = 0.0
            for e in range(3):
                denom_sum += (pheromones[i][e] ** alpha) * (heuristics[i][e] ** beta)
            numerator = (pheromones[i][d] ** alpha) * (heuristics[i][d] ** beta)
            prob_id = numerator / denom_sum
            pid.append(prob_id)

        print(pid)

        # update lattice with new position


        # if i > 0:
            # update pheromones?

        # pheromone update:
        # T(i,d) = (1 - rho) * T(i,d) + delta(i,d,c)
        # see article about delta, 'cause that shit's weird



def checkLeft(col,row,table):
    left = table[row][col-2]
    down = table[row+1][col-1]
    up = table[row-1][col-1]

    if left and up and down:
        raise Exception("left: dead end")
    else:
        count = 0
        if(left == "h"):
            count += 1
        if(down == "h"):
            count += 1
        if(up == "h"):
            count += 1
        return count

def checkUp(col,row,table):
    left = table[row-1][col-1]
    right = table[row-1][col+1]
    up = table[row-2][col]

    if left and up and right:
        raise Exception("up: dead end")
    else:
        count = 0
        if(left == "h"):
            count += 1
        if(right == "h"):
            count += 1
        if(up == "h"):
            count += 1
        return count

def checkRight(col,row,table):
    right = table[row][col+2]
    down = table[row+1][col+1]
    up = table[row-1][col+1]

    if right and up and down:
        raise Exception("right: dead end")
    else:
        count = 0
        if(right == "h"):
            count += 1
        if(down == "h"):
            count += 1
        if(up == "h"):
            count += 1
        return count

def checkDown(col,row,table):
    left = table[row+1][col-1]
    down = table[row+2][col]
    right = table[row+1][col+1]

    if left and right and down:
        raise Exception("down: dead end")
    else:
        count = 0
        if(left == "h"):
            count += 1
        if(down == "h"):
            count += 1
        if(right == "h"):
            count += 1
        return count


def print_folding(string, fold):

    seq = hpview3k.HPFold(string)

    if len(seq) != len(string):
        print("The sequence %s contains illegal characters." % (string))
        sys.exit(1)
        
    absfold = hpview3k.make_absfold(fold)
    relfold = hpview3k.make_relfold(fold)

    if len(absfold) != len(fold) and len(relfold) != len(fold):
        print("The folding %s contains illegal characters." % fold)
        sys.exit(1)
        
    if len(absfold) == len(seq) - 1:
        seq.SetAbsFold(absfold)
    elif len(relfold) == len(seq) - 1:
        seq.SetRelFold(relfold)
    else:
        print("The folding %s has wrong length." % (fold))
        sys.exit(1)

    seq.PrintFold()

def main():
    aco()
    

if __name__ == '__main__':
    main()
