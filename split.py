"""
==================================================================
AUTHOR: HIEN VU
LAST MODIFIED: 27-05-18
==================================================================
Splits data into test and training data (4:1) for KNN
INPUT: 		distcolour.csv (containing all data)
OUTPUT: 	distcolourtest.csv (containing test data)
			distcolourtrain.csv (containing training data)
USAGE: execute from terminal
			`python3 split.py`
==================================================================
"""

# open file
file = open("distcolour.csv", "r")
data = file.readlines()

# open output files
test = open("distcolourtest.csv", "w")
train = open("distcolourtrain.csv", "w")

# header row
test.write(data[0])
train.write(data[0])

# separate every 4th entry to test data
for i in range(1, len(data)):
	if i%5 == 0:
		test.write(data[i])
	else:
		train.write(data[i])

file.close()
test.close()
train.close()
