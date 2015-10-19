## Project Preliminary Data Analysis
This assignment involves detailed analysis of your Project dataset. Its a team assignment. You should hand in your write-up using the submission page linked at the end of this page.

For this experiment, you should do the analysis you plan to do for your final project on the data sample you have so far. Dont try to work at scale yet. You should use this stage to plan your final analysis.

You will probably find it most convenient to do your analysis/write-up with an IPython Notebook. You can attach the notebook to your submission, but make sure all the data cells and graphics cells have been evaluated in the file you submit. We wont have access to your data, and wont be able to rerun the cells. If you have to run any long calculations, save the results to a file and reload them in the notebook so you can keep editing and quickly re-running the notebook.

Please use the following named sections. Its fine to re-use text from your earlier project assignments. But some projects have made large or small changes in their project topic and we need to keep track of their current topic.

## Problem Statement and Background (2 points)
A high-level statement of the problem you intend to address, e.g. finding correspondences between neural recordings and DNN layers. Try to translate the high-level into specific questions if you can.

Give background on the problem you are solving: why it is interesting, who is interested, what is known, some references about it, etc.

## The Data Source(s) You Are Using (2 points)
Describe the data source(s) you have. How much data you have now, and how much you expect to use for your final analysis. We will need that information soon so we can get the necessary data to you.

## Data Joining/Cleaning You Did (4 points)
If data is being joined, describe the joining process and any problems with it - explain the metric used for fuzzy joins.

Explain how you will handle missing or duplicate keys. Describe the tools you used to examine/repair/clean the data.

If you found any statistical anomalies last time, explain how you plan to deal with them.

## Analysis Approach (3 points)
Describe what analysis you are doing: This will probably comprise:

- Featurization: Explain how you generated features from the raw data. e.g. thresholding to produce binary features, binning, tf-idf, multinomial -> multiple binary features (one-hot encoding). 
- Describe any value transformations you did, e.g. histogram normalization.
- Modeling: Which machine learning models did you try? Which do you plan to try in the future?
- Performance measurement: How will you evaluate your model and improve featurization etc.

## Preliminary Results (6 Points)
Summarize the results you have so far:

Define suitable performance measures for your problem. Explain why they make sense, and what other measures you considered.
Give the results. These might include accuracy scores, ROC plots and AUC, or precision/recall plots, or results of hypothesis tests.
Describe any tuning that you did.
Explain any hypothesis tests you did. Be explicit about the null and alternative hypothesis. Be very clear about the test you used and how you used it. Include all the experiment details (between/within-subjects, degrees-of-freedom etc). Be frugal with tests. Do not try many tests and report the best results.
Use graphics! Please use visual presentation whenever possible. The next best option is a table. Try to avoid "inlining" important results.

## Final Analysis, any Obstacles (3 Points)
Describe the final analysis you plan to do:

- Scale: how much data will you use?
- Model complexity: What complexity of models will you use, this is relevant for models like clustering, factor models, Random Forests etc.
- What tools will you use?
- Estimate of processing time? You should be able to form an estimate of how much time you need on your chosen tools.
and outline any obstacles you foresee.

___

# Chart Prediction by Data Daddies

In this project, we will attempt to discover the features behind the popular music of each generation. For instance, if Britney Spears, “Oops I Did It Again” made the charts in 2001, and The Beatles’ “Real Love” made the charts in 1996, we want to see what made the music popular back then – was it the timbre, audio quality, or lyrics? We will then attempt to build a model that is able to predict when the song would have been most popular, which can be useful for future music analyses.

### Installation

1. Obtain the Million Song Dataset, or Million Song Subset: http://labrosa.ee.columbia.edu/millionsong/pages/getting-dataset
2. Obtain the sample codebase. https://github.com/tb2332/MSongsDB 
3. Download SQLite DB Browser: http://sqlitebrowser.org
4. Download Panoply (to open HDFS5): http://www.giss.nasa.gov/tools/panoply/download_mac.html
5. Clone the repo, and work in **dataexploration.py**. Set your own path to the Million Song Dataset subset in **setup.py**.

### Acknowledgements
----

Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. 
The Million Song Dataset. In Proceedings of the 12th International Society
for Music Information Retrieval Conference (ISMIR 2011), 2011.


