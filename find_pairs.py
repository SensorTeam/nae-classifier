"""
==================================================================
AUTHOR: HIEN VU
LAST MODIFIED: 27-04-18
==================================================================
Refines contours by finding ones that are matched with pairs, using 
signal duality and signal orientation
Takes as input an image and its respective contours from find_eye.py
Returns pair contours and array of details for each pair
==================================================================
"""

import cv2
import numpy as np 
import math

# find pairs
def find_pairs(image, cnts):
	pair_det = []
	con_det = []
	con_pairs = []
	for con in cnts:
		(x, y) = find_centre(con)
		extL = tuple(con[con[:,:,0].argmin()][0])
		extR = tuple(con[con[:,:,0].argmax()][0])
		extT = tuple(con[con[:,:,1].argmin()][0])
		extB = tuple(con[con[:,:,1].argmax()][0])
		con_det.append([x, y, extL, extR, extT, extB])
	# compare with every contour after itself
	for i in range(0, len(cnts)-1):
		con1 = con_det[i]
		x1 = con1[0]
		y1 = con1[1]
		w1 = con1[3][0]-con1[2][0]
		h1 = con1[5][1]-con1[4][1]
		for j in range(i+1, len(cnts)):
			con2 = con_det[j]
			x2 = con2[0]
			y2 = con2[1]
			w2 = con2[3][0]-con2[2][0]
			h2 = con2[5][1]-con2[4][1]
			# same height and width (within 1.7)
			if 0.59*w2 < w1 < 1.7*w2 and 0.59*h2 < h1 < 1.7*h2:
				# angle of orientation < 30 deg
				if x2 == x1:
					pass
				else:
					theta = math.degrees(math.atan((y2-y1) / (x2-x1)))
					if -30 < theta < 30:
						# x not more than 7 times the average eye width across
						maxdist = (w1+w2) / 2 * 14
						if abs(x2-x1) < maxdist:
							# add eyes to list of pairs
							if x1 < x2:
								pair_det.append([con_det[i], con_det[j]])
								con_pairs.append([cnts[i], cnts[j]])
							else:
								pair_det.append([con_det[j], con_det[i]])
								con_pairs.append([cnts[j], cnts[i]])
	pairs = [con_pairs, pair_det]
	return pairs

# find the approximate centre of each shape 
# using centre of contour ave w/ brightest pixels
def find_centre(con):
	M = cv2.moments(con)
	x = int(M["m10"] / M["m00"])
	y = int(M["m01"] / M["m00"])
	# find brightest pixels in the contour and average x and y values
	# average those with centre of contour
	return (x, y)
