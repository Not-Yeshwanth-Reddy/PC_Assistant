# """
# Template Finding algorithm using 6 different methods.
# Finds the given template on the screen. (from the ScreenShot)
# """
import numpy
import cv2
import pyautogui
from matplotlib import pyplot as plt
from Data import strings

# Sample data -
# > Log_list = ["Mouse _|_ Moved _|_ (1214, 587) _|_ 11 _|_ 50 _|_ 47 _|_ 779491", "Mouse _|_ Pressed.Button.right _|_ (1312, 708) _|_ 11 _|_ 50 _|_ 45 _|_ 662823 _|_ None _|_ None _|_ Icon_Not_Found", "Mouse _|_ Pressed.Button.left _|_ (1214, 591) _|_ 11 _|_ 50 _|_ 48 _|_ 328612 _|_ Icons/Icon26969.png _|_ Icons/Icon16620_shape.png _|_ Perfect"]
# > Log_Number = 2
# This code gives boundaries of the template from screen shot.

Temp_png_file = strings.Temp_png_file


def search(log_list, log_number):
	left = []
	right = []
	top = []
	bottom = []
	template_name = (log_list[log_number]).split(" _|_ ")[7]
	template = cv2.imread(template_name, 0)
	pyautogui.screenshot(Temp_png_file)
	img = cv2.imread(Temp_png_file, 0)
	img2 = img.copy()
	w, h = template.shape[::-1]

	# All the 6 methods for comparison in a list
	methods = ['cv2.TM_CCOEFF', 'cv2.TM_SQDIFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF_NORMED']

	for method in methods:
		img = img2.copy()
		method = eval(method)

		# Apply template Matching
		res = cv2.matchTemplate(img, template, method)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

		# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
		if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
			top_left = min_loc
		else:
			top_left = max_loc
		bottom_right = (top_left[0] + w, top_left[1] + h)

		cv2.rectangle(img, top_left, bottom_right, 255, 2)
		# print(top_left, bottom_right)
		left.append(top_left[0])
		top.append(top_left[1])
		right.append(bottom_right[0])
		bottom.append(bottom_right[1])
		plt.subplot(121), plt.imshow(res, cmap='gray')
		plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
		plt.subplot(122), plt.imshow(img, cmap='gray')
		plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
		plt.suptitle(method)
	
	left = numpy.bincount(left).argmax()						# Getting the most frequent element in the array
	top = numpy.bincount(top).argmax()							# Getting the most frequent element in the array
	right = numpy.bincount(right).argmax()						# Getting the most frequent element in the array
	bottom = numpy.bincount(bottom).argmax()					# Getting the most frequent element in the array
	# print("left : ", left)
	# print("top : ", top)
	# print("right : ", right)
	# print("bottom : ", bottom)
	icon_location = ((left[0], top[0]), (right[0], bottom[0]))
	if left[1] >= 4 or right[1] >= 4 or top[1] >= 4 or bottom[1] >= 4:
		return icon_location, True
	else:
		return icon_location, False

# Icon_Location, Found =  search(Log_list, Log_Number)
# print(Icon_Location, Found)
