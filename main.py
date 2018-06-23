"""
==================================================================
AUTHOR: HIEN VU
LAST MODIFIED: 20-04-18
==================================================================
Locates the eyes and extracts interpupillary distance and 
chromaticity (colour) data from images
Adds eye data to training database with label
INPUT: image (.jpg .png .tiff) containing eyeshine signal, class c
OUTPUT: number of detected pairs, .jpg file with potential eyeshine 
			circled, csv with data appended
USAGE: execute from terminal
			`python3 main.py -i path-to-image -c class`
==================================================================
"""

from find_eye import *
from find_pairs import *
from get_colour import *
import argparse
import csv
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the normal image file")
ap.add_argument("-c", "--class", help = "class for training data")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])
orig = image.copy()
new = image.copy()

# for training data
ID = args["class"]

# find pairs of eyes
contours = find_eye(image)
[con_pairs, pair_det] = find_pairs(image, contours)
num_pairs = len(con_pairs)
fname = os.path.basename(args["image"])
print("------- RESULTS -------")
print("SEARCHED " + str(fname))
print("FOUND " + str(num_pairs) + " PAIR/S")

# set of colours for labelling pairs
colours = [(255,0,0),(0,0,255),(0,255,0),(255,255,0),(255,0,255),(0,255,255),(100,200,100),(100,0,200),(200,100,200),(200,100,100)]
i=0
# circle around the pairs found in the image
for pair in con_pairs:
	i+=1
	col = colours[i%10]
	if len(pair)==2:
		for eye in pair:
			(cX, cY), radius = cv2.minEnclosingCircle(eye)
			cv2.circle(new, (int(cX), int(cY)), int(radius+8), col, 5)
	else:
		pass
# save circled image
cv2.imwrite(fname[0:-4]+"_circled.jpg", new)

"""
# set up new databases
# interpupillary distance and colour
fields1 = ['file','ID','distance','hue','r','g','b']
f1 = open("distcolour.csv", 'w')
writer = csv.writer(f1)
writer.writerow(fields1)
f1.close()
"""

# For each pair
for i in range(0, num_pairs):
	# get eye details for the pair
	con1, con2 = con_pairs[i][0], con_pairs[i][1]
	pair = pair_det[i]
	eye1, eye2 = pair[0], pair[1]

	# interpupillary distance (relative to pupil width)
	w1, w2 = eye1[3][0]-eye1[2][0], eye2[3][0]-eye2[2][0]
	ave_w = (w1+w2) / 2
	dist = math.sqrt((eye2[0]-eye1[0])**2 + (eye2[1]-eye1[1])**2) / ave_w

	# get colour
	col1 = get_colour(orig, eye1[0:2], ave_w/2)
	col2 = get_colour(orig, eye2[0:2], ave_w/2)
	ave_col = ave_eye_colours(col1, col2)
	r,g,b = ave_col
	hue = get_hue(ave_col)
	
	# print results
	print("---------")
	print("NAE Pair " + str(i+1))
	print("Interpupillary distance: " + str(dist))
	print("Colour (hue): " + str(hue))
	print("Colour (RGB): " + str(ave_col))
	
	# add interpupillary distance and colour to database
	f1 = open("distcolour"+str(ID)+".csv", 'a')
	writer = csv.writer(f1)
	writer.writerow([fname,ID, dist, hue, r, g, b])
	f1.close()
	

