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

  pp.pprint(["Hello"])
  pp.pprint(features)
  return features

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
  return render_template('index.html', song_name=song_title, predicted_year=year, titles=[song.title for song in songs], artist=demo.artist_name)

@app.route('/song_year/<song_name>')
def song_year(song_name=None):
  #features = get_features(song)
  features = np.array([  6.55146500e+01,   2.27000000e+00,   3.00000000e+00,
           7.10000000e-02,  -2.27100000e+01,   6.09290000e+01,
                    1.00088000e+02,   5.00000000e+00,   6.95000000e-01])
  year = model.predict(features)
  year = str(int(year[0]))
  return render_template('year.html', song_name=song_name, predicted_year=year)

if __name__ == '__main__':
  app.debug = True
  app.run()
