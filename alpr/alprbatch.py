import os
from struct import*
import sys
import subprocess

outFile = open('batchOut.txt', 'w')
outFile.write(sys.argv[1] + "\n")
outFile.flush()

def scan_dir_alpr(dir):
	for name in os.listdir(dir):
	    path = os.path.join(dir,name)

	    if(os.path.isfile(path)):
			outFile.writelines(name + "\n")
			#outFile.flush()
			#subprocess.call(['alpr', name], stdout = outFile)
			test = subprocess.Popen(['alpr', name], stdout=subprocess.PIPE)
			test_val = test.communicate()[0]
            
			if test_val.startswith('No license'):
				outFile.writelines(test_val)
			else:
				test_split = test_val.split("\n")[1].split("\t")[0].split("- ")[1]
				outFile.write(test_split + "\n")
			    #print(test_split)

	    else:
			outFile.writelines(name + "\n")
			#outFile.flush()
			os.chdir(path)
			scan_dir_alpr(path)
		

currentPath = os.getcwd()
scanPath = os.path.join(currentPath, sys.argv[1])
scan_dir_alpr(scanPath)

outFile.close()

