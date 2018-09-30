"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""

import datetime
from Image_Processing import get_action_frames, convert_to_bw, group_pixels, crop_section, draw_shape, get_group_size


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
			if int(temp_mouse_location[0])+2 > int(mouse_location[0]) > int(temp_mouse_location[0])-2 and int(temp_mouse_location[1]) + 2 > int(mouse_location[1]) > int(temp_mouse_location[1]) - 2:
				log_number += 1
				continue
			subtracted_image_name = get_action_frames.get_frames(log_list, log_number, start_time, mouse_location)
			print(subtracted_image_name, "-------------getting_subtracted_frames")
			bw_image_name = convert_to_bw.convert(subtracted_image_name)
			print(bw_image_name, "-------------convert_to_bw_image")
			grouped_image_name = group_pixels.group(bw_image_name, Grouping_Threshold)
			print(grouped_image_name, "------------group_dispersed_objects")
			bounding_box_coordinates = get_group_size.size(grouped_image_name, mouse_location)
			print(bounding_box_coordinates, "-----------get_group_size")
			safe_time = search_for_safe_time(log_list, log_number, bounding_box_coordinates)
			print(safe_time-start_time, "--------------search_for_safe_time")
			icon_name, icon_correctness = crop_section.crop(bounding_box_coordinates, (safe_time - (start_time + 200)), grouped_image_name)			# Remove start_time+200 and put actual delay of that computer
			print(icon_name, "--------------crop_icon")
			shaped_icon_name = draw_shape.get_shape(icon_name)
			print(shaped_icon_name, "--------------get_icon_shape")
			insertion_done = insert_icon_names(log_list, log_number, icon_name, shaped_icon_name, icon_correctness)
			print(insertion_done, "--------------insert_icon_names")
		log_number += 1

	log_list = remove_waste_mouse_logs(log_list)				# Removing Moved mouse logs. we dont need all the mouse moved locations for replaying

	text_file2.writelines(log_list) 							# write words to the file

	text_file2.close() 											# don't forget to close the file
	text_file1.close() 											# don’t forget to close the file

# main_function()
