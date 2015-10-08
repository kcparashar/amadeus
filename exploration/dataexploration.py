from setup import *

allKeys = []
allLocations = []

def getKeysOfSongs(h5):
	key = h5['/analysis/songs']['key'][0]
	if h5['/analysis/songs']['key_confidence'][0] > 0.7: # 70% threshold for EchoNest to guess the key correctly
		allKeys.append(key)

def getLocationOfSongs(h5):
	lat = h5['/metadata/songs']['artist_latitude'][0]
	lon = h5['/metadata/songs']['artist_longitude'][0]
	if lat and lon and not math.isnan(lat) and not math.isnan(lon):
		allLocations.append([lat, lon])


def enumerateFiles():
	count = 0

	for root, dirs, files in os.walk(msd_subset_data_path):
		files = glob.glob(os.path.join(root,'*.h5'))
		count = len(files)

		for f in files:
				with parser.File(f, 'r') as h5:
					# Running each of the following lines takes time.
					# getKeysOfSongs(h5)
					getLocationOfSongs(h5)
	plotAll()

def plotAll():
	# Extract all location information into a csv
	with open('location.csv', 'w') as fp:
	    a = csv.writer(fp, delimiter=',')
	    a.writerow(['lat', 'lon'])
	    a.writerows(allLocations)

	# Plot keys of the subset
	# plt.hist(allKeys)
	# plt.grid(True)
	# plt.show()



enumerateFiles()