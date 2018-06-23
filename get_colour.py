"""
==================================================================
AUTHOR: HIEN VU
LAST MODIFIED: 27-04-18
==================================================================
Finds the colour of eyeshine
Two functions: 
	get_colour() finds the eyeshine colour from a single eye
	ave_eye_colour() averages for the two eyes if the colours are 
	sufficiently similar
==================================================================
"""

from skimage.draw import circle

##### GET_COLOUR #####
# Get overall colour from eyeshine glow of one NAE
# Takes as input an image, centre of eye coordinates, and radius
def get_colour(image, eye, rad):
	# use skimage to draw circle and get all pixels inside it
	# circle is 1.5 times the radius of contour to obtain surrounding 'glow'
	# which is side effect of blooming from high ISO
	xx, yy = circle(eye[0], eye[1], rad*1.5)
	tot_r, tot_g, tot_b = 0, 0, 0
	numpix = len(xx)
	# get colours for pixels in the circle drawn
	for i in range(0, numpix):
		x = xx[i]
		y = yy[i]
		try:
			b,g,r = image[y,x]
			# if pixel is not white or black
			if r < 250 and g < 250 and b < 250:
				if r > 30 and g > 30 and b > 30:
					tot_r += r
					tot_g += g
					tot_b += b
		except:
			numpix -= 1
	# average out rgb values
	ave_r = tot_r / numpix
	ave_g = tot_g / numpix
	ave_b = tot_b / numpix
	return [ave_r, ave_g, ave_b]


##### AVE_EYE_COLOURS #####
# given two rgb inputs, if they are similar enough
# find the average colour of eyeshine
def ave_eye_colours(col1, col2):
	ave_col = [0, 0, 0]
	tot1, tot2 = 0, 0
	for i in range(0, 3):
		tot1 += col1[i]
		tot2 += col2[i]
	for i in range(0, 3):
		# find ratio of r, g, and b values
		rat1 = col1[i] / tot1
		rat2 = col2[i] / tot2
		# if colour ratio is sufficiently similar between two eyes
		if abs(rat1-rat2) < 0.1 :
			ave_col[i] = (col1[i]+col2[i]) / 2
		# else, eyes could be different colours
		else:
			ave_col = col1
			print("Eyes are different colours. Colour for eye1 used as average.")
	return ave_col
