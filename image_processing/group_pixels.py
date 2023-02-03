import cv2
import numpy


def find_if_close(cnt1, cnt2, grouping_threshold):											# Taken from a website
	row1, row2 = cnt1.shape[0], cnt2.shape[0]
	for i in range(row1):
		for j in range(row2):
			dist = numpy.linalg.norm(cnt1[i]-cnt2[j])
			if abs(dist) < grouping_threshold:
				return True
			elif i == row1-1 and j == row2-1:
				return False


def group(image_name, grouping_threshold):								# Taken from website and modified a bit
	if image_name is None:
		return None
	img = cv2.imread(image_name)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, 127, 255, 0)
	im2, contours, heir = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 2)
	length = len(contours)
	status = numpy.zeros((length, 1))

	for i, cnt1 in enumerate(contours):
		x = i
		if i != length-1:
			for j, cnt2 in enumerate(contours[i+1:]):
				x = x+1
				dist = find_if_close(cnt1, cnt2, grouping_threshold)
				if dist:
					val = min(status[i], status[x])
					status[x] = status[i] = val
				else:
					if status[x] == status[i]:
						status[x] = i+1
	unified = []
	maximum = int(status.max())+1
	for i in range(maximum):
		pos = numpy.where(status == i)[0]
		if pos.size != 0:
			cont = numpy.vstack(contours[i] for i in pos)
			hull = cv2.convexHull(cont)
			unified.append(hull)

	cv2.drawContours(img, unified, -1, (0, 255, 0), 2)					# Marks a boundary around a cluster of white spots
	cv2.drawContours(thresh, unified, -1, 255, -1)						# Converts all the pixels inside the border into white
	cv2.imwrite(image_name[:-4]+"_grouped.png", thresh)				# save Subtracted frame as PNG file
	return image_name[:-4]+"_grouped.png"							# Returns the image's name
