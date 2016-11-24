import os
import subprocess
import time

def runQuick():


	folder = '/Users/simonfischer/Documents/bioinformatik/biotree/bioalg-trees/unique_distance_matrices'
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


			f = open(folderForQuick + "/" + file[:-4] + ".newick",'w')
			f.write(output.decode("utf-8")) # python will convert \n to os.linesep
			f.close()

	print(names)
	print(elapsedTime)

def runRapidNJ():
	folder = '/Users/simonfischer/Documents/bioinformatik/biotree/bioalg-trees/unique_distance_matrices'
	folderForRapid = '/Users/simonfischer/Documents/bioinformatik/biotree/bioalg-trees/project2/rapid/'
	cmdForRapid = '/Users/simonfischer/Downloads/bin-2.3.2/mac_64/rapidnj'
	names = ""
	elapsedTime = ""
	for file in os.listdir(folder):
		if file.endswith(".phy"):
			cmd = cmdForRapid + " " + folder + "/"+ file + "  -i pd -o t -x " + folderForRapid +  file[:-4] + ".newick"

			start = time.time()
			output = subprocess.check_output(cmd, shell=True)
			end = time.time()

			elapsed = end - start

			names += ","+file
			elapsedTime += "," + str(elapsed)


	print(names)
	print(elapsedTime)



def main():
	runRapidNJ()
	

if __name__ == '__main__':
    main()
