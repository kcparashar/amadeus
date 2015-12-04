from pyspark import SparkContext
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils

sc = SparkContext("local", "Amadeus Random Forest", pyFiles=['random_forest.py'])

# Load and parse the data file into an RDD of LabeledPoint.
data = sc.textFile("data_timbre.csv")
zipped_data = data.zipWithIndex()
keyed_data = zipped_data.map(lambda line: (line[-1], line[:-1]))

target = sc.textFile("target_timbre.csv")
zipped_target = target.zipWithIndex()
keyed_target = zipped_target.map(lambda line: (line[-1], line[:-1]))

target_data = keyed_data.join(keyed_target)
labled_point_data = target_data.map(lambda tup: LabeledPoint(tup[1][1][0], tup[1][0][0].split(',')))

#map(lambda line: line.split(",")).map(lambda line: tuple((feature for feature in line)))

# Split the data into training and test sets (30% held out for testing)
print("Creating Training and Test Data Split")
(trainingData, testData) = labled_point_data.randomSplit([0.7, 0.3])

# Train a RandomForest model.
#  Empty categoricalFeaturesInfo indicates all features are continuous.
#  Note: Use larger numTrees in practice.
#  Setting featureSubsetStrategy="auto" lets the algorithm choose.

model = RandomForest.trainRegressor(trainingData, categoricalFeaturesInfo={},
                                    numTrees=1000, featureSubsetStrategy="auto",
                                    impurity='variance', maxDepth=8, maxBins=32)

# # Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(testData.count())
print('Test Mean Squared Error = ' + str(testMSE))
print('Learned regression forest model:')
print(model.toDebugString())

# # Save and load model
# model.save(sc, "myModelPath")
# sameModel = RandomForestModel.load(sc, "myModelPath")
