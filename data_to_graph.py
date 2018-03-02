# To use this script must install the fpdf module, run: `sudo pip install fpdf`
# Usage: `python data_to_graph.py <parsedDataFile>`

import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_pdf import PdfPages
from fpdf import FPDF

#Setting Up Variables, Some are storing data that is not used during this script -> camera_software & source & Similiarity
text_file = sys.argv[1]
data_entry = False
end_flag = False
test_type = ''
source = []
similarity = []
camera_software = []
distance = []
best_value = []
plate = []
first_time = True
which = 0
pdf = FPDF()
pdf_names = []
def dograph(value,title,source,datax,plate):
    # Stripping New Line and Converting String into INT to use in MatPlot
    for i in range(len(value)):
        value[i].rstrip('\n')
        value[i] = int(float(value[i]))

    for i in range(len(datax)):
        datax[i].rstrip('\n')
        datax[i] = int(float(datax[i]))

    plt.xlabel('Distance')
    plt.ylabel('Plate Similarity')



    plate =  plate.rstrip('\n')
    title_pdf = title + ' ' + plate + '.png'
    new_title  = title + ' ' + plate
    plt.title(new_title)
    datax = sorted(datax,key = int)
    # Splitting Data between Both sources
    even = best_value[0::2]
    odd = best_value[1::2]

    plt.plot(datax,even, color='red', linestyle='-', marker='o')

    plt.plot(datax,odd,color='green', linestyle='-', marker = 'o')

    red_patch = mpatches.Patch(color='red', label='OpenALPR')
    green_patch = mpatches.Patch(color='green', label='Cloud-OpenALPR')
    plt.legend(handles=[red_patch,green_patch])
    pdf_names.append(title_pdf)
    plt.savefig(new_title)
   # plt.show()
    plt.cla()


def makepdf(graphnames):
    graphnames.sort()
    for each in graphnames:
        pdf.add_page()
        pdf.image(each)
    pdf.output("GraphData.pdf", "F")
#------------

parse = open(text_file,'r')
# Parses through each line checking each label

for line in parse:
    data = line.split(':::')
    for i,j in enumerate(data):
        if j == "Plate":
                plate.append(data[i+1])
        if j == "Test":
            if data_entry:
                data_entry = False
                # Creates Graph once it encounters a different test
                if test_type != data[i+1]:
                    which = 0
                    if (len(plate) == 2):
                        if (first_time):
                            which = 0
                            first_time = False;
                        else:
                            which = 1
                    dograph(best_value,test_type,source,distance,plate[which])
                    #Reset Variables
                    data_entry = False
                    end_flag = False
                    test_type = ''
                    source = []
                    similarity = []
                    camera_software = []
                    distance = []
                    best_value = []
            data_entry = True
            test_type = data[i+1]
            distance.append(data[i+2])
        if j == "Source":
            source.append(data[i+1])
        if j == "Result":
            camera_software.append(data[i+1])
            similarity.append(data[i+2])
        if j == "Best":
            end_flag = True
            best_value.append(data[i+1])
makepdf(pdf_names)
parse.close()
sys.exit()

