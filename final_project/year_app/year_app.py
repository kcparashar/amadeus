from flask import Flask, render_template
import numpy as np
import pickle
app = Flask(__name__)

with open('cats', 'r') as open_file:
  model = pickle.load(open_file)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/song_year/<song_name>')
def song_year(song_name):
  #features = get_features(song)
  features = np.array([  6.55146500e+01,   2.27000000e+00,   3.00000000e+00,
           7.10000000e-02,  -2.27100000e+01,   6.09290000e+01,
                    1.00088000e+02,   5.00000000e+00,   6.95000000e-01])
  print(features)
  year = model.predict(features)
  print(year)
  print(str(int(year[0])))
  pdb.set_trace()
  return render_template('year.html', predicted_year = str(year[0]))

if __name__ == '__main__':
  app.run()
