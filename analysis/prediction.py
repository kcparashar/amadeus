from sklearn import cross_validation, ensemble, linear_model, feature_selection, neighbors
import csv
import numpy as np
import pdb

def main():
    f2 = open('accuracies.txt','w')

    print("Loading Data...")
    
    train = np.genfromtxt(open('data_timbre.csv','r'), delimiter=',', dtype='f8')
    train[np.isnan(train)] = 0
    target = np.genfromtxt(open('target_timbre.csv','r'), delimiter=',', dtype='f8')

    print("Creating test and train data... \n")

    X_train, X_test, y_train, y_test = cross_validation.train_test_split(train, target, test_size=0.1, random_state=0)


    # kNN classifier
    print("Generating kNN...")
    knn = neighbors.KNeighborsClassifier() # default neighbors is 5,
    knn.fit(X_train, y_train);

    print("kNN Accuracy: ")
    knn_accuracy = model_accuracy(knn, X_test, y_test)
    f2.write('kNN accuracy: ' + knn_accuracy + '\n')

    # Random Forest
    print("Generating Random Forest...")
    rf = ensemble.RandomForestClassifier(n_estimators=1000, n_jobs=8)
    rf.fit(X_train, y_train)

    print("Random Forest Accuracy: ")
    rf_accuracy = model_accuracy(rf, X_test, y_test)
    f2.write('Random Forest accuracy: ' + rf_accuracy + '\n')

    # Linear Regression Model
    print("Generating Linear Regression...")
    lr = linear_model.LinearRegression(n_jobs=8)
    lr.fit(X_train, y_train)

    print("Linear Regression Accuracy: ")
    lr_accuracy = model_accuracy(lr, X_test, y_test)
    f2.write('Linear Regression accuracy: ' + lr_accuracy + '\n')

    # Logistic Regression Model
    print("Generating Logistic Regression...")
    lr2 = linear_model.LogisticRegression()
    lr2.fit(X_train, y_train)

    # rfe = feature_selection.RFE(lr2, 2)
    # rfe.fit(X_train, y_train)
    print("Logistic Regression Accuracy: ")
    lr2_accuracy = model_accuracy(lr2, X_test, y_test)
    f2.write('Logistic Regression accuracy: ' + lr2_accuracy + '\n')

    f2.close()

def model_accuracy(model, test_set, test_target):
    guesses = model.predict(test_set)
    right = 0

    for counter, guess in enumerate(guesses):
        if abs(guess - test_target[counter]) < 10:
            right += 1

    accuracy = str(right*1.0/len(test_target))
    print 'Number of close guesses are: ' + str(right)
    print 'Total accuracy = ' + accuracy  + '\n'
    return accuracy



if __name__=="__main__":
    main()
