import cv2
import numpy


def size(grouped_image_name, mouse_location):				# Returns the left,top,right,bottom of the Contineous_Compoent near mouse_location
	if grouped_image_name is None:
		return None
	img = cv2.imread(grouped_image_name, 0)									# Reading Image in Black And White
	left, top, right, bottom = img.shape[:2][1], img.shape[:2][0], 0, 0		# Initialising Variables
	ret, labels = cv2.connectedComponents(img)								# Getting Connected Components
	for i in range(1, ret):													# ret = no. of connected components in the image
		temp_array_y, temp_array_x = numpy.where(labels == i)						# Getting the co.ordinates into numpy arrays
		if (int(mouse_location[0]) in temp_array_x) and (int(mouse_location[1]) in temp_array_y):		# Checking if they are in arrays or not
			left = numpy.amin(temp_array_x)-2									# Assigning the minX to left
			right = numpy.amax(temp_array_x)+2									# Assigning the maxX to right
			top = numpy.amin(temp_array_y)-2									# Assigning the minY to top
			bottom = numpy.amax(temp_array_y)+2									# Assigning the maxY to bottom
			bounding_box_coordinates = left, top, right, bottom
			return bounding_box_coordinates
	bounding_box_coordinates = left, top, right, bottom
	return bounding_box_coordinates
