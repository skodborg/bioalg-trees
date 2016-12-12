
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
	for i, data in enumerate(testData):

		fold = folding.fold_hp_string(data)
		score = ant_folding.score_folding(data, fold)

		print(str(i+1) + ": " + data + " " + fold + " " + str(score))

def main():
    runExperiment()

    

if __name__ == '__main__':
    main()
