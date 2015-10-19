from setup import *

pp = pprint.PrettyPrinter(indent=2) 
allKeys = []
allLocations = []

allEnergy = []
allDance = []
allHotness = []
allTempo = []
allLoudness = []

def getKeysOfSongs(h5):
	key = h5['/analysis/songs']['key'][0]
	if h5['/analysis/songs']['key_confidence'][0] > 0.7: # 70% threshold for EchoNest to guess the key correctly
		allKeys.append(key)

def getEnergyOfSongs(h5):
	energy = h5['/analysis/songs']['energy'][0]
	if energy: 
		print energy
		allEnergy.append(energy)

def getDanceOfSongs(h5):
	danceability = h5['/analysis/songs']['danceability'][0]
	if danceability: 
		print danceability
		allDance.append(danceability)

def getSongHotness(h5):
	hotness = h5['/metadata/songs']['song_hotttnesss'][0]
	if hotness and not math.isnan(hotness): 
		if math.isnan(hotness):
			allHotness
		allHotness.append(hotness)

def getTempoOfSong(h5):
	tempo = h5['/analysis/songs']['tempo'][0]
	if tempo and not math.isnan(tempo): 
		allTempo.append(tempo)

def getLocationOfSongs(h5):
	lat = h5['/metadata/songs']['artist_latitude'][0]
	lon = h5['/metadata/songs']['artist_longitude'][0]
	if lat and lon and not math.isnan(lat) and not math.isnan(lon):
		allLocations.append([lat, lon])

def compareTwo(h5, x_info, y_info, x_arr, y_arr):
	x = h5['/'+x_info[0]+'/songs'][x_info[1]][0]
	if x and not math.isnan(x): 
		y = h5['/'+y_info[0]+'/songs'][y_info[1]][0]
		if y and not math.isnan(y): 
			x_arr.append(x)
			y_arr.append(y)

def countUniqueArtists():
	conn = sqlite3.connect(os.path.join(msd_subset_addf_path,
	                                    'subset_track_metadata.db'))
	q = "SELECT DISTINCT artist_name FROM songs"
	res = conn.execute(q)
	all_artist_names_sqlite = res.fetchall()
	conn.close()

	print "There are " +str(len(all_artist_names_sqlite)) + " distinct artists in our 10,000 song subset"

def averageLengthOfSongs():
	conn = sqlite3.connect(os.path.join(msd_subset_addf_path,
	                                    'subset_track_metadata.db'))
	q = "SELECT duration FROM songs"
	res = conn.execute(q)
	all_durations = res.fetchall()
	durations = [duration[0] for duration in all_durations if duration[0]]

	conn.close()

	print "The mean duration of the songs is " + "{:.2f}".format((np.mean(durations)/60.0)) + " minutes with a std dev of " + \
	 "{:.2f}".format((np.std(durations)/60.0)) + ", min of " + "{:.2f}".format((min(durations)/60.0)) + ", and a max of " + "{:.2f}".format((max(durations)/60.0))

def studyYears():
	conn = sqlite3.connect(os.path.join(msd_subset_addf_path,
	                                    'subset_track_metadata.db'))
	q = "SELECT year FROM songs"
	res = conn.execute(q)
	all_years = res.fetchall()
	years = [year[0] for year in all_years if year[0]]
	conn.close()

	plt.hist(years, bins=100, range=(1910,2010))
	plt.grid(True)
	# plt.show()

	print "The song years range from " + str(min(years)) + " to " + str(max(years))

	yearCount = Counter(years)

	print "There are the most ("+str(yearCount.most_common(1)[0][1])+" songs) from " + str(yearCount.most_common(1)[0][0])  	

def compareArtist():
	conn = sqlite3.connect(os.path.join(msd_subset_addf_path,
	                                    'subset_track_metadata.db'))
	q = "SELECT artist_familiarity, artist_hotttnesss FROM songs"
	res = conn.execute(q)
	results = res.fetchall()
	familiarity = [result[0] for result in results if result[0] and result[1]]
	hotness = [result[1] for result in results if result[0] and result[1]]

	conn.close()
	makeScatterPlot(familiarity, hotness, "Familiartiy of artist", "Hotness of Artist")

def enumerateFiles():
	count = 0

	for root, dirs, files in os.walk(msd_subset_data_path):
		files = glob.glob(os.path.join(root,'*.h5'))
		count = len(files)
		for f in files:
				with parser.File(f, 'r') as h5:
					# Running each of the following lines takes time.
					# getKeysOfSongs(h5)
					# getLocationOfSongs(h5)
					# getEnergyOfSongs(h5)
					# getDanceOfSongs(h5)
					# compareTwo(h5, ['metadata', 'song_hotttnesss'], ['analysis', 'tempo'], allHotness, allTempo)
					compareTwo(h5, ['analysis', 'loudness'], ['analysis', 'tempo'], allLoudness, allTempo)
					compareTwo(h5, ['analysis', 'loudness'], ['analysis', 'tempo'], allLoudness, allTempo)
	plotAll()

def makeScatterPlot(x, y, xlabel, ylabel):
	x = np.array(x)
	y = np.array(y)
	plt.scatter(x,y)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	m, b = np.polyfit(x, y, 1) # compute linear regression line
	plt.plot(x, m*x + b, '-', color='red')
	slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
	r_squared = r_value * r_value
	print "The r-squared value for " +xlabel + " vs. " + ylabel + " is " + "{:.5f}".format(r_squared)
	plt.show()


def plotAll():
	print "beginning plotting"
	# Extract all location information into a csv
	# with open('location.csv', 'w') as fp:
	#     a = csv.writer(fp, delimiter=',')
	#     a.writerow(['lat', 'lon'])
	#     a.writerows(allLocations)

	# Plot keys of the subset
	# plt.hist(allKeys)
	# plt.grid(True)
	# plt.show()
	makeScatterPlot(allLoudness, allTempo, "Loudness of Song", "Tempo of Song")
	print(r_value)


# enumerateFiles()

countUniqueArtists()
averageLengthOfSongs()
# studyYears()
compareArtist()



