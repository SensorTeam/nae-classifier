"""
==================================================================
AUTHOR: HIEN VU
LAST MODIFIED: 01-06-18
==================================================================
KNN WITH INTERPUPILLARY DISTANCE AND EYESHINE COLOUR
INPUT: 		distcolourtest.csv (containing test data)
			distcolourtrain.csv (containing training data)
OUTPUT: 	KNN map with given k and weights 
			Prediction accuracy of test data
USAGE: execute from terminal
			`python3 knn.py`

Modified from scikit-learn.org. Original code available at
http://scikit-learn.org/stable/tutorial/statistical_inference/supervised_learning.html
==================================================================
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from sklearn import neighbors, datasets
from sklearn.preprocessing import StandardScaler


############## SET MACRO VARIABLES #####################

# How many nearest neighbours?
n_neighbors = 15
# 'uniform' or 'distance' # distance assigns weights proportional to the inverse of the distance from query point
WEIGHT = 'distance'

########################################################

# returns prediction accuracy for test data
def predict(filename, model):
	with open(filename, 'r') as f:
		reader = csv.reader(f)
		raw = list(reader)[1:]

	data = np.asarray([row[1:4] for row in raw])
	y = data[:, 0].astype(np.int)
	X = data[:, 1:].astype(np.float)

	# Standardise data (mean=0, std=1)
	X = StandardScaler().fit_transform(X)
	accuracy = 0
	for i in range(len(X)):
		actual = y[i]
		p = model.predict([X[i]])
		if actual == p:
			accuracy += 1
	accuracy = accuracy/len(X)
	return accuracy


# open database
with open('distcolourtrain.csv', 'r') as f:
	reader = csv.reader(f)
	raw = list(reader)[1:]

data = np.asarray([row[1:4] for row in raw])
y = data[:, 0].astype(np.int)
X = data[:, 1:].astype(np.float)

# Standardise data (mean=0, std=1)
X = StandardScaler().fit_transform(X)

h = .01  # step size in the mesh

# Create color maps
cmap_light = ListedColormap(['#FFAAAA', '#AAAAFF', '#AAFFAA', '#FFF3AA', '#F3AAFF'])
cmap_bold = ListedColormap(['#FF0000', '#0000FF', '#00FF00', '#FFDB00', '#DC00FF'])

# we create an instance of Neighbours Classifier and fit the data.
clf = neighbors.KNeighborsClassifier(n_neighbors, weights=WEIGHT)
clf.fit(X, y)

# Plot the decision boundary. For that, we will assign a color to each
# point in the mesh [x_min, x_max]x[y_min, y_max].
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

# Predictions
print("=======================\nk=%s, weights=%s" %(n_neighbors, WEIGHT))
print("Test Data Accuracy: " + str(predict("distcolourtest.csv", clf)))

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(figsize = (10,8))
plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

# Plot also the training points
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
            edgecolor='k', s=20)
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.title("k = %i, weights = '%s'"
          % (n_neighbors, WEIGHT),fontsize=20)
#plt.suptitle("NAE Species Classification",fontsize=15)
plt.xlabel('Hue',fontsize=17)
plt.ylabel('Interpupillary distance',fontsize=17)
leg = [Line2D([0],[0], marker='o', color='w', label='fox', markerfacecolor='#FF0000', markeredgecolor='k',markersize=5),
		Line2D([0],[0], marker='o', color='w', label='cat', markerfacecolor='#0000FF', markeredgecolor='k',markersize=5),
		Line2D([0],[0], marker='o', color='w', label = 'sheep', markerfacecolor='#00FF00', markeredgecolor='k',markersize=5),
		Line2D([0],[0], marker='o', color='w', label = 'deer', markerfacecolor='#FFDB00', markeredgecolor='k',markersize=5),
		Line2D([0],[0], marker='o', color='w', label = 'leopard', markerfacecolor='#DC00FF', markeredgecolor='k',markersize=5)]

plt.legend(handles=leg)
plt.show()

