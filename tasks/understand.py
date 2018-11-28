"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""

import datetime
from Data import strings
from image_processing import get_action_frames, to_Black_n_White, group_pixels, crop_section, draw_shape, get_group_size
from database_manager import insert_icon_name, remove_unwanted_mouse_logs, search_for_safe_time

Recorded_Video_Location = strings.Recorded_Video_Location
Final_Icon_Name = strings.Final_Icon_Name # %d.png
Frame_Name = strings.Frame_Name
All_Log_File_Name = strings.All_Log_File_Name
Grouping_Threshold = 15


def get_present_date_time():												# Returns a string of month_date_hr_min_sec_millsec
	now = datetime.datetime.now()
	month, date, hours, minutes, seconds, milliseconds = now.month, now.day, now.hour, now.minute, now.second, now.microsecond
	now_datetime = str(month)+"_"+str(date)+"_"+str(hours)+"_"+str(minutes)+"_"+str(seconds)+"_"+str(milliseconds)
	return now_datetime


def get_file_name(log_list):											# Returns a string containing the MainTask voice log of user
	line = [line for line in log_list if ("Main Task" in line and "Voice_U" in line)][0].split(" _|_ ")
	file_name = strings.Train_Data_Location
	file_name = file_name + str(line[2]) + '.txt'
	return file_name


def main_function():														# The Driver Code
	text_file1 = open(All_Log_File_Name, 'r')					# Reading The All_Logs file
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
			bw_image_name = to_Black_n_White.convert(subtracted_image_name)
			print(bw_image_name, "-------------convert_to_bw_image")
			grouped_image_name = group_pixels.group(bw_image_name, Grouping_Threshold)
			print(grouped_image_name, "------------group_dispersed_objects")
			bounding_box_coordinates = get_group_size.size(grouped_image_name, mouse_location)
			print(bounding_box_coordinates, "-----------get_group_size")
			safe_time = search_for_safe_time.search(log_list, log_number, bounding_box_coordinates)
			print(safe_time-start_time, "--------------search_for_safe_time")
			icon_name, icon_correctness = crop_section.crop(bounding_box_coordinates, (safe_time - (start_time + 200)), grouped_image_name)			# Remove start_time+200 and put actual delay of that computer
			print(icon_name, "--------------crop_icon")
			shaped_icon_name = draw_shape.get_shape(icon_name)
			print(shaped_icon_name, "--------------get_icon_shape")
			insertion_done = insert_icon_name.insert(log_list, log_number, icon_name, shaped_icon_name, icon_correctness)
			print(insertion_done, "--------------insert")
		log_number += 1

	log_list = remove_unwanted_mouse_logs.remove(log_list)				# Removing Moved mouse logs. we don't need all the mouse moved locations for replaying

	text_file2.writelines(log_list) 							# write words to the file

	text_file2.close() 											# don't forget to close the file
	text_file1.close() 											# don’t forget to close the file

# search()
