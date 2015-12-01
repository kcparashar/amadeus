from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
import numpy as np
import pickle
import requests
import pprint
pp = pprint.PrettyPrinter(indent=4)

from pyechonest import config
config.ECHO_NEST_API_KEY="VMCC2VTEPX2L3TL5V"
from pyechonest import artist as pyartist
from pyechonest import song as pysong

import py7D
import json


app = Flask(__name__)

with open('cats', 'r') as open_file:
# with open('../../../rf.pkl', 'r') as open_file:
  model = pickle.load(open_file)
print "done"

key_dict={0:"C", 1:"C#", 2:"D", 3:"E"+u"\u266D", 4:"E", 5:"F", 6:"F#", 7:"G", 8:"A"+u"\u266D", 9:"A", 10:"B"+u"\u266D", 11:"B"}


# 'duration', 'end_of_fade_in', 'key','key_confidence','loudness',
# 'start_of_fade_out','tempo','time_signature''time_signature_confidence'
def get_features(song):
  features = []

  a_sum = song.audio_summary
  url = a_sum['analysis_url']
  # print "\n"*5
  # print url
  # print "\n"*5
  
  viz_dict = {}

  r = requests.get(url)
  info = r.json()['track']
  features.append(a_sum['duration'])
  features.append(info['end_of_fade_in'])
  features.append(info['key'])
  features.append(info['key_confidence'])
  features.append(info['loudness'])
  features.append(info['start_of_fade_out'])
  features.append(info['tempo'])
  features.append(info['time_signature'])
  features.append(info['time_signature_confidence'])
  # pp.pprint(features)


  viz_dict['dancy'] = a_sum['danceability']*100
  viz_dict['tempo'] = str(int(a_sum['tempo']))
  viz_dict['tempo_rate'] = 60.0/float( a_sum['tempo'])
  viz_dict['loudness'] = a_sum['loudness']
  viz_dict['energy'] = a_sum['energy']*100
  viz_dict["key"] = key_dict[a_sum['key']]
  viz_dict["inst"] = a_sum["instrumentalness"]
  viz_dict["liveness"] = a_sum["liveness"]
  viz_dict["acousticness"] = a_sum["acousticness"]
  viz_dict["valence"] = a_sum["valence"]
  viz_dict["speech"] = a_sum["speechiness"]
  viz_dict["artist_hottness"] = song.artist_hotttnesss
  viz_dict["song_hotttnesss"] = song.song_hotttnesss
  viz_dict["song_currency"] = song.get_song_currency()
  viz_dict["artist_familiarity"] = song.get_artist_familiarity()
  viz_dict["song_discovery"] = song.get_song_discovery()
  pp.pprint(a_sum)
 
  pp.pprint(viz_dict)

  return features, viz_dict

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/song_guess', methods=['GET', 'POST'])
def guess_song():
  count = 0
  while count < 3:
    try:
      songs = pysong.search(title=request.form['song'], buckets=['id:7digital-US', 'tracks', 'song_discovery'], limit=True, results=50, sort="song_hotttnesss-desc")
      break
    except:
      count+=1
    print "Timed out, try again"
  song = songs[0]
  artist_x = song.artist_name
  # pp.pprint([(song.title, song.artist_name) for song in songs[:5]])
  # pp.pprint(song.get_tracks('7digital-US'))
  for_song = song.get_tracks('7digital-US')[0]
  cover_url = for_song['release_image']
  # print cover_url
  foreign_id = for_song['foreign_id'].split(":")[-1]
  # print foreign_id
  response = py7D.request('track', 'details', trackID=str(foreign_id), pageSize=3)
  rel_year = response['response']['track']['release']['releaseDate'].split("-")[0]
  listen = py7D.preview_url(foreign_id)
  print
  print listen
  print
  # pp.pprint(response['response']['track'])
  a_sum = song.audio_summary
  duration = a_sum['duration']
  features, viz_dict = get_features(song)
  year = model.predict(features)
  year = str(int(year[0]))
  print year, rel_year
  return render_template('index.html', song_name=songs[0].title, predicted_year=year, artist=artist_x, 
      actual_year=rel_year, img_url=cover_url, dancy=viz_dict['dancy'], energy=viz_dict['energy'], 
      loudness=viz_dict['loudness'], tempo=viz_dict['tempo'], tempo_rate=viz_dict['tempo_rate'],
      key=viz_dict['key'], a_hot=viz_dict["artist_hottness"], s_hot=viz_dict["song_hotttnesss"],
      a_fam = viz_dict["artist_familiarity"], song_currency = viz_dict["song_currency"], valence=viz_dict["valence"],
      speech = viz_dict["speech"], acousticness=viz_dict["acousticness"], liveness=viz_dict["liveness"],
      song_disc=viz_dict["song_discovery"], mp3=listen )


if __name__ == '__main__':
  app.debug = True
  app.run()
