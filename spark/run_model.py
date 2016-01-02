from pyspark import SparkContext
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils

sc = SparkContext("local", "Amadeus Random Forest Run", pyFiles=['run_model.py'])

data = sc.textFile("data_timbre.csv")
zipped_data = data.zipWithIndex()
keyed_data = zipped_data.map(lambda line: (line[-1], line[:-1]))

target = sc.textFile("target_timbre.csv")
zipped_target = target.zipWithIndex()
keyed_target = zipped_target.map(lambda line: (line[-1], line[:-1]))

target_data = keyed_data.join(keyed_target)
labled_point_data = target_data.map(lambda tup: LabeledPoint(tup[1][1][0], tup[1][0][0].split(',')))

# Split the data into training and test sets (30% held out for testing)
print("Creating Training and Test Data Split")
(trainingData, testData) = labled_point_data.randomSplit([0.7, 0.3])

model = RandomForestModel.load(sc, "myRFModel")

predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(testData.count())
print('Test Mean Squared Error = ' + str(testMSE))

testAccuracy = labelsAndPredictions.map(lambda (v, p): 1 if (abs(v - p) < 10) else 0).sum() / float(testData.count())
print('Total Accuracy = ' + str(testAccuracy))
