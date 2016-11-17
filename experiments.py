import newick_parser as nwk
import rfdist as rfdist
from prettytable import PrettyTable


alignments = ["ClustalOmega",
              "kalign",
              "MAFFT",
              "MUSCLE"]

njMethods = ["QUICK", "RAPID"]




def experiment1():
    i = 0
    x = ""
    for alignment in alignments:
        for method in njMethods:
            if((alignment == "MUSCLE" and method == "QUICK")):
                continue
            x = x + alignment+"/"+method+","


    x = x + "\n"
    for alignment in alignments:
        for method in njMethods:
            if((alignment == "MUSCLE" and method == "QUICK")):
                continue
            x = x + alignment + "/" + method+","
          
            for alignment2 in alignments:
                for method2 in njMethods:
                    if((alignment == "MUSCLE" and method == "QUICK") or  (alignment2 == "MUSCLE" and method2 == "QUICK")):
                        continue
                    i += 1
                    tree1Path = "data/" + alignment + "/" + method + "patbase_aibtas.newick"
                    tree2Path = "data/" + alignment2 + "/" + method2 + "patbase_aibtas.newick"
                    tree1 = nwk.parse_newicktree(tree1Path)
                    tree2 = nwk.parse_newicktree(tree2Path)
                    x = x + str(rfdist.rfdist(tree1, tree2)) + ","
                    #print("Compare: \""+ tree1Path + "\" and \"" + tree2Path + "\" SCORE: " + str(rfdist.rfdist(tree1, tree2)))
            x = x + "\n"


    print(x)

def experiment2():

    for alignment in alignments:
        for method in njMethods:

            if(alignment == "MUSCLE" and method == "QUICK"):
                continue

            tree1Path = "data/" + alignment + "/" + method + "patbase_aibtas.newick"
            tree2Path = "data/" + alignment + "/" + method + "patbase_aibtas_permuted.newick"
            tree1 = nwk.parse_newicktree(tree1Path)
            tree2 = nwk.parse_newicktree(tree2Path)
            print(alignment + "-" + method + ", " + str(rfdist.rfdist(tree1, tree2)))



def main():
    experiment2();


if __name__ == '__main__':
    main()