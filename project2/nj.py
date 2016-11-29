import argparse
import sys
import numpy as np
import time
import os
sys.path.append('../project1')
import utils


def process_distance_matrices(path_to_distancematrices):
    runningtimes = []
    outputdir = 'nj_opt_newicktrees/'
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    # for fname in ['89_Adeno_E3_CR1.phy']:
    for fname in os.listdir(path_to_distancematrices):
        print('processing %s' % fname)
        start = time.time()
        resulttree = nj_opt(path_to_distancematrices + fname)
        # resulttree = nj(path_to_distancematrices + fname)
        end = time.time()
        
        f = open(outputdir + fname[:-4] + '.new', 'w')
        f.write(resulttree.as_newick())
        f.close()
        runtime = end - start

        f2 = open('%srun_%s.txt' % (outputdir, fname), 'w')
        f2.write('%s:%s' % (fname, runtime))
        f2.close()
        
        runningtimes.append((fname, runtime))
        print('finished %s in time %f\n\n' % (fname, runtime))

    str_runningtimes = ''
    for tup in runningtimes:
        str_runningtimes += '%s:%f\n' % (tup[0], tup[1])
    f = open(outputdir + 'running_times.txt', 'w')
    f.write(str_runningtimes)
    f.close()



def nj(phylibfile, outputfile=None):
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

    # -------- initialization --------
    mDist, name2idx = parseDistMatrix(phylibfile)
    k_count = 1
    mDist = np.array(mDist)

    # step 1:
    S = []

    # step 2:
    T = utils.Tree()
    for s in list(name2idx.keys()):
        newnode = utils.Node(aId=s)
        S.append(newnode)
        T.root.add_child(newnode)

    # -------- algorithm loop --------
    while len(S) > 3:
        # start = time.time()
        N = np.array([[None for _ in range(len(S))] for _ in range(len(S))])
        for si in S:
            i = name2idx[si.id]
            ri = 1 / (len(S) - 2) * np.sum(mDist[i])
            for sj in S:
                j = name2idx[sj.id]
                d_ij = mDist[i][j]
                rj = 1 / (len(S) - 2) * np.sum(mDist[j])
                n_ij = d_ij - (ri + rj)
                N[i][j] = n_ij

        #   (b)
        # we want the min dist between two distinct nodes, diagonal is inf
        np.fill_diagonal(N, float('inf'))
        min_n_ij = np.argmin(N)
        min_i, min_j = divmod(min_n_ij, len(S))
        
        # step 2:
        k = utils.Node(aId='k%i' % k_count)
        T.root.add_child(k)
        k_count += 1

        # step 3:
        # TODO: fix, very ugly hacks because of tree data structure :(
        si_name = [s[0] for s in name2idx.items() if s[1] == min_i][0]
        sj_name = [s[0] for s in name2idx.items() if s[1] == min_j][0]
        si = [n for n in S if n.id == si_name][0]
        sj = [n for n in S if n.id == sj_name][0]
        d_ij = mDist[min_i][min_j]
        ri = 1 / (len(S) - 2) * np.sum(mDist[min_i])
        rj = 1 / (len(S) - 2) * np.sum(mDist[min_j])
        gamma_ki = (d_ij + ri - rj) / 2
        gamma_kj = d_ij - gamma_ki
        # assert(gamma_kj == (d_ij + rj - ri) / 2)
        T.root.remove_child(si)
        T.root.remove_child(sj)
        k.add_child(si)
        k.add_child(sj)
        si.parentEdge = gamma_ki
        sj.parentEdge = gamma_kj

        # step 4:
        # TODO: clean up code, very ugly
        temp_S = [s for s in S if s not in [k, si, sj]]
        d_km = [None for _ in range(len(S))]
        for m in temp_S:
            m_idx = name2idx[m.id]
            d_im = mDist[min_i][m_idx]
            d_jm = mDist[min_j][m_idx]
            d_km[m_idx] = (d_im + d_jm - d_ij) / 2

        # delete row i and j
        for idx in sorted([min_i, min_j], reverse=True):
            mDist = np.delete(mDist, idx, axis=0)

        # delete col i and j
        for idx in sorted([min_i, min_j], reverse=True):
            mDist = np.delete(mDist, idx, axis=1)
            del d_km[idx]

        # append d_km as row and col to the end of mDist, extending its dim by 1x1
        numpy_d_km = np.array([d_km])

        mDist = np.concatenate((mDist, numpy_d_km.T), axis=1)
        d_km.append(0.0)
        mDist = np.concatenate((mDist, np.array([d_km])), axis=0)
        
        # step 5:
        S = [s for s in S if s.id not in [si.id, sj.id]]

        name2idx = {name: idx for name, idx in name2idx.items()
                    if idx not in [min_i, min_j]}

        for key, value in name2idx.items():
            gt_i = gt_j = False
            if value > min_i:
                gt_i = True
            if value > min_j:
                gt_j = True
            if gt_i:
                name2idx[key] -= 1
            if gt_j:
                name2idx[key] -= 1

        name2idx[k.id] = len(name2idx)
        S.append(k)
        # end = time.time()
        # print('time: %f' % (end - start))

    # --------- termination ----------
    i, j, m = S
    # use root as the node 'v' in pseudo code
    idx_i = name2idx[i.id]
    idx_j = name2idx[j.id]
    idx_m = name2idx[m.id]
    d_ij = mDist[idx_i][idx_j]
    d_im = mDist[idx_i][idx_m]
    d_jm = mDist[idx_j][idx_m]

    vi = (d_ij + d_im - d_jm) / 2
    vj = (d_ij + d_jm - d_im) / 2
    vm = (d_im + d_jm - d_ij) / 2

    i.parentEdge = vi
    j.parentEdge = vj
    m.parentEdge = vm

    print(T)
    return T


def nj_opt(phylibfile, outputfile=None):
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

    # -------- initialization --------
    mDist, name2idx = parseDistMatrix(phylibfile)
    k_count = 1
    mDist = np.array(mDist)

    # step 1:
    S = []

    # step 2:
    T = utils.Tree()
    for s in list(name2idx.keys()):
        newnode = utils.Node(aId=s)
        S.append(newnode)
        T.root.add_child(newnode)

    cached_rowsum = np.sum(mDist, axis=1)

    # -------- algorithm loop --------
    while len(S) > 3:
        # start = time.time()
        N = np.array([[None for _ in range(len(S))] for _ in range(len(S))])
        for si in S:
            i = name2idx[si.id]
            ri = 1 / (len(S) - 2) * cached_rowsum[i]
            for sj in S:
                j = name2idx[sj.id]
                d_ij = mDist[i][j]
                rj = 1 / (len(S) - 2) * cached_rowsum[j]
                n_ij = d_ij - (ri + rj)
                N[i][j] = n_ij

        #   (b)
        # we want the min dist between two distinct nodes, diagonal is inf
        np.fill_diagonal(N, float('inf'))
        min_n_ij = np.argmin(N)
        min_i, min_j = divmod(min_n_ij, len(S))
        
        # step 2:
        k = utils.Node(aId='k%i' % k_count)
        T.root.add_child(k)
        k_count += 1

        # step 3:
        # TODO: fix, very ugly hacks because of tree data structure :(
        si_name = [s[0] for s in name2idx.items() if s[1] == min_i][0]
        sj_name = [s[0] for s in name2idx.items() if s[1] == min_j][0]
        si = [n for n in S if n.id == si_name][0]
        sj = [n for n in S if n.id == sj_name][0]
        d_ij = mDist[min_i][min_j]
        ri = 1 / (len(S) - 2) * cached_rowsum[min_i]
        rj = 1 / (len(S) - 2) * cached_rowsum[min_j]
        gamma_ki = (d_ij + ri - rj) / 2
        gamma_kj = d_ij - gamma_ki
        # assert(gamma_kj == (d_ij + rj - ri) / 2)
        T.root.remove_child(si)
        T.root.remove_child(sj)
        k.add_child(si)
        k.add_child(sj)
        si.parentEdge = gamma_ki
        sj.parentEdge = gamma_kj

        # step 4:
        # TODO: clean up code, very ugly
        temp_S = [s for s in S if s not in [k, si, sj]]
        d_km = [None for _ in range(len(S))]
        for m in temp_S:
            m_idx = name2idx[m.id]
            d_im = mDist[min_i][m_idx]
            d_jm = mDist[min_j][m_idx]
            d_km[m_idx] = (d_im + d_jm - d_ij) / 2

        # delete row i and j
        for idx in sorted([min_i, min_j], reverse=True):
            mDist = np.delete(mDist, idx, axis=0)
            cached_rowsum = np.delete(cached_rowsum, idx)


        # delete col i and j
        for idx in sorted([min_i, min_j], reverse=True):
            # updated cached rowsum to reflect the removal of two columns
            removed_col = mDist.T[idx]
            cached_rowsum -= removed_col

            mDist = np.delete(mDist, idx, axis=1)
            del d_km[idx]

        # append d_km as row and col to the end of mDist, extending its dim by 1x1
        numpy_d_km = np.array([d_km])
        mDist = np.concatenate((mDist, numpy_d_km.T), axis=1)

        cached_rowsum += numpy_d_km[0]

        d_km.append(0.0)
        mDist = np.concatenate((mDist, np.array([d_km])), axis=0)
        cached_rowsum = np.append(cached_rowsum, np.sum(numpy_d_km))
        
        
        # step 5:
        S = [s for s in S if s.id not in [si.id, sj.id]]

        name2idx = {name: idx for name, idx in name2idx.items()
                    if idx not in [min_i, min_j]}

        for key, value in name2idx.items():
            gt_i = gt_j = False
            if value > min_i:
                gt_i = True
            if value > min_j:
                gt_j = True
            if gt_i:
                name2idx[key] -= 1
            if gt_j:
                name2idx[key] -= 1

        name2idx[k.id] = len(name2idx)
        S.append(k)
        # end = time.time()
        # print('time: %f' % (end - start))

    # --------- termination ----------
    i, j, m = S
    # use root as the node 'v' in pseudo code
    idx_i = name2idx[i.id]
    idx_j = name2idx[j.id]
    idx_m = name2idx[m.id]
    d_ij = mDist[idx_i][idx_j]
    d_im = mDist[idx_i][idx_m]
    d_jm = mDist[idx_j][idx_m]

    vi = (d_ij + d_im - d_jm) / 2
    vj = (d_ij + d_jm - d_im) / 2
    vm = (d_im + d_jm - d_ij) / 2

    i.parentEdge = vi
    j.parentEdge = vj
    m.parentEdge = vm

    print(T)
    return T


def main():
    # parser = argparse.ArgumentParser()

    # help_mDist = "Name of file containing distance matrix in phylib format"
    # parser.add_argument('distancematrix', help=help_mDist)

    # args = parser.parse_args()

    # nj(args.distancematrix)
    # nj_opt(args.distancematrix)
    
    path_to_distancematrices = './distance_matrices/'
    process_distance_matrices(path_to_distancematrices)

if __name__ == '__main__':
    main()
