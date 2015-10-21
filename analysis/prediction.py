from sklearn import cross_validation, ensemble, linear_model, feature_selection

import numpy as np
import pdb

def main():
	train = np.genfromtxt(open('data_no_timbre.csv','r'), delimiter=',', dtype='f8')
	train[np.isnan(train)] = 0
	target = np.genfromtxt(open('target_no_timbre.csv','r'), delimiter=',', dtype='f8')

	X_train, X_test, y_train, y_test = cross_validation.train_test_split(train, target, test_size=0.1, random_state=0)

	# pdb.set_trace()
	
	# Random Forest
	# rf = ensemble.RandomForestClassifier(n_estimators=1000, n_jobs=8)
	# rf.fit(X_train, y_train)
	
	# Linear Regression Model
	# lr = linear_model.LinearRegression(n_jobs=8)
	# lr.fit(X_train, y_train)

	# Logistic Regression Model
	lr2 = linear_model.LogisticRegression()
	# lr2.fit(X_train, y_train)

	rfe = feature_selection.RFE(lr2, 2)
	rfe.fit(X_train, y_train)

	model = rfe # Set model here for prediction
	
	guesses = model.predict(X_test)

	right = 0

	for counter, guess in enumerate(guesses):
		if abs(guess - y_test[counter]) < 5:
			right += 1

	print 'Number of close guesses are: ' + str(right)
	print 'Total accuracy = ' + str(right*1.0/len(y_test))

if __name__=="__main__":
	main()