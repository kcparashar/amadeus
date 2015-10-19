from setup import *

pp = pprint.PrettyPrinter(indent=2) 


"""
Method to convert all hdf5 files into csv with 10,000 lines of format:

"""
def convert_to_csv():
	for root, dirs, files in os.walk(msd_subset_data_path):
		files = glob.glob(os.path.join(root,'*.h5'))
		count = 0
		for f in files:
				with parser.File(f, 'r') as h5:
					count += 1

	print count

convert_to_csv()