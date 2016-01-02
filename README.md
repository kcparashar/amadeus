# Amadeus
"**Predict the popular year for a song**."

### Goal
In this project, we will attempt to discover the features behind the popular music of each generation. For instance, if Britney Spears, “Oops I Did It Again” made the charts in 2001, and The Beatles’ “Real Love” made the charts in 1996, we want to see what made the music popular back then – was it the timbre, audio quality, or lyrics? We will then attempt to build a model that is able to predict when the song would have been most popular, which can be useful for future music analyses.

### Installation

1. Obtain the Million Song Dataset, or Million Song Subset: http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset
2. Obtain the sample codebase. https://github.com/tb2332/MSongsDB 
3. Download SQLite DB Browser: http://sqlitebrowser.org
4. Download Panoply (to open HDFS5): http://www.giss.nasa.gov/tools/panoply/download_mac.html
5. Clone the repo, and work in **dataexploration.py**. Set your own path to the Million Song Dataset subset in **setup.py**.

### Installing the EchoNestAPI 

Either: 
- Use setuptools: `easy_install -U pyechonest`
- Download the zip from the releases page: https://github.com/echonest/pyechonest/releases
  - Unpack, navigate to the echonest directory and run: `sudo python setup.py install`


### Acknowledgements
----

Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. 
The Million Song Dataset. In Proceedings of the 12th International Society
for Music Information Retrieval Conference (ISMIR 2011), 2011.


