"""
# Script used to take generate a file that contains parsed data to be used for visualization.
# (Input data comes from raw "alprbatch.py output" 

Usage:
	`python output_to_data.py <inputFile> <outputFile>`

"""


import sys
import numpy

def parse(file, parsedData):

	plate = None
	test = None
	image = None
	distance = None
	source = None
	result = None
	best = None


	for line in file:

		if line.startswith("Plate"):
			split_line = line.split(":::")
			plate = split_line[1]

			parsedData[plate] = {}

		if line.startswith("Test"):
			split_line = line.split(":::")
			test = split_line[1]

			parsedData[plate][test] = {}

		if line.startswith("Image"):
			split_line = line.split(":::")
			image = split_line[1].split("_")

			
			distance = image[0][-2:]
			type_info = image[1].split(".")[0]

			if not distance in parsedData[plate][test]:
				parsedData[plate][test][distance] = {}

		if line.startswith("open"):
			split_line = line.split(":::")
			test_result = split_line[1]
			source = "Open"
			similarity = getSimilarity(plate, test_result)

			if not source in parsedData[plate][test][distance]:
				parsedData[plate][test][distance][source] = {}

			if not "Result" in parsedData[plate][test][distance][source]:
				parsedData[plate][test][distance][source]["Result"] = {}

			parsedData[plate][test][distance][source]["Result"][type_info] = similarity

		if line.startswith("cloud"):
			split_line = line.split(":::")
			test_result = split_line[1]
			source = "Cloud"
			similarity = getSimilarity(plate, test_result)

			if not source in parsedData[plate][test][distance]:
				parsedData[plate][test][distance][source] = {}

			if not "Result" in parsedData[plate][test][distance][source]:
				parsedData[plate][test][distance][source]["Result"] = {}

			parsedData[plate][test][distance][source]["Result"][type_info] = similarity


	#print ("Counter " + str(counter))

def prettyPrint(parsedData):

	#

	for plate, plate_data in zip( parsedData.keys(), parsedData.values() ):

		print("Plate:::" + plate.rstrip('\n') )
		for test, test_data in zip( plate_data.keys(), plate_data.values() ):				
			
			for distance, distance_data in zip( test_data.keys(), test_data.values() ):

				print("Test:::" + test.rstrip('\n') + ":::" + distance.rstrip('\n'))
				for source, source_data in zip( distance_data.keys(), distance_data.values() ):

					print("Source:::" + source)
					for element, element_data in zip( source_data.keys(), source_data.values() ):

						if element == "Best":
							print("Best:::" + str(element_data))

						else:
							for result_type, result_value in zip( element_data.keys(), element_data.values() ):
								print("Result:::" + result_type + ":::" + str(result_value))


def getSimilarity(plate, test):
	similarity = 0.0

	if not test.startswith("No license"):

		for plate_char, test_char in zip(plate, test):
			if plate_char == test_char:
				similarity += 1

	similarity = similarity/len(plate)
	similarity = similarity*100
	similarity = int(similarity)

	return similarity 


def generateBest(parsedData):

	for plate in parsedData.values():
		for test in plate.values():
			for distance in test.values():
				for source in distance.values():
					#best_value = max( source["Result"].values() )
					best_value = numpy.mean( source["Result"].values() )
					source["Best"] = best_value


def main():

	inputFilename = sys.argv[1]

	file = open(inputFilename,'r')

	parsedData = {}

	parse(file, parsedData)

	generateBest(parsedData)

	prettyPrint(parsedData)

	file.close()




if __name__ == '__main__':
	main()