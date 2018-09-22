"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""

import datetime

import cv2
import numpy as np

Recorded_Video = 'Logs/screen_record.mp4'
Final_Icon_Name = "Icons/Icon"# %d.png
Frame_Name = "Frames/Frame"
Grouping_Threshold = 15


def get_present_date_time():												# Returns a string of month_date_hr_min_sec_millsec
	now = datetime.datetime.now()
	month, date, hours, minutes, seconds, milliseconds = now.month, now.day, now.hour, now.minute, now.second, now.microsecond
	now_datetime = str(month)+"_"+str(date)+"_"+str(hours)+"_"+str(minutes)+"_"+str(seconds)+"_"+str(milliseconds)
	return now_datetime


def get_file_name(log_list):											# Returns a string containing the MainTask voice log of user
	line = [line for line in log_list if ("Main Task" in line and "Voice_U" in line)][0].split(" _|_ ")
	file_name = 'Train_Data/'+str(line[2]) + '.txt'
	return file_name


def remove_waste_mouse_logs(log_list):									# Removing Extra MouseMoved Logs
	line_no = 0
	count = 0
	word_list = []
	for line in log_list:
		if "Mouse _|_ Moved" in line:
			if count == 0:
				word_list.append(log_list[line_no]) 								# append to the list
			count += 1
		else:
			if count != 0:
				word_list.append(log_list[(line_no-1)]) 							# append to the list
			word_list.append(log_list[line_no]) 									# append to the list
			count = 0
		line_no += 1
	return word_list


def insert_icon_names(log_list, log_number, icon_name, shaped_icon_name, icon_correctness):
	if icon_name is not None:
		line = log_list[log_number]
		line = (line[:-1]+" _|_ "+icon_name+" _|_ "+shaped_icon_name+" _|_ "+icon_correctness+"\n")
		log_list[log_number] = line
		# log_list.insert(log_number+1, "Mouse _|_ Pressed _|_ "+shaped_icon_name+" _|_ "+icon_correctness+"\n")
		# log_list.insert(log_number+1, "Mouse _|_ Pressed _|_ "+icon_name+" _|_ "+icon_correctness+"\n")
		return True
	else:
		line = log_list[log_number]
		line = (line[:-1]+" _|_ None _|_ None _|_ "+icon_correctness+"\n")
		log_list[log_number] = line
		return False


def get_icon_shape(icon_name):
	if icon_name is None:
		return None
	shaped_icon_name = icon_name.split(".")
	shaped_icon_name = str(shaped_icon_name[0]) + "_shape." + str(shaped_icon_name[1])
	img = cv2.imread(icon_name, cv2.IMREAD_GRAYSCALE)
	gray1 = cv2.Canny(img, 70, 50)
	cv2.imwrite(shaped_icon_name, gray1)
	return shaped_icon_name


def crop_icon(bounding_box_coordinates, time, image_name):
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
	vidcap = cv2.VideoCapture(Recorded_Video)								# Reading Video
	vidcap.set(cv2.CAP_PROP_POS_MSEC, time)									# taking a frame at given time from video
	success, image = vidcap.read()											# Searching for frame in Video
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


def search_for_safe_time(log_list, log_number, bounding_box_coordinates):	# Searching for a time when the mouse is not in the frame
	if bounding_box_coordinates is None:
		return None
	left, top, right, bottom = bounding_box_coordinates							# Un-parsing the tuple
	for i in range(log_number, 0, -1):											# i from log_number to 0 with -1 for every loop
		# print("log_number : ",i)
		if "Mouse" in log_list[i] and "Moved" in log_list[i]:					# Searching for Mouse Moved in log_list
			(x1, y1) = (str(log_list[i].split(" _|_ ")[2])[1:-1]).split(", ")	# Taking the x,y co-ordinates from the Log
			# print(x1, y1)
			# print(left, top, right, bottom)
			if int(x1) < left or int(x1) > right or int(y1) < top or int(y1) > bottom:  	# Checking if mouse is inside of the frame or not
				safe_time = int(sum(x*int(t) for x, t in zip([3600, 60, 1, 1/1000000], log_list[i][:-1].split(" _|_ ")[3:]))*1000)
				print("Safe time : ", safe_time)								# Printing Safetime
				print("Mouse_Location at safe_time : ", x1, y1)					# Printing Mouse location at this time
				print("left, top, right, bottom :", left, top, right, bottom)	# Printing Frame Boundaries
				return safe_time												# Returning safe_time
		# else:
		# 	break


def find_bounding_box(grouped_image_name, mouse_location):				# Returns the left,top,right,bottom of the Contineous_Compoent near mouse_location
	if grouped_image_name is None:
		return None
	img = cv2.imread(grouped_image_name, 0)									# Reading Image in Black And White
	left, top, right, bottom = img.shape[:2][1], img.shape[:2][0], 0, 0		# Initilizing Variables
	ret, labels = cv2.connectedComponents(img)								# Getting Connected Components
	for i in range(1, ret):													# ret = no. of connected components in the image
		temp_array_y, temp_array_x = np.where(labels == i)						# Getting the co.ordinates into numpy arrays
		if (int(mouse_location[0]) in temp_array_x) and (int(mouse_location[1]) in temp_array_y):		# Checking if they are in arrays or not
			left = np.amin(temp_array_x)-2									# Assigning the minX to left
			right = np.amax(temp_array_x)+2									# Assigning the maxX to right
			top = np.amin(temp_array_y)-2									# Assigning the minY to top
			bottom = np.amax(temp_array_y)+2									# Assigning the maxY to bottom
			bounding_box_coordinates = left, top, right, bottom
			return bounding_box_coordinates
	bounding_box_coordinates = left, top, right, bottom
	return bounding_box_coordinates


def find_if_close(cnt1, cnt2):											# Takien from a website
	row1, row2 = cnt1.shape[0], cnt2.shape[0]
	for i in range(row1):
		for j in range(row2):
			dist = np.linalg.norm(cnt1[i]-cnt2[j])
			if abs(dist) < Grouping_Threshold:
				return True
			elif i == row1-1 and j == row2-1:
				return False


def group_dispersed_objects(image_name):								# Taken from website and modified a bit
	if image_name is None:
		return None
	img = cv2.imread(image_name)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, 127, 255, 0)
	im2, contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL, 2)
	length = len(contours)
	status = np.zeros((length, 1))

	for i, cnt1 in enumerate(contours):
		x = i
		if i != length-1:
			for j, cnt2 in enumerate(contours[i+1:]):
				x = x+1
				dist = find_if_close(cnt1, cnt2)
				if dist:
					val = min(status[i], status[x])
					status[x] = status[i] = val
				else:
					if status[x] == status[i]:
						status[x] = i+1
	unified = []
	maximum = int(status.max())+1
	for i in range(maximum):
		pos = np.where(status == i)[0]
		if pos.size != 0:
			cont = np.vstack(contours[i] for i in pos)
			hull = cv2.convexHull(cont)
			unified.append(hull)

	cv2.drawContours(img, unified, -1, (0, 255, 0), 2)					# Marks a boundry around a cluster of white spots
	cv2.drawContours(thresh, unified, -1, 255, -1)						# Converts all the pixels inside the border into white
	cv2.imwrite(image_name[:-4]+"_grouped.png", thresh)				# save Subtracted frame as PNG file
	return image_name[:-4]+"_grouped.png"							# Returns the image's name


def convert_to_bw_image(image_name):									# Converts Grey Image into Black and White
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


def getting_subtracted_frames(log_list, log_number, start_time, mouse_location):	# Find change in screen and subtract it to get only changed component
	present_time = int((sum(x * int(t) for x, t in zip([3600, 60, 1, 1/1000000], log_list[log_number][:-1].split(" _|_ ")[3:]))*1000)-start_time)
	print("Clicked at : ", mouse_location)
	print("Present Time : ", present_time+start_time, ":", present_time)
	vidcap = cv2.VideoCapture(Recorded_Video)								# Reading Video
	fps = vidcap.get(cv2.CAP_PROP_FPS)										# Getting the fps of video
	vidcap.set(cv2.CAP_PROP_POS_MSEC, present_time)						# taking a frame at given Time from video
	success, image1 = vidcap.read()											# Searching for frame in Video
	if success:																# If the frame is found in Video
		cv2.imwrite(Frame_Name+"%d.png" % present_time, image1)				# save frame as PNG file-----------------------------
		frame_time = 100													# initilizing the frame_time as 100
		while True:														# This keeps running until it gets something is the Subtracted Image
			vidcap.set(cv2.CAP_PROP_POS_MSEC, (present_time-frame_time))		# taking a frame at given Time - frame_time from video
			success, image2 = vidcap.read()									# Searching for frame in Video
			if success:														# If the frame is found in Video
				cv2.imwrite(Frame_Name+f'{int(present_time)}, ({frame_time}).png', image2)		# save frame as PNG file-----------
				image3 = image2 - image1									# subtracting the image pixel color values
				image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)
				if cv2.countNonZero(image3) == 0:							# Checking if the Image is completely black or not
					frame_time += (1000/fps)								# If Complete Black, Taking 1 frame previous to it.
				else:														# If not completely Black, then save and return Image name
					cv2.imwrite(Frame_Name+"%d(sub).png" % present_time, image3)	# save Subtracted frame as PNG file--------------
					# cv2.imwrite('Icon_Image.png', image3)					# save Subtracted frame as PNG file
					return Frame_Name + "%d(sub).png" % present_time  # Returning the image's name
			else:															# If the frame not found in video, just continue the while loop--------------------------------------------------------------------------------
				continue													# continue
	else:																	# if frame not found in video, just pass
		return None															# Returns None type when not found


def main_function():														# The Driver Code
	text_file1 = open('Logs/All_Logs.txt', 'r')					# Reading The All_Logs file
	log_list = text_file1.readlines()							# Making a List of Strings from All_Logs.txt
	text_file2_name = get_file_name(log_list)					# Getting a name for the file to save the logs in All_Logs.txt
	text_file2 = open(text_file2_name, 'w')						# Creating the file with the name of MainTask
	log_number = 0
	mouse_location = ['0', '0']

	start_time = int(sum(x * int(t) for x, t in zip([3600, 60, 1, 1/1000000], [Log for Log in log_list if "Screen_Recorder" in Log][0][:-1].split(" _|_ ")[3:]))*1000)
	print("Start Time : ", start_time)

	while len(log_list) > log_number:
		temp_mouse_location = mouse_location
		if "Mouse" in log_list[log_number] and "Pressed" in log_list[log_number] and "Mouse" in log_list[log_number + 1] and "Released" in log_list[log_number + 1]:
			mouse_location = (str(log_list[log_number].split(" _|_ ")[2])[1:-1]).split(", ")			# Getting Mouse Locations
			print(mouse_location, log_number)
			print(temp_mouse_location)
			if int(temp_mouse_location[0])+2 > int(mouse_location[0]) > int(temp_mouse_location[0])-2 and\
					int(temp_mouse_location[1]) + 2 > int(mouse_location[1]) > int(temp_mouse_location[1]) - 2:
				log_number += 1
				continue
			subtracted_image_name = getting_subtracted_frames(log_list, log_number, start_time, mouse_location)
			print(subtracted_image_name, "-------------getting_subtracted_frames")
			bw_image_name = convert_to_bw_image(subtracted_image_name)
			print(bw_image_name, "-------------convert_to_bw_image")
			grouped_image_name = group_dispersed_objects(bw_image_name)
			print(grouped_image_name, "------------group_dispersed_objects")
			bounding_box_coordinates = find_bounding_box(grouped_image_name, mouse_location)
			print(bounding_box_coordinates, "-----------find_bounding_box")
			safe_time = search_for_safe_time(log_list, log_number, bounding_box_coordinates)
			print(safe_time-start_time, "--------------search_for_safe_time")
			icon_name, icon_correctness = crop_icon(bounding_box_coordinates, (safe_time - (start_time + 200)), grouped_image_name)			# Remove start_time+200 and put actual delay of that computer
			print(icon_name, "--------------crop_icon")
			shaped_icon_name = get_icon_shape(icon_name)
			print(shaped_icon_name, "--------------get_icon_shape")
			insertion_done = insert_icon_names(log_list, log_number, icon_name, shaped_icon_name, icon_correctness)
			print(insertion_done, "--------------insert_icon_names")
		log_number += 1

	log_list = remove_waste_mouse_logs(log_list)				# Removing Moved mouse logs. we dont need all the mouse moved locations for replaying

	text_file2.writelines(log_list) 							# write words to the file

	text_file2.close() 											# don't forget to close the file
	text_file1.close() 											# don’t forget to close the file

# main_function()
