import argparse
import newick_parser as nwk
import utils


def rfdist(tree1, tree2):
    t1 = tree1
    t2 = tree2

    # step 1:
    # reroot the trees with a common root (1st one found in leaflist of t1)
    commonRoot = t1.root.leaflist()[0]
    t1.reroot(commonRoot)
    for n in t2.root.leaflist():
        if n.id == commonRoot.id:
            t2.reroot(n)
            break

    # step 2:
    # make a depth-first numbering of the leaves in t1
    def dfs_numbering():
        count = 1

        def func(node):
            nonlocal count
            if node.is_leaf():
                node.data = count
                count += 1
        return func
    t1.dfs(dfs_numbering())

    # step 3:
    # rename leaves in t2 cf. the depth-first numbering of leaves in t1
    rename_tbl = []
    t1.dfs(lambda node: rename_tbl.append((node.id, node.data))
           if node.is_leaf() else 'do nothing')
    rename_dict = dict(rename_tbl)

    def rename(node):
        if node.id in rename_dict:
            node.data = rename_dict[str(node.id)]
    t2.dfs(rename)

    # step 4:
    # annotate internal nodes in t1 with dfs-intervals, identify
    # intervals in t2 as these are potential shared splits
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
                    node.data = {'min': float('inf'),
                                 'max': float('-inf'),
                                 'size': 0,
                                 'id': node.id}
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
    inner_node_annotation(t2)

    # step 5:
    # find shared splits between t1 and t2 and calculate the final rf distance
    t1_splits = []
    t1.dfs(lambda node: t1_splits.append(node.data)
           if not node.is_leaf() else 'do nothing')
    t2_splits = []
    t2.dfs(lambda node: t2_splits.append(node.data)
           if not node.is_leaf() else 'do nothing')

    t1_splits = [(e['min'], e['max'], e['size']) for e in t1_splits]
    t2_splits = [(e['min'], e['max'], e['size']) for e in t2_splits]
    shared_splits = list(set(t1_splits).intersection(set(t2_splits)))

    rfdist = len(set(t1_splits)) + len(set(t2_splits)) - 2 * len(shared_splits)

    return rfdist


def main():
    parser = argparse.ArgumentParser()

    help_t1 = "Name of file containing 1st tree in newick format"
    parser.add_argument('tree1', help=help_t1)
    help_t2 = "Name of file containing 2nd tree in newick format"
    parser.add_argument('tree2', help=help_t2)

    args = parser.parse_args()

    tree1 = nwk.parse_newicktree(args.tree1)
    tree2 = nwk.parse_newicktree(args.tree2)

    rfdist(tree1, tree2)


if __name__ == '__main__':
    main()
