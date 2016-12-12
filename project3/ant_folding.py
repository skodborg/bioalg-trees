import folding
import hpview3k
import sys
import numpy as np
import random as rnd
import math

def aco(S='hhppppphhppphppphp', known_minimal_energy=None):
    ants = 100 if len(S) <= 25 else 15
    alpha = 1
    beta = 2
    rho = 0.9  # pheromone evaporation coeff.
    theta = 0.05
    # steps = 100
    n = len(S)

    input_known_minimal_energy = None
    if known_minimal_energy:
        input_known_minimal_energy = known_minimal_energy
    else:
        input_known_minimal_energy = score_folding(S, folding.fold_hp_string(S))

    # initialize pheromones to 1.0 for all i,d as they have no effect on the decision
    # initially (no previous ants have walked, no pheromones has been left, nothing
    # exists to follow yet) - update as we decide moves
    pheromones = [[1.0, 1.0, 1.0] for _ in range(n)]
    pheromones[0] = None
    pheromones[n-1] = None

    # m_pheromones = [None for _ in range(n)]
    # heuristics format: (S)traight, (L)eft, (R)ight
    # heuristics = [(1.0, 1.0, 1.0)]
    # m_heuristics = [None for _ in range(n)]
    d = {0: 'S', 1: 'L', 2: 'R'}

    ant_trails = []

    result = ''
    iterations = 50
    
    for iteration in range(iterations):
        # if iteration % 1000 == 0:
        #     print(iteration)
        # print('new iteration')
        for ant in range(ants):
        # for ant in range(1):
            trail = []
            lattice = [[None for _ in range(n*3)] for _ in range(n*3)]
        
            # TODO: initpos = rnd.randint(0, n - 2)
            initpos = 0  # all ants start at left-most position in sequence
            fst = S[initpos]
            snd = S[initpos + 1]

            # TODO: arbitrary positions instead of in the middle?
            lattice[n][n] = fst
            lattice[n][n+1] = snd

            prevpos = (n, n)
            currpos = (n, n+1)

            # print('starting pos: %i,%i' % (n, n))
            # print('first direction is relative to nothing, i.e. trivial, going to %i,%i' % (n, n+1))

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

                dead_ends = [False, False, False]
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
                            # heuristics_id = straight(currpos[0], currpos[1], lattice)
                            h_id = straight(currpos[0], currpos[1], lattice)
                            heuristics_id.append(h_id)
                        except Exception as err:
                            dead_ends[d] = True
                            heuristics_id.append(0)
                            # print('My Exception: %s' % err)
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
                            # heuristics_id = left(currpos[0], currpos[1], lattice)
                            h_id = left(currpos[0], currpos[1], lattice)
                            heuristics_id.append(h_id)
                        except Exception as err:
                            dead_ends[d] = True
                            heuristics_id.append(0)
                            # print('My Exception: %s' % err)
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
                            # heuristics_id = right(currpos[0], currpos[1], lattice)
                            h_id = right(currpos[0], currpos[1], lattice)
                            heuristics_id.append(h_id)
                        except Exception as err:
                            dead_ends[d] = True
                            heuristics_id.append(0)
                            # print('My Exception: %s' % err)

                # heuristics_id = list(map(lambda x: x + 1, heuristics_id))
                # heuristics.append(heuristics_id)
                heuristics_id = tuple([x+1 for x in heuristics_id])

                # if i == 1 or i == 2:
                #     print('iteration %i\t\t%s' % (iteration, str(heuristics_id)))

                for d in range(3):
                    denom_sum = 0.0
                    for e in range(3):
                            denom_sum += (pheromones[i][e] ** alpha) * (heuristics_id[e] ** beta)
                    numerator = (pheromones[i][d] ** alpha) * (heuristics_id[d] ** beta)
                    #     denom_sum += (pheromones[i][e] ** alpha) * (heuristics[i][e] ** beta)
                    # numerator = (pheromones[i][d] ** alpha) * (heuristics[i][d] ** beta)
                    prob_id = numerator / denom_sum
                    pid.append(prob_id)

                deadend_directions = [i for i, x in enumerate(dead_ends) if x]
                # if deadend_directions:
                #     print(deadend_directions)
                if len(deadend_directions) == 3:
                    # TODO: handle all dead ends by backtracking
                    print('TODO: found a dead end, implement backtracking')
                if len(deadend_directions) == 2:
                    # print('2 dead ends')
                    # identify non-deadend and make it a 100% choice below by altering pid
                    possible_direction = list(set([0, 1, 2]) - set(deadend_directions))[0]
                    pid = [0.0, 0.0, 0.0]
                    pid[possible_direction] = 1.0
                    # print(pid)
                if len(deadend_directions) == 1:
                    # print('1 dead end')
                    # one dead end, distribute its value to the other two possibilities
                    deadend = deadend_directions[0]
                    possible_direction = list(set([0, 1, 2]) - set([deadend]))
                    half_deadend_prob = math.floor(pid[deadend] / 2)
                    other_half_deadend_prob = pid[deadend] - half_deadend_prob
                    pid[possible_direction[0]] += half_deadend_prob
                    pid[possible_direction[1]] += other_half_deadend_prob
                    pid[deadend] = 0.0
                    # print(pid)

                # pick an element from {S, L, R} with probabilities as defined by pid
                # directions: S:0, L:1, R:2
                # if ant == 0:
                #     print('ant %i:\t%s' % (ant, str(pid)))
                chosen_direction = np.random.choice(3, 1, p=pid)

                # if ant == 0:
                #     print('chosen direction: %i' % chosen_direction)

                if chosen_direction == 0:
                    trail.append('S')
                elif chosen_direction == 1:
                    trail.append('L')
                else:
                    trail.append('R')

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

                # if ant == 0 and iteration == 49:
                #     print(np.array(lattice[3:10]))
                #     print()

                # print('facing %s that leaves us at %i,%i' % (current_direction.upper(), newpos[0], newpos[1]))
                # print()

                # update cached positions to perform the move
                prevpos = currpos
                currpos = newpos
                
            ant_trails.append(tuple(trail))
            # print(np.array(lattice))
            # for s in lattice:
            #     print(s[int(n-8):int(n*4/3)])
        

        # for trail in ant_trails:
        #     fold = 'F' + ''.join(trail).replace('S', 'F')
        #     print('%s\t\tscore: %i' % (fold, score_folding(S, fold)))

        # TODO:
            # pheromone update should depend on the relative success of the ant's tour
            # i.e. if it found an attractive tour (lots of H-H-pairs), it should influence
            # the other ants more than the unattractive tours taken by other ants
            # so the delta term should be affected by the final score of the tour taken
            # by the particular ant? let it drop pheromone reflecting the score of the tour
            # going this way

            # need to update christian's script to do this






        # pheromone update:
            # once all ants have taken a path, the pheromones are updated
            # T(x,y) = (1 - rho) * SUM_k (delta(T(x,y)^k))
            #   where delta(T(x,y)^k) is the amount of pheromone deposited by the k'th
            #   ant, such that delta(T(x,y)^k) = Q/L_k if ant k uses curve xy in its tour
            #   and 0 if not
            #   where Q is a constant and L_k is the cost of the k'th ant's tour (typically length)
            #           so L_k is just |S| here?
            #           no difference between ants, so all deposited pheromone is the same amount? just 1?

            # T(i,d) = (1 - rho) * T(i,d) + delta(i,d,c)
            # see article about delta, 'cause that shit's weird



        # bias the next iteration by updating the pheromones with
        # the best path found in this iteration
        best_trail = None
        best_trail_score = 0
        for trail in ant_trails:
            formatted_trail = 'F' + ''.join(trail).replace('S', 'F')
            trail_score = score_folding(S, formatted_trail)
            if not trail_score:
                trail_score = 0
            if trail_score > best_trail_score:
                best_trail = trail
                best_trail_score = trail_score
        print('best trail: %i \t %s' % (best_trail_score, 'F' + ''.join(best_trail).replace('S', 'F')))

        for i in range(initpos+1, n-1):

            S_count = 1 if best_trail[i-1] == 'S' else 0
            L_count = 1 if best_trail[i-1] == 'L' else 0
            R_count = 1 if best_trail[i-1] == 'R' else 0
            # S_count = sum([1 for x in ant_trails if x[i-1] == 'S'])
            # L_count = sum([1 for x in ant_trails if x[i-1] == 'L'])
            # R_count = sum([1 for x in ant_trails if x[i-1] == 'R'])

            # S_count = 0
            # L_count = 0
            # R_count = 0
            # for trail in ant_trails:
            #     formatted_trail = 'F' + ''.join(trail).replace('S', 'F')
            #     trail_score = score_folding(S, formatted_trail)
            #     if not trail_score:
            #         trail_score = 0
            #     if formatted_trail[i] == 'S':
            #         S_count += trail_score / input_known_minimal_energy
            #     if formatted_trail[i] == 'L':
            #         L_count += trail_score / input_known_minimal_energy
            #     if formatted_trail[i] == 'R':
            #         R_count += trail_score / input_known_minimal_energy
            
            pheromones[i][0] = (1 - rho) * pheromones[i][0] + S_count
            pheromones[i][1] = (1 - rho) * pheromones[i][1] + L_count
            pheromones[i][2] = (1 - rho) * pheromones[i][2] + R_count

        # print(pheromones)

            # TODO: should pheromones be able to hit 0? I guess so

        if iteration == iterations - 1:
            result = ''.join(ant_trails[0]).replace('S', 'F')
            result = ''.join(best_trail).replace('S', 'F')
            # print(''.join(ant_trails[1]).replace('S', 'F'))
        ant_trails.clear()

        # print('pheromones')
        # print(len(pheromones))
        # print('best trail')
        # print(len(best_trail))
    # print('pid: %s' % pid)
    # print('pheromones')
    # print(pheromones)
    return 'F' + result


def checkWest(row,col,table):
    left = table[row][col-2]
    down = table[row+1][col-1]
    up = table[row-1][col-1]

    if table[row][col-1]:
        raise Exception('west: already occupied')

    if left and up and down:
        raise Exception("west: dead end")
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

    if table[row-1][col]:
        raise Exception('north: already occupied')

    if left and up and right:
        raise Exception("north: dead end")
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

    if table[row][col+1]:
        raise Exception('east: already occupied')

    if right and up and down:
        raise Exception("east: dead end")
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

    if table[row+1][col]:
        raise Exception('south: already occupied')

    if left and right and down:
        raise Exception("south: dead end")
    else:
        count = 0
        if(left == "h"):
            count += 1
        if(down == "h"):
            count += 1
        if(right == "h"):
            count += 1
        return count

def north(row, col):
    return row-1, col

def south(row, col):
    return row+1, col

def east(row, col):
    return row, col+1

def west(row, col):
    return row, col-1

def score_folding(string, fold):

    seq = hpview3k.HPFold(string)

    if len(seq) != len(string):
        print("The sequence %s contains illegal characters." % (string))
        sys.exit(1)
        
    absfold = hpview3k.make_absfold(fold)
    relfold = hpview3k.make_relfold(fold)

    if len(absfold) != len(fold) and len(relfold) != len(fold):
        print("The folding %s contains illegal characters." % (fold))
        sys.exit(1)
        
    if len(absfold) == len(seq) - 1:
        seq.SetAbsFold(absfold)
    elif len(relfold) == len(seq) - 1:
        seq.SetRelFold(relfold)
    else:
        print("The folding %s has wrong length." % (fold))
        sys.exit(1)

    return seq.Score()


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
    # input = 'hhhpphhh'
    input = 'hhppppphhppphppphp'
    
    result = aco(input, 4)
    print(result)
    print_folding(input, result)
    print('score: %i' % score_folding(input, result))



    # result = aco('ppphhpphhhhpphhhphhphhphhhhpppppppphhhhhhpphhhhhhppppppppphphhphhhhhhhhhhhpphhhphhphpphphhhpppppphhh')
    # print(result)
    # print_folding('ppphhpphhhhpphhhphhphhphhhhpppppppphhhhhhpphhhhhhppppppppphphhphhhhhhhhhhhpphhhphhphpphphhhpppppphhh', result)

    # best:
    # FFRRFFRLRFRRLLRRL: 3

    # worst:
    # FFLRLFFFRFLFLRFLF
    # i mean... not even a single fold, nothing is folded up against
    # anything but its immediate neighbours in the string

    

if __name__ == '__main__':
    main()
