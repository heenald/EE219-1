import cPickle
import os
from sklearn.datasets import fetch_20newsgroups
from sklearn import svm
import sklearn.metrics as smet
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
from sklearn import cross_validation
import numpy as np


###
# Load datsets
###
comp_tech = [
    "comp.graphics",
    "comp.os.ms-windows.misc",
    "comp.sys.ibm.pc.hardware",
    "comp.sys.mac.hardware"
]

rec_act = [
    "rec.autos",
    "rec.motorcycles",
    "rec.sport.baseball",
    "rec.sport.hockey"
]

train = fetch_20newsgroups(
    subset = 'train',
    categories = comp_tech + rec_act,
)

test =  fetch_20newsgroups(
    subset = 'test',
    categories = comp_tech + rec_act
)

###
# Process datasets with new classifications
###
train.target = map(lambda x : int(0 <= x and x < 4), train.target)
test.target = map(lambda x : int(0 <= x and x < 4), test.target)

if not (os.path.isfile("Data/Train_LSI.pkl") and os.path.isfile("Data/Test_LSI.pkl")):
    print "Performing LSI on the TFxIDF matrices for Train and Test"
    execfile('d.py')


train_lsi = cPickle.load(open("Data/Train_LSI.pkl", "r"))
test_lsi = cPickle.load(open("Data/Test_LSI.pkl", "r"))

print "Dataset prepared for SVM"

print "Learning best parameter value for k!"
params = list(range(-3, 4))
scores = []

for param in params:
    print "Parameter ", param
    classifier = svm.SVC(kernel='linear', C = 10 ** -(param))
    scores.append(
        np.mean(
            cross_validation.cross_val_score(
                classifier,
                train_lsi,
                train.target,
                cv = 5
            )
        )
    )

best_param = params[scores.index(max(scores))]

print "Best Score was obtained for k = ", best_param
classifier = svm.SVC(kernel='linear', C = 10 ** -(best_param))

classifier = svm.SVC(kernel='linear')

print "Training SVM classifier"
classifier.fit(train_lsi, train.target)

print "Predicting classifications of testing dataset"
predicted = classifier.predict(test_lsi)

print "Statistics of SVM classifiers:"
print "Accuracy is ", smet.accuracy_score(test.target, predicted) * 100
print "Precision is ", smet.precision_score(test.target, predicted, average='macro') * 100

print "Recall is ", smet.recall_score(test.target, predicted, average='macro') * 100

print "Confusion Matrix is ", smet.confusion_matrix(test.target, predicted)


x, y, _ = roc_curve(test.target, predicted)

plt.plot(x, y, label="ROC Curve")

plt.plot([0, 1], [0, 1])

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.2])

plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('ROC Curves for SVM Classifier')
plt.legend(loc="best")

plt.savefig('plots/svm.png', format='png')
plt.show()
