from Bio import Phylo
import xml.etree.ElementTree as ET
import re
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
                # TODO: add below to tree
                # if c.branch_length:
                    # print(c.branch_length)
                # else:
                    # print('no branch_length')
                # internal
                innernode = utils.Node(mytreenode, aId='inner%i' % idcount)
                idcount += 1
                mytreenode.add_child(innernode)
                queue.append((c, innernode))

    print(mytree)
    print('\nrerooting with %s as new root\n' % mytree.root.leaflist()[4])
    mytree.reroot(mytree.root.leaflist()[4])
    print(mytree)


def test_slide_tree_example():
    t1 = utils.Tree()
    t1_node1 = utils.Node(aId='1')
    t1.root = t1_node1
    t1_node2 = utils.Node(aId='2')
    t1_node3 = utils.Node(aId='3')
    t1_node4 = utils.Node(aId='4')
    t1_node5 = utils.Node(aId='5')
    t1_node6 = utils.Node(aId='6')
    t1_node7 = utils.Node(aId='7')
    t1_inner1 = utils.Node(aId='inner1')
    t1_inner2 = utils.Node(aId='inner2')
    t1_inner3 = utils.Node(aId='inner3')
    t1_inner4 = utils.Node(aId='inner4')
    t1_inner5 = utils.Node(aId='inner5')
    t1_node1.add_child(t1_inner1)
    t1_inner1.add_child(t1_inner2)
    t1_inner1.add_child(t1_inner3)
    t1_inner2.add_child(t1_node4)
    t1_inner2.add_child(t1_node6)
    t1_inner3.add_child(t1_inner4)
    t1_inner3.add_child(t1_inner5)
    t1_inner4.add_child(t1_node5)
    t1_inner4.add_child(t1_node7)
    t1_inner5.add_child(t1_node2)
    t1_inner5.add_child(t1_node3)

    print(t1)

    t2 = utils.Tree()
    t2_node1 = utils.Node(aId='1')
    t2.root = t2_node1
    t2_node2 = utils.Node(aId='2')
    t2_node3 = utils.Node(aId='3')
    t2_node4 = utils.Node(aId='4')
    t2_node5 = utils.Node(aId='5')
    t2_node6 = utils.Node(aId='6')
    t2_node7 = utils.Node(aId='7')
    t2_inner1 = utils.Node(aId='inner1')
    t2_inner2 = utils.Node(aId='inner2')
    t2_inner3 = utils.Node(aId='inner3')
    t2_inner4 = utils.Node(aId='inner4')
    t2_node1.add_child(t2_inner1)
    t2_inner1.add_child(t2_node6)
    t2_inner1.add_child(t2_inner2)
    t2_inner2.add_child(t2_node4)
    t2_inner2.add_child(t2_inner3)
    t2_inner3.add_child(t2_node5)
    t2_inner3.add_child(t2_node7)
    t2_inner3.add_child(t2_inner4)
    t2_inner4.add_child(t2_node2)
    t2_inner4.add_child(t2_node3)

    print(t2)


    # step 2: make a depth-first numbering of the leaves in t1
    def dfs_numbering():
        count = 1
        def func(node):
            nonlocal count
            if node.is_leaf():
                node.data = count
                count += 1
        return func
    t1.dfs(dfs_numbering())

    # step 3: rename leaves in t2 cf. the depth-first numbering of leaves in t1
    rename_tbl = []
    t1.dfs(lambda node : rename_tbl.append((node.id, node.data)) if node.is_leaf() else 'do nothing')
    print(dict(rename_tbl))
    rename_dict = dict(rename_tbl)
    print(rename_dict['6'])
    





def main():
    # parse_newicktree('tree1.new')
    test_slide_tree_example()

if __name__ == '__main__':
    main()
