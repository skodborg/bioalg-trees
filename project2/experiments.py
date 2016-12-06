import os
import subprocess
import time
import sys
sys.path.append('../project1')

import newick_parser as nwk
import rfdist as rfdist


def runQuick():


	# Absolute paths beacuse we are using the cmd to execute quick
	folder = '/Users/simonfischer/Documents/bioinformatik/biotree/bioalg-trees/project2/distance_matrices'
	folderForQuick = 'quick'
	cmdForQuick = '/Users/simonfischer/Downloads/quicktree_1.1/bin/quicktree'
	names = ""
	elapsedTime = ""
	for file in os.listdir(folder):
		if file.endswith(".phy"):
			cmd = cmdForQuick + " " + folder + "/"+ file

			start = time.time()
			output = subprocess.check_output(cmd, shell=True)
			end = time.time()

			elapsed = end - start

			names += ","+file
			elapsedTime += "," + str(elapsed)


			f = open(folderForQuick + "/" + file[:-4] + ".new",'w')
			f.write(output.decode("utf-8")) # python will convert \n to os.linesep
			f.close()

	print(names)
	print(elapsedTime)

def runRapidNJ():

	# Absolute paths beacuse we are using the cmd to execute rapid
	folder = '/Users/simonfischer/Documents/bioinformatik/biotree/bioalg-trees/project2/distance_matrices'
	folderForRapid = '/Users/simonfischer/Documents/bioinformatik/biotree/bioalg-trees/project2/rapid/'
	cmdForRapid = '/Users/simonfischer/Downloads/bin-2.3.2/mac_64/rapidnj'
	names = ""
	elapsedTime = ""
	for file in os.listdir(folder):
		if file.endswith(".phy"):
			cmd = cmdForRapid + " " + folder + "/"+ file + "  -i pd -o t -x " + folderForRapid +  file[:-4] + ".new"

			start = time.time()
			output = subprocess.check_output(cmd, shell=True)
			end = time.time()

			elapsed = end - start

			names += ","+file
			elapsedTime += "," + str(elapsed)


	print(names)
	print(elapsedTime)

def compareTrees(path1, path2):
    print("Comparing " + path1  + " and " + path2)
    names = ""
    values = ""
    for file1 in os.listdir(path1):
        if file1.endswith(".newick") or file1.endswith(".new"):
            names += ", " + file1[:-4]

            tree1 = nwk.parse_newicktree(path1 + "/" + file1)

            #print(path2 + "/" + file1)
            tree2 = nwk.parse_newicktree(path2 + "/" + file1)


            values += ", " + str(rfdist.rfdist(tree1, tree2))
    print(names)
    print(values)  


def divideList():
    their = "1010.148008, 1381.678318, 1571.265909, 1997.527358, 2246.515009, 2623.143338, 3.795291, 11.061757, 25.509092, 48.017770, 89.911697, 188.484136, 274.840255, 0.313552"
    #their = "0.5069370269775391, 0.6585650444030762, 0.5598330497741699, 0.8477580547332764, 0.9339251518249512, 0.8169398307800293, 0.02202296257019043, 0.03275299072265625, 0.04919290542602539, 0.056723833084106445, 0.12647604942321777, 0.1663517951965332, 0.20669007301330566, 0.012032032012939453"
    our = "4277.495719, 6000.171313, 6920.152123, 8939.407731, 10272.332280, 14162.085274, 14.742557, 40.580975, 91.691191, 170.996032, 331.101792, 719.482883, 1069.082789, 1.192358"
    
    ourList = [float(x) for x in our.split(',')]
    theirList = [float(x) for x in their.split(', ')]

    result = ""
    for i in range(0, len(ourList)):
        result += ", " + str(theirList[i]/ourList[i])
    print(result)

def main():
    #runRapidNJ()
    #runQuick()
    #compareTrees("rapid", "quick")
    #compareTrees("nj_newicktrees", "quick")
    #compareTrees("nj_newicktrees", "rapid")
    #compareTrees("nj_newicktrees", "nj_opt_newicktrees")
    divideList()
	


if __name__ == '__main__':
    main()
