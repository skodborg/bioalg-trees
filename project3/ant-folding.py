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
    # initialize pheromones to 1.0 for all i,d as they have no effect on the decision
    # initially (no previous ants have walked, no pheromones has been left, nothing
    # exists to follow yet) - update as we decide moves
    pheromones = [(1.0, 1.0, 1.0) for _ in range(n)]
    # m_pheromones = [None for _ in range(n)]
    # heuristics format: (S)traight, (L)eft, (R)ight
    heuristics = [(1.0, 1.0, 1.0)]
    # m_heuristics = [None for _ in range(n)]
    d = {0: 'S', 1: 'L', 2: 'R'}
    lattice = [[None for _ in range(n*3)] for _ in range(n*3)]
    

    # TODO: initpos = rnd.randint(0, n - 2)
    initpos = 0  # all ants start at left-most position in sequence
    fst = S[initpos]
    snd = S[initpos + 1]

    # TODO: arbitrary positions instead of in the middle?
    lattice[n][n] = fst
    lattice[n][n+1] = snd
    
    # for ant in range(ants):
    prevpos = (n, n)
    currpos = (n, n+1)

    print('starting pos: %i,%i' % (n, n))
    print('first direction is relative to nothing, i.e. trivial, going to %i,%i' % (n, n+1))

    for i in range(initpos+1, n-1):
        # print(i)
        pid = []

        # heuristics format: [S, L, R]-triple
        #                    (S)traight, (L)eft, (R)ight
        heuristics_id = []

        current_direction = None
        if prevpos[0] > currpos[0]:
            current_direction = 'north'
        if prevpos[0] < currpos[0]:
            current_direction = 'south'
        if prevpos[1] > currpos[1]:
            current_direction = 'west'
        if prevpos[1] < currpos[1]:
            current_direction = 'east'


        for d in range(3):
            if d == 0:  # Straight
                straight = None
                if current_direction == 'north':
                    straight = checkNorth
                elif current_direction == 'south':
                    straight = checkSouth
                elif current_direction == 'east':
                    straight = checkEast
                else: # current_direction == 'west'
                    straight = checkWest
                try:
                    h_id = straight(currpos[0], currpos[1], lattice)
                    heuristics_id.append(h_id)
                except Exception as err:
                    print('My Exception: %s' % err)
            elif d == 1:  # Left
                left = None
                if current_direction == 'north':
                    left = checkWest
                elif current_direction == 'south':
                    left = checkEast
                elif current_direction == 'east':
                    left = checkNorth
                else: # current_direction == 'west'
                    left = checkSouth
                try:
                    h_id = left(currpos[0], currpos[1], lattice)
                    heuristics_id.append(h_id)
                except Exception as err:
                    print('My Exception: %s' % err)
            else: # d == 2,  # Right
                right = None
                if current_direction == 'north':
                    right = checkEast
                elif current_direction == 'south':
                    right = checkWest
                elif current_direction == 'east':
                    right = checkSouth
                else: # current_direction == 'west'
                    right = checkNorth
                try:
                    h_id = right(currpos[0], currpos[1], lattice)
                    heuristics_id.append(h_id)
                except Exception as err:
                    print('My Exception: %s' % err)

        heuristics_id = list(map(lambda x: x + 1, heuristics_id))
        heuristics.append(heuristics_id)

        for d in range(3):
            denom_sum = 0.0
            for e in range(3):
                denom_sum += (pheromones[i][e] ** alpha) * (heuristics[i][e] ** beta)
            numerator = (pheromones[i][d] ** alpha) * (heuristics[i][d] ** beta)
            prob_id = numerator / denom_sum
            pid.append(prob_id)

        print('direction probabilities from here:')
        print(pid)

        # pick an element from {S, L, R} with probabilities as defined by pid
        # directions: S:0, L:1, R:2
        chosen_direction = np.random.choice(3, 1, p=pid)

        if chosen_direction == 0:
            print('choice: Straight')
        elif chosen_direction == 1:
            print('choice: Left')
        else:
            print('choice: Right')

        # update lattice with new position
        newpos = [currpos[0], currpos[1]]
        if current_direction == 'north':
            if chosen_direction == 0:
                # straight; corresponds to NORTH
                newpos[0] -= 1
            elif chosen_direction == 1:
                # left; corresponds to WEST
                newpos[1] -= 1
            else: # chosen_direction == 2:
                # right; corresponds to EAST
                newpos[1] += 1
        elif current_direction == 'south':
            if chosen_direction == 0:
                # straight; corresponds to SOUTH
                newpos[0] += 1
            elif chosen_direction == 1:
                # left
                newpos[1] += 1
            else: # chosen_direction == 2:
                # right
                newpos[1] -= 1
        elif current_direction == 'east':
            if chosen_direction == 0:
                # straight
                newpos[1] += 1
            elif chosen_direction == 1:
                # left
                newpos[0] -= 1
            else: # chosen_direction == 2:
                # right
                newpos[0] += 1
        else: # current_direction == 'west':
            if chosen_direction == 0:
                # straight
                newpos[1] -= 1
            elif chosen_direction == 1:
                # left
                newpos[0] += 1
            else: # chosen_direction == 2:
                # right
                newpos[0] -= 1
        lattice[newpos[0]][newpos[1]] = S[i]

        print('facing %s that leaves us at %i,%i' % (current_direction.upper(), newpos[0], newpos[1]))
        print()

        # update cached positions to perform the move
        prevpos = currpos
        currpos = newpos

        # pheromone update:
        # if no pheromone exists for this i (first ant traveling) then append?
        # T(i,d) = (1 - rho) * T(i,d) + delta(i,d,c)
        # see article about delta, 'cause that shit's weird
    

    print(np.array(lattice))
    # for s in lattice:
    #     print(s[int(n-8):int(n*4/3)])



def checkWest(row,col,table):
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

def checkNorth(row,col,table):
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

def checkEast(row,col,table):
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

def checkSouth(row,col,table):
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
    aco('hhhh')
    

if __name__ == '__main__':
    main()
