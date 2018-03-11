
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
def dograph(title,plate, data1, data2):

    plt.xlabel('Distance')
    plt.ylabel('Plate Similarity')

    plate =  plate.rstrip('\n')
    title_pdf = title + ' ' + plate + '.png'
    new_title  = title + ' ' + plate
    plt.title(new_title)

    dists = [tup[0] for tup in data1]
    open_vals = [tup[1][0] for tup in data1]
    cloud_vals = [tup[1][0] for tup in data2]

    plt.plot(dists, open_vals, color='red', linestyle='-', marker='o')

    plt.plot(dists, cloud_vals, color='green', linestyle='-', marker='o')
    red_patch = mpatches.Patch(color='red', label='OpenALPR')
    green_patch = mpatches.Patch(color='green', label='Cloud-OpenALPR')
    plt.legend(handles=[red_patch,green_patch])
    axes = plt.gca()
    axes.set_ylim([0, 100])
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
                    # collate and sort distance, value, source tuples
                    data_array = [(float(value.strip('\n')), image_source.strip('\n')) for value, image_source in zip(best_value, source)]

                    data_open = [tup for tup in data_array if tup[1].startswith('Open')]
                    data_cloud = [tup for tup in data_array if tup[1].startswith('Cloud')]
                    
                    open_data = [(int(float(dist.strip('\n'))), val_tup) for dist, val_tup in zip(distance, data_open)]
                    cloud_data = [(int(float(dist.strip('\n'))), val_tup) for dist, val_tup in zip(distance, data_cloud)]

                    open_data.sort(key=lambda tup: tup[0])
                    cloud_data.sort(key=lambda tup: tup[0])


                    dograph(test_type,plate[which],open_data, cloud_data)
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

