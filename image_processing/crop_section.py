import cv2
from Data import strings

Recorded_Video_Location = strings.Recorded_Video_Location
Final_Icon_Name = strings.Final_Icon_Name# %d.png
Frame_Name = strings.Frame_Name


def crop(bounding_box_coordinates, time, image_name):
	if bounding_box_coordinates is None:
		return None, None
	img = cv2.imread(image_name)
	max_x, max_y, min_x, min_y = img.shape[:2][1], img.shape[:2][0], 0, 0
	left, top, right, bottom = bounding_box_coordinates
	if right-left < 0 or bottom-top < 0:
		return None, "Icon_Not_Found"
	elif left < min_x:
		left = min_x
	elif right > max_x:
		right = max_x
	elif top < min_y:
		top = min_y
	elif bottom > max_y:
		bottom = max_y
	captured_video = cv2.VideoCapture(Recorded_Video_Location)								# Reading Video
	captured_video.set(cv2.CAP_PROP_POS_MSEC, time)									# taking a frame at given time from video
	success, image = captured_video.read()											# Searching for frame in Video
	if success:																# If the frame is found in Video
		cv2.imwrite(Frame_Name+"%d.png" % time, image)						# save frame as PNG file
		image = image[top:bottom, left:right]
		cv2.imwrite(Final_Icon_Name+"%d.png" % time, image)					# save frame as PNG file
		print("(L,T), (R,B) : (", left, top, "), (", right, bottom, ")")
		print(Final_Icon_Name+"%d.png" % time)
	if right-left < 2 and bottom-top < 2:
		print("----------------------------------------------Tiny_Icon")
		return (Final_Icon_Name+"%d.png" % time), "Tiny_Icon"
	else:
		print("----------------------------------------------")
		return (Final_Icon_Name+"%d.png" % time), "Perfect"
