# Your API Key: VMCC2VTEPX2L3TL5V 
# Your Consumer Key: dda50f21c3821c6209b5898ce647c1eb 
# Your Shared Secret: khQ/AUT4T+C3ZtbPWZu9iw
# 
import sys
import requests
import pprint
import json
pp = pprint.PrettyPrinter(indent=4)

api_key = "VMCC2VTEPX2L3TL5V"
from pyechonest import config
config.ECHO_NEST_API_KEY=api_key
from pyechonest import artist as pyartist
from pyechonest import song as pysong


def all_artist(artist):
	art = pyartist.Artist(artist)

def search_artist(query):
	results = pyartist.search(name=query,sort="familiarity-desc")
	pp.pprint(results)
	songs_by_artist(results[0].id)

def songs_by_artist(art_id):
	results = pysong.search(artist_id=art_id)
	return results

def search_song(query):
	results = pysong.search(title=query, results=50,sort="artist_familiarity-desc")
	pp.pprint([(song.title, song.artist_name, song.id) for song in results])

search_artist("Fetty Wap")
print("\n"*3)
search_song("Hello")
