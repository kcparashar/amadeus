from sklearn import cross_validation, ensemble, linear_model, feature_selection, neighbors, metrics
import csv
import numpy as np
import pdb

def main():
    f2 = open('accuracies.txt','a') # Wipe file
    f2.close()

    print("Loading Data...")
    
    train = np.genfromtxt(open('data_timbre_good.csv','r'), delimiter=',', dtype='f8')
    train[np.isnan(train)] = 0
    target = np.genfromtxt(open('target_timbre_good.csv','r'), delimiter=',', dtype='f8')

    print("Creating test and train data... \n")

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(train, target, test_size=0.1, random_state=0)

    # kNN classifier
    # print("Generating kNN...")
    # knn = neighbors.KNeighborsClassifier() # default neighbors is 5,
    # knn.fit(X_train, y_train);
    # knn_accuracy, knn_predictions = model_accuracy(knn, X_test, y_test)
    # printer(y_test, knn_predictions, knn_accuracy, 'k Nearest Neighbors')

    # Random Forest
    # print("Generating Random Forest...")
    # rf = ensemble.RandomForestClassifier(n_estimators=1000, n_jobs=8)
    # rf.fit(X_train, y_train)
    # rf_accuracy, rf_predictions = model_accuracy(rf, X_test, y_test)
    # printer(y_test, rf_predictions, rf_accuracy, 'Random Forest')

    # Linear Regression Model
    print("Generating Linear Regression...")
    lr = linear_model.LinearRegression(n_jobs=8)
    lr.fit(X_train, y_train)
    lr_accuracy, lr_predictions = model_accuracy(lr, X_test, y_test)
    printer(y_test, lr_predictions, lr_accuracy, 'Linear Regression')

    # Logistic Regression Model
    print("Generating Logistic Regression...")
    lr2 = linear_model.LogisticRegression()
    lr2.fit(X_train, y_train)
    lr2_accuracy, lr2_predictions = model_accuracy(lr2, X_test, y_test)
    printer(y_test, lr2_predictions, lr2_accuracy, 'Logistic Regression')


def model_accuracy(model, test_set, test_target):
    guesses = model.predict(test_set)
    right = 0

    predictions = []

    for counter, guess in enumerate(guesses):
        predictions.append(guess)
        if abs(guess - test_target[counter]) < 10:
            right += 1

    accuracy = str(right*1.0/len(test_target))
    print 'Number of close guesses are: ' + str(right)
    print 'Total accuracy = ' + accuracy  + '\n'
    return accuracy, predictions

def printer(y_test, predictions, accuracy, accuracy_type):
    print 'Predicting with ' + accuracy_type

    f2 = open('accuracies.txt','a')
    mean_squared_error = metrics.mean_squared_error(y_test, predictions)
    mean_absolute_error = metrics.mean_absolute_error(y_test, predictions)

    accuracy_print = accuracy_type + ' accuracy: ' + str(accuracy) + 'with mean squared error: ' + str(mean_squared_error) \
      + ' and mean_absolute_error: ' + str(mean_absolute_error) + '\n'
    print accuracy_print
    f2.write(accuracy_print)
    f2.close()


if __name__=="__main__":
    main()
