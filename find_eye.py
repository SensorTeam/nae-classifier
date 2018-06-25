"""
==================================================================
AUTHOR: HIEN VU
LAST MODIFIED: 14-04-18
==================================================================
Locates potential eyeshine signals from an image
Finding potential eye signals from a .jpg by finding bright spots 
in the image. Does not take into account signal duality or orientation.

Modified from PyImageSearch, Rosebreck A. Original code available at
https://www.pyimagesearch.com/2016/10/31/detecting-multiple-bright-spots-in-an-image-with-python-and-opencv/ 
==================================================================
"""

from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
import math

####### SET MACROS ####

GRADIUS = 1		# gaussian blur radius, must be odd

THRESH = 220		# minimum brightness

MINAREA = 10			# refine mask sizes
MAXAREA = 30000

MINCIRCULARITY = 0.6		# between 0 and 1

MAXRADIUS = 3000		# max eye radius

#######################


# Returns list of contours refined by size, circularity, and radius
def mask_circles(contours):
	contours_area = []
	contours_circles = []
	contours_radius = []
	# find contours of correct area
	for con in contours:
		area = cv2.contourArea(con)
		if MINAREA < area < MAXAREA:
			contours_area.append(con)
		
			# find contours of sufficient circularity
			perimeter = cv2.arcLength(con, True)
			if perimeter == 0:
				break
			circularity = 4*math.pi*(area/(perimeter*perimeter))
			if MINCIRCULARITY < circularity < 1.0:
				contours_circles.append(con)
				
				# find contours of smaller radius			
				(x, y), radius = cv2.minEnclosingCircle(con)
				if radius < MAXRADIUS:
					contours_radius.append(con)
					
	return contours_radius


# Returns final contours of potential eye signals
def find_eye(image):
	 
	# make a copy of the image and convert it to grayscale
	orig = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# apply a Gaussian blur to the image then find the brightest region
	blurred = cv2.GaussianBlur(gray, (GRADIUS, GRADIUS), 0)

	# threshold the image to reveal light regions in the blurred image
	# any pixel with brightness greater than THRESH is set to white, everything else set to black
	thresh = cv2.threshold(gray, THRESH, 255, cv2.THRESH_BINARY)[1]

	"""
	# erode and dilate to remove noise
	thresh = cv2.erode(thresh, None, iterations=2)
	thresh = cv2.dilate(thresh, None, iterations=4)
	"""

	# connected component analysis
	# mask stores "large" components
	labels = measure.label(thresh, neighbors=8, background=0)
	mask = np.zeros(thresh.shape, dtype="uint8")

	for label in np.unique(labels):
		# if label is background, ignore
		if label == 0:
			continue
		# else construct label mask and count pixels
		labelMask = np.zeros(thresh.shape, dtype="uint8")
		labelMask[labels == label] = 255
		numPixels = cv2.countNonZero(labelMask)
		mask = cv2.add(mask, labelMask)

	# find contours
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	cnts_final = mask_circles(cnts)

	return cnts_final