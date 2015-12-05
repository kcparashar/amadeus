from pyspark import SparkContext
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.util import MLUtils

sc = SparkContext("local", "Amadeus Random Forest Run", pyFiles=['run_model.py'])

model = RandomForestModel.load(sc, "myRFModel")

predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum() / float(testData.count())
print('Test Mean Squared Error = ' + str(testMSE))

testAccuracy = labelsAndPredictions.map(lambda (v, p): 1 if (abs(v - p) < 10) else 0).sum() / float(testData.count())
print('Total Accuracy = ' + str(testAccuracy))
