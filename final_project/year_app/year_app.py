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

app = Flask(__name__)

with open('cats', 'r') as open_file:
  model = pickle.load(open_file)

# 'duration', 'end_of_fade_in', 'key','key_confidence','loudness',
# 'start_of_fade_out','tempo','time_signature''time_signature_confidence'
def get_features(song):
  features = []

  a_sum = song.audio_summary
  url = a_sum['analysis_url']
  print "\n"*5
  print url
  print "\n"*5

  r = requests.get(url)
  info = r.json()['track']
  print r.json().keys()
  features.append(a_sum['duration'])
  features.append(info['end_of_fade_in'])
  features.append(info['key'])
  features.append(info['key_confidence'])
  features.append(info['loudness'])
  features.append(info['start_of_fade_out'])
  features.append(info['tempo'])
  features.append(info['time_signature'])
  features.append(info['time_signature_confidence'])

  pp.pprint(["Hello"])
  pp.pprint(features)
  return features, info['']

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/song_guess', methods=['GET', 'POST'])
def guess_song():
  songs = pysong.search(title=request.form['song'], results=50, sort="song_hotttnesss-desc")
  song_title = songs[0].title
  demo = songs[0]
  
  a_sum = demo.audio_summary
  duration = a_sum['duration']
  features = get_features(demo)
  year = model.predict(features)
  year = str(int(year[0]))
  return render_template('index.html', song_name=song_title, predicted_year=year, titles=[song.title for song in songs], artist=demo.artist_name, actual_year=1234)


if __name__ == '__main__':
  app.debug = True
  app.run()
