import argparse
import sys
sys.path.append('../project1')
import utils
import numpy as np


def parseDistMatrix(phylibfile):
    f = open(phylibfile, 'r')
    dim = int(f.readline())
    mDist = []
    name2idx = {}
    for i in range(dim):
        nextline = f.readline().rstrip().split(' ')
        name = nextline.pop(0)
        name2idx[name] = i
        mDist_row = list(map(float, nextline))
        mDist.append(mDist_row)
    return mDist, name2idx

def nj(phylibfile):
    # -------- initialization --------
    mDist, name2idx = parseDistMatrix(phylibfile)
    
    # step 1:
    S = list(name2idx.keys())

    # step 2:
    T = utils.Tree()
    for s in S:
        T.root.add_child(utils.Node(aId=s))
    
    # -------- algorithm loop --------
    # step 1:
    #   (a)
    N = [[None for _ in range(len(S))] for _ in range(len(S))]
    for si in S:
        for sj in S:
            i = name2idx[si]
            j = name2idx[sj]
            d_ij = mDist[i][j]
            ri = 1 / (len(S) - 2) * sum(mDist[i])
            rj = 1 / (len(S) - 2) * sum(mDist[j])
            n_ij = d_ij - (ri + rj)
            N[i][j] = n_ij
    #   (b)
    N = np.array(N)
    min_n_ij = np.argmin(N)
    min_i, min_j = divmod(min_n_ij, len(S))
    print((min_i, min_j))

    # step 2:
    # TODO

    # step 3:
    # TODO

    # step 4:
    # TODO

    # step 5:
    # TODO

    # --------- termination ----------
    # TODO

    

def main():
    parser = argparse.ArgumentParser()

    help_mDist = "Name of file containing distance matrix in phylib format"
    parser.add_argument('distancematrix', help=help_mDist)

    args = parser.parse_args()

    nj(args.distancematrix)


if __name__ == '__main__':
    main()
