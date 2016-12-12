
import folding as folding
import hpview3k
import ant_folding

testData = [
"hhppppphhppphppphp",
"hphphhhppphhhhpphh",
"phpphphhhphhphhhhh",
"hphpphhphpphphhpphph",
"hhhpphphphpphphphpph",
"hhpphpphpphpphpphpphpphh",
"pphpphhpppphhpppphhpppphh",
"ppphhpphhppppphhhhhhhpphhpppphhpphpp",
"pphpphhpphhppppphhhhhhhhhhpppppphhpphhpphpphhhhh",
"hhphphphphhhhphppphppphpppphppphppphphhhhphphphphh",
"pphhhphhhhhhhhppphhhhhhhhhhphppphhhhhhhhhhhhpppphhhhhhphhphp",
"hhhhhhhhhhhhphphpphhpphhpphpphhpphhpphpphhpphhpphphphhhhhhhhhhhh",
"hhhhpppphhhhhhhhhhhhpppppphhhhhhhhhhhhppphhhhhhhhhhhhppphhhhhhhhhhhhppphpphhpphhpphph",
"pppppphphhppppphhhphhhhhphhpppphhpphhphhhhhphhhhhhhhhhphhphhhhhhhppppppppppphhhhhhhpphphhhpppppphphh",
"ppphhpphhhhpphhhphhphhphhhhpppppppphhhhhhpphhhhhhppppppppphphhphhhhhhhhhhhpphhhphhphpphphhhpppppphhh"]



def runExperiment():
    known_minimal_energy = [4,8,9,9,10,9,8,14,23,21,36,42,53,48,50]
    for i, data in enumerate(testData):
        # fold = folding.fold_hp_string(data)
        fold = ant_folding.aco(data, known_minimal_energy[i])
        score = ant_folding.score_folding(data, fold)

        print(str(i+1) + ": " + data + " " + fold + " " + str(score))

def main():
    runExperiment()

    

if __name__ == '__main__':
    main()
