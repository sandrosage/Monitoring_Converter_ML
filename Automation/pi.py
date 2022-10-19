import argparse
from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV
import time

start_time = time.time()
ap = argparse.ArgumentParser()
ap.add_argument("-cls", "--classifier", required=True,
	help="Choose classifier")
args = vars(ap.parse_args())
cls = args["classifier"]
print(cls + " selected!")

iris = datasets.load_iris()

match cls:
	case "SVM":
		print("SVM")
		parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
		svc = svm.SVC()
		clf = GridSearchCV(svc, parameters)
		clf.fit(iris.data, iris.target)
		print(clf.best_params_)

	case "DT":
		print("DT")

	case "RF":
		print("RF")

	case "KNN":
		print("KNN")
	
stop_time = time.time()

elapsed_time = stop_time-start_time
print(str(elapsed_time) + " s")




