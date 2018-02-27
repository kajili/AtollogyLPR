# Usage for this script: "python alprbatch.py [imageDirectory] [output file name]"


import os
from struct import*
import sys
import subprocess
import time

start = time.time()

outFile = open(sys.argv[2], 'w')
outFile.write("Container:::" +sys.argv[1] + "\n")
outFile.flush()

labels = ['Image:::', 'Test:::', 'Plate:::']

def scan_dir_alpr(dir, script_path, depth):
	cloud_script = script_path + '/OpenALPR_Cloud_API.py'
	for name in os.listdir(dir):
		path = os.path.join(dir,name)

		if(os.path.isfile(path)):
			outFile.writelines(labels[depth] + name + "\n")
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
			outFile.writelines(labels[depth] + name + "\n")
			curr_depth = depth - 1
			os.chdir(path)
			scan_dir_alpr(path, script_path, curr_depth)
		
depth = 2
currentPath = os.getcwd()
scanPath = os.path.join(currentPath, sys.argv[1])
scan_dir_alpr(scanPath, currentPath, depth)

outFile.close()
end = time.time()
print("time elapsed: " + str(end-start) + " seconds.")