## Name: analysis_Spark.py 
## Authors: Krishna Parashar, Max Wolffe
## Purpose: Run Analysis on Million Dollar Dataset using Spark 

### Imports
import numpy as np
import csv
import pdb

from pyspark import SparkContext, Bootstrap
from sklearn import cross_validation, ensemble, linear_model, feature_selection, neighbors, datasets
from sklearn.cross_validation import train_test_split


def parallelize(sc, model, train, target, size, X_train, X_test, y_train, y_test):
	samples = sc.parallelize(Bootstrap(size))

	trained_data = samples.map(lambda (i, _): model.fit(train[i], target[i])).predict(X_test).map()
	return trained_data


def model_accuracy(model, test_set, test_target):
    guesses = model.predict(test_set)
    right = 0

    for counter, guess in enumerate(guesses):
        if abs(guess - test_target[counter]) < 5:
            right += 1

    print 'Number of close guesses are: ' + str(right)
    print 'Total accuracy = ' + str(right*1.0/len(test_target))


def main():
    print("Loading Data...")
    with open('data_no_timbre.csv','r') as f:
        reader = csv.reader(f)
        headers = next(reader)
    train = np.genfromtxt(open('data_no_timbre.csv','r'), delimiter=',', dtype='f8', skip_header=1)
    train[np.isnan(train)] = 0
    target = np.genfromtxt(open('target_no_timbre.csv','r'), delimiter=',', dtype='f8')

    print("Creating test and train data...")
    X_train, X_test, y_train, y_test = train_test_split(train, target, test_size=0.1, random_state=0)

    # pdb.set_trace()

    # kNN classifier
    print("Generating kNN...")
    knn = neighbors.KNeighborsClassifier() # default neighbors is 5
   	knn_fit = (SparkContext("local", "Boost"), knn, train, target, target.size, X_train, X_test, y_train, y_test)
    knn.fit(X_train, y_train);

    # Random Forest
    print("Generating Random Forest...")
    rf = ensemble.RandomForestClassifier(n_estimators=1000, n_jobs=8)
    rf.fit(X_train, y_train)

    # Linear Regression Model
    print("Generating Linear Regression...")
    lr = linear_model.LinearRegression(n_jobs=8)
    lr.fit(X_train, y_train)

    # Logistic Regression Model
    print("Generating Logistic Regression...")
    lr2 = linear_model.LogisticRegression()
    # lr2.fit(X_train, y_train)

    rfe = feature_selection.RFE(lr2, 2)
    rfe.fit(X_train, y_train)

    print("kNN Accuracy: ")
    model_accuracy(knn, X_test, y_test)
    print("Random Forest Accuracy: ")
    model_accuracy(rf, X_test, y_test)
    print("Linear Regression Accuracy: ")
    model_accuracy(lr, X_test, y_test)
    print("Logistic Regression Accuracy: ")
    model_accuracy(rfe, X_test, y_test)



if __name__=="__main__":
    main()
