import argparse
from Bio import Phylo
import utils


def parse_newicktree(treefile):
    tree = Phylo.read(treefile, 'newick')
    # Phylo.draw_ascii(tree)

    mytree = utils.Tree()
    queue = [(tree.root, mytree.root)]
    idcount = 1
    while queue:
        tup = queue.pop()
        treenode = tup[0]
        mytreenode = tup[1]
        for c in treenode:
            if c.name:
                # leaf
                leafnode = utils.Node(mytreenode, aId=c.name)
                mytreenode.add_child(leafnode)
            else:
                # internal
                innernode = utils.Node(mytreenode, aId='inner%i' % idcount)
                idcount += 1
                mytreenode.add_child(innernode)
                queue.append((c, innernode))
                # TODO: add c.branch_length to parentEdge

    return mytree


def draw_newicktree(treefile):
    tree = Phylo.read(treefile, 'newick')
    Phylo.draw_ascii(tree)


def main():
    parser = argparse.ArgumentParser()

    help_mDist = "Name of file containing newick tree to draw"
    parser.add_argument('newicktreefile', help=help_mDist)

    args = parser.parse_args()

    draw_newicktree(args.newicktreefile)

if __name__ == '__main__':
    main()