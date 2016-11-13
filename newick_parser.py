from Bio import Phylo
import xml.etree.ElementTree as ET
import re
import utils

def parse_newicktree(treefile):
    tree = Phylo.read(treefile, 'newick')
    Phylo.draw_ascii(tree)
    
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

    # print(mytree)
    # print('\nrerooting with %s as new root\n' % mytree.root.leaflist()[4])
    # mytree.reroot(mytree.root.leaflist()[4])
    # print(mytree)
    return mytree


def rfdist(tree1=None, tree2=None):
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

    # print(t1)

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

    # print(t2)

    if tree1 and tree2:
        t1 = tree1
        t2 = tree2

    print(tree1)
    print(tree2)

    # TODO: difference in rf-distance between rooting at [0] and [9]
    commonRoot = t1.root.leaflist()[0]
    t1.reroot(commonRoot)
    for n in t2.root.leaflist():
        if n.id == commonRoot.id:
            t2.reroot(n)
            break


    print(t1)
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
    # print(dict(rename_tbl))
    rename_dict = dict(rename_tbl)
    # print(rename_dict['6'])
    def rename(node):
        if node.id in rename_dict:
            node.data = rename_dict[str(node.id)]
    t2.dfs(rename)

    print(rename_dict)


    def inner_node_annotation(tree):
        root = tree.root
        stack = [root]
        while stack:
            node = stack[-1]
            if node.is_leaf():
                dfs_num = node.data
                parent_max = node.parent.data['max']
                parent_min = node.parent.data['min']
                if dfs_num > parent_max:
                    node.parent.data['max'] = dfs_num
                if dfs_num < parent_min:
                    node.parent.data['min'] = dfs_num
                node.parent.data['size'] += 1
                stack.pop()
            else:
                if not node.data:
                    # first time visiting; create data-dict for inner node
                    # and queue all its children, then continue;
                    node.data = {'min':float('inf'), 'max':float('-inf'), 'size':0, 'id':node.id}
                    stack += node.children  # node.children always non-empty
                else:
                    if node == root:
                        break
                    # second time visiting node, a data-dict has been created
                    # and filled by all children; update parent accordingly
                    parent_dict = node.parent.data
                    this_dict = node.data
                    this_min = this_dict['min']
                    this_max = this_dict['max']
                    this_size = this_dict['size']
                    parent_min = parent_dict['min']
                    parent_max = parent_dict['max']
                    if this_min < parent_min:
                        parent_dict['min'] = this_min
                    if this_max > parent_max:
                        parent_dict['max'] = this_max
                    parent_dict['size'] += this_size

                    this_dict['interval'] = this_max - this_min + 1 == this_size
                    stack.pop()



    inner_node_annotation(t1)
    # print('\n\n')
    inner_node_annotation(t2)

    # t1.dfs(lambda x: print('%s \t %s' % (str(x.id), str(x.data))))
    # print()
    # t2.dfs(lambda x: print('%s \t %s' % (str(x.id), str(x.data))))
    

    t1_splits = []
    t1.dfs(lambda node: t1_splits.append(node.data) if not node.is_leaf() else 'do nothing')
    t2_splits = []
    t2.dfs(lambda node: t2_splits.append(node.data) if not node.is_leaf() else 'do nothing')
    # t2_splits = [n for n in t2_splits if 'interval' in n and n['interval']]
    
    print(t1_splits)
    print()
    print(t2_splits)
    print()

    

    # print(t1_df_intervals)
    # print(t2_splits)

    t1_splits = [(e['min'], e['max'], e['size']) for e in t1_splits]
    t2_splits = [(e['min'], e['max'], e['size']) for e in t2_splits]
    # print()
    print(t1_splits)
    print(t2_splits)

    shared_splits = list(set(t1_splits).intersection(set(t2_splits)))
    print(shared_splits)

    print(len(set(t1_splits)))
    print(len(set(t2_splits)))
    print(len(shared_splits))
    


    rfdist = len(set(t1_splits)) + len(set(t2_splits)) - 2 * len(shared_splits)
    print('rf-dist: %i' % rfdist)

    
    # shared_intervals = list(t1_df_intervals) - list(t2_df_intervals)
    # print(shared_intervals)



def main():
    t1 = parse_newicktree('tree1.new')
    t2 = parse_newicktree('tree2.new')

    rfdist(t1, t2)
    # rfdist()

    


if __name__ == '__main__':
    main()
