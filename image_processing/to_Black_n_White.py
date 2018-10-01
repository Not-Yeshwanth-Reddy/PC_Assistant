import cv2


def convert(image_name):									# Converts Grey Image into Black and White
	if image_name is None:
		return None
	img = cv2.imread(image_name, 0)								# Readig Image using cv2
	height, width = img.shape
	# pixel = im.load()											# Loading Image pixels into 'pixel'
	for i in range(height):										# Assigning X values of image to i
		for j in range(width):									# Assigning Y values of image to j
			if img[i, j] != 0:									# checking if that pixel is Black or not
				img[i, j] = 255									# If not Black, Make it pure White
			else:												# Jut pass if it's a black pixel
				pass											# pass
	cv2.imwrite(image_name, img)								# Saving the image
	return image_name											# Returning the Image's Name
