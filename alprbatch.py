# Usage for this script: "python alprbatch.py <imageDirectory>"
# Output goes to batchOut.txt

import os
from struct import*
import sys
import subprocess

outFile = open('batchOut.txt', 'w')
outFile.write(sys.argv[1] + "\n")
outFile.flush()

def scan_dir_alpr(dir, script_path):
	cloud_script = script_path + '/OpenALPR_Cloud_API.py'
	for name in os.listdir(dir):
	    path = os.path.join(dir,name)

	    if(os.path.isfile(path)):
			outFile.writelines(name + "\n")
			test = subprocess.Popen(['alpr', name], stdout=subprocess.PIPE)
			test_val = test.communicate()[0]
            
			if test_val.startswith('No license'):
				outFile.write('open:::')
				outFile.writelines(test_val)
			else:
				test_split = test_val.split("\n")[1].split("\t")[0].split("- ")[1]
				outFile.write('open:::')
				outFile.write(test_split + "\n")
			
			test = subprocess.Popen(['python', cloud_script, name], stdout=subprocess.PIPE)
			outFile.write('cloud:::')
			test_val = test.communicate()[0]
			outFile.writelines(test_val)

	    else:
			outFile.writelines(name + "\n")
			os.chdir(path)
			scan_dir_alpr(path, script_path)
		

currentPath = os.getcwd()
scanPath = os.path.join(currentPath, sys.argv[1])
scan_dir_alpr(scanPath, currentPath)

outFile.close()

