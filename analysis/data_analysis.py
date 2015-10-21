from setup import *
from sklearn import datasets

pp = pprint.PrettyPrinter(indent=2)

print_local = False # Allows output supression in ipynotebook.

"""
Method to convert all hdf5 files into csv with 10,000 lines of format:
data:
key, mode, tempo, time_signature, loudness, *timbre*

target:
year

The indices of the two match up.

"""
def convert_to_csv():
    i = 0
    header = ['duration',
            'end_of_fade_in',
            'key',
            'key_confidence',
            'loudness',
            'start_of_fade_out',
            'tempo',
            'time_signature',
            'time_signature_confidence']
    #Include header which describes features extracted.
    data = [header]
    target = []
    count = 0


    for root, dirs, files in os.walk(msd_subset_data_path):
        files = glob.glob(os.path.join(root,'*.h5'))
        for f in files:
            local_print("Getting data from: " + str(f))
            with parser.File(f, 'r') as h5:
                year = get_year(h5)
                if year:
                    count +=1
                    target.append([year])
                    row = []
                    local_print("Getting duration...")
                    row += [get_analysis_property(h5,'duration')]
                    local_print("Getting End Fade...")
                    row += [get_analysis_property(h5,'end_of_fade_in')]
                    local_print("Getting Key...")
                    row += [get_analysis_property(h5,'key')]
                    row += [get_analysis_property(h5,'key_confidence')]
                    local_print("Getting Loudness...")
                    row += [get_analysis_property(h5,'loudness')]
                    local_print("Getting Start Fade Out...")
                    row += [get_analysis_property(h5,'start_of_fade_out')]
                    local_print("Getting Tempo...")
                    row += [get_analysis_property(h5,'tempo')]
                    local_print("Getting Time Signiture...")
                    row += [get_analysis_property(h5,'time_signature')]
                    row += [get_analysis_property(h5,'time_signature_confidence')]
                    local_print(str(len(row)) + " Features aquired.")
                    local_print(row)
                    # uncomment row below to get the timbre as well.
                    # row += [get_timbre(h5)]
                    # print row
                    data.append(row)
                    i+=1

    with open('data_no_timbre.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerows(data)

    local_print(target)
    with open('target_no_timbre.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerows(target)

    sample = data[1]
    return zip(sample, header)

def local_print(string):
    if print_local:
        print(string)

def get_timbre(h5):
    listy = []
    timbres = h5['analysis']['segments_timbre']
    print_local(len(timbres))
    timbres = np.array(timbres, dtype='f2')
    timbres = timbres.flatten()
    return list(timbres)

def get_analysis_property(h5, prop):
    to_return = h5['/analysis/songs'][prop][0]
    if to_return:
        return to_return
    else:
        return 0

def get_year(h5):
    to_return = h5['/musicbrainz/songs']['year'][0]
    if to_return:
        return to_return
    else:
        return 0


sample = convert_to_csv()
print(sample)
