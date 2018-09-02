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


def get_file_name(Log_list):											# Returns a string containing the MainTask voice log of user
	line = [line for line in Log_list if ("Main Task" in line and "Voice_U" in line)][0].split(" _|_ ")
	file_name = 'Train_Data/'+str(line[2]) + '.txt'
	return file_name


def remove_waste_mouse_logs(Log_list):									# Removing Extra MouseMoved Logs
	line_no	= 0
	count	= 0
	word_list	= []
	for line in Log_list:
		if("Mouse _|_ Moved" in line):
			if(count==0):
				word_list.append(Log_list[line_no]) 								# append to the list
			count+=1
		else:
			if(count!=0):
				word_list.append(Log_list[(line_no-1)]) 							# append to the list
			word_list.append(Log_list[line_no]) 									# append to the list
			count=0
		line_no+=1
	return word_list


def insert_icon_names(Log_list, Log_Number, Icon_Name, Shaped_Icon_Name, Icon_Correctness):
	if(Icon_Name != None):
		line = Log_list[Log_Number]
		line = (line[:-1]+" _|_ "+Icon_Name+" _|_ "+Shaped_Icon_Name+" _|_ "+Icon_Correctness+"\n")
		Log_list[Log_Number] = line
		# Log_list.insert(Log_Number+1, "Mouse _|_ Pressed _|_ "+Shaped_Icon_Name+" _|_ "+Icon_Correctness+"\n")
		# Log_list.insert(Log_Number+1, "Mouse _|_ Pressed _|_ "+Icon_Name+" _|_ "+Icon_Correctness+"\n")
		return True
	else:
		line = Log_list[Log_Number]
		line = (line[:-1]+" _|_ None _|_ None _|_ "+Icon_Correctness+"\n")
		Log_list[Log_Number] = line
		return False


def get_icon_shape(Icon_Name):
	if(Icon_Name == None):
		return None
	Shaped_Icon_Name = Icon_Name.split(".")
	Shaped_Icon_Name = str(Shaped_Icon_Name[0]) + "_shape." + str(Shaped_Icon_Name[1])
	img = cv2.imread(Icon_Name, cv2.IMREAD_GRAYSCALE)
	gray1 = cv2.Canny(img, 70, 50)
	cv2.imwrite(Shaped_Icon_Name, gray1)
	return Shaped_Icon_Name


def crop_icon(Bounding_Box_Coordinates, Time, Image_Name):
	if(Bounding_Box_Coordinates == None):
		return None, None
	img = cv2.imread(Image_Name)
	MaxX, MaxY, MinX, MinY = img.shape[:2][1], img.shape[:2][0], 0, 0
	Left, Top, Right, Bottom = Bounding_Box_Coordinates
	if(Right-Left<0 or Bottom-Top<0):
		return None, "Icon_Not_Found"
	elif(Left<MinX):	Left = MinX
	elif(Right>MaxX):	Right = MaxX
	elif(Top<MinY):		Top = MinY
	elif(Bottom>MaxY):	Bottom = MaxY
	vidcap = cv2.VideoCapture(Recorded_Video)								# Reading Video
	vidcap.set(cv2.CAP_PROP_POS_MSEC,Time)									# taking a frame at given Time from video
	success,image = vidcap.read()											# Searching for frame in Video
	if success:																# If the frame is found in Video
		cv2.imwrite(Frame_Name+"%d.png" % Time, image)						# save frame as PNG file
		image = image[Top:Bottom, Left:Right]
		cv2.imwrite(Final_Icon_Name+"%d.png" % Time, image)					# save frame as PNG file
		print("(L,T), (R,B) : (",Left, Top,"), (",Right, Bottom,")")
		print(Final_Icon_Name+"%d.png" % Time)
	if(Right-Left<2 and Bottom-Top<2):
		print("----------------------------------------------Tiny_Icon")
		return (Final_Icon_Name+"%d.png" % Time), "Tiny_Icon"
	else:
		print("----------------------------------------------")
		return (Final_Icon_Name+"%d.png" % Time), "Perfect"


def search_for_safe_time(Log_list, Log_Number, Bounding_Box_Coordinates):	# Searching for a time when the mouse is not in the frame
	if(Bounding_Box_Coordinates == None):
		return None
	Left, Top, Right, Bottom = Bounding_Box_Coordinates							# Un-parsing the tuple
	Safe_Time = int(sum(x*int(t) for x, t in zip([3600, 60, 1, 1/1000000], Log_list[Log_Number][:-1].split(" _|_ ")[3:]))*1000)
	for i in range(Log_Number, 0, -1):											# i from Log_Number to 0 with -1 for every loop
		# print("Log_Number : ",i)
		if("Mouse" in Log_list[i] and "Moved" in Log_list[i]):					# Searching for Mouse Moved in Log_list
			(x1, y1) = (str(Log_list[i].split(" _|_ ")[2])[1:-1]).split(", ")	# Taking the x,y co-ordinates from the Log
			# print(x1, y1)
			# print(Left, Top, Right, Bottom)
			if(int(x1)<Left or int(x1)>Right or int(y1)<Top or int(y1)>Bottom):	# Checking if mouse is inside of the frame or not
				Safe_Time = int(sum(x*int(t) for x, t in zip([3600, 60, 1, 1/1000000], Log_list[i][:-1].split(" _|_ ")[3:]))*1000)
				print("Safe time : ", Safe_Time)								# Printing Safetime
				print("Mouse_Location at Safe_Time : ", x1,y1)					# Printing Mouse location at this time
				print("Left, Top, Right, Bottom :", Left, Top, Right, Bottom)	# Printing Frame Boundries
				return Safe_Time												# Returning Safe_Time
		# else:
		# 	break


def Find_Bounding_Box(Grouped_Image_Name, Mouse_Location):				# Returns the Left,Top,Right,Bottom of the Contineous_Compoent near Mouse_Location
	if(Grouped_Image_Name == None):
		return None
	img = cv2.imread(Grouped_Image_Name, 0)									# Reading Image in Black And White
	Left, Top, Right, Bottom = img.shape[:2][1], img.shape[:2][0], 0, 0		# Initilizing Variables
	ret, labels = cv2.connectedComponents(img)								# Getting Connected Components
	for i in range(1, ret):													# ret = no. of connected components in the image
		TempArrayY, TempArrayX = np.where(labels == i)						# Getting the co.ordinates into numpy arrays
		if (int(Mouse_Location[0]) in TempArrayX) and (int(Mouse_Location[1]) in TempArrayY):		# Checking if they are in arrays or not
			Left	= np.amin(TempArrayX)-2									# Assigning the minX to Left
			Right	= np.amax(TempArrayX)+2									# Assigning the maxX to Right
			Top		= np.amin(TempArrayY)-2									# Assigning the minY to Top
			Bottom	= np.amax(TempArrayY)+2									# Assigning the maxY to Bottom
			Bounding_Box_Coordinates = Left, Top, Right, Bottom
			return Bounding_Box_Coordinates
	Bounding_Box_Coordinates = Left, Top, Right, Bottom
	return Bounding_Box_Coordinates


def Find_If_Close(cnt1,cnt2):											# Takien from a website
	row1,row2 = cnt1.shape[0],cnt2.shape[0]
	for i in range(row1):
		for j in range(row2):
			dist = np.linalg.norm(cnt1[i]-cnt2[j])
			if abs(dist) < Grouping_Threshold :
				return True
			elif i==row1-1 and j==row2-1:
				return False


def Group_Dispersed_Objects(Image_Name):								# Taken from website and modified a bit
	if(Image_Name == None):
		return None
	img = cv2.imread(Image_Name)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(gray,127,255,0)
	im2,contours,hier = cv2.findContours(thresh,cv2.RETR_EXTERNAL,2)
	LENGTH = len(contours)
	status = np.zeros((LENGTH,1))

	for i,cnt1 in enumerate(contours):
		x = i
		if i != LENGTH-1:
			for j,cnt2 in enumerate(contours[i+1:]):
				x = x+1
				dist = Find_If_Close(cnt1,cnt2)
				if dist == True:
					val = min(status[i],status[x])
					status[x] = status[i] = val
				else:
					if status[x]==status[i]:
						status[x] = i+1
	unified = []
	maximum = int(status.max())+1
	for i in range(maximum):
		pos = np.where(status==i)[0]
		if pos.size != 0:
			cont = np.vstack(contours[i] for i in pos)
			hull = cv2.convexHull(cont)
			unified.append(hull)

	cv2.drawContours(img,unified,-1,(0,255,0),2)					# Marks a boundry around a cluster of white spots
	cv2.drawContours(thresh,unified,-1,255,-1)						# Converts all the pixels inside the border into white
	cv2.imwrite(Image_Name[:-4]+"_grouped.png", thresh)				# save Subtracted frame as PNG file
	return Image_Name[:-4]+"_grouped.png"							# Returns the image's name


def convert_to_bw_image(Image_Name):									# Converts Grey Image into Black and White
	if(Image_Name == None):
		return None
	img = cv2.imread(Image_Name, 0)								# Readig Image using cv2
	height, width = img.shape
	# pixel = im.load()											# Loading Image pixels into 'pixel'
	for i in range(height):										# Assigning X values of image to i
		for j in range(width):									# Assigning Y values of image to j
			if(img[i, j] != 0):									# checking if that pixel is Black or not
				img[i, j] = 255									# If not Black, Make it pure White
			else:												# Jut pass if it's a black pixel
				pass											# pass
	cv2.imwrite(Image_Name,img)									# Saving the image
	return (Image_Name)											# Returning the Image's Name


def getting_subtracted_frames(Log_list, Log_Number, Start_Time, Mouse_Location):	# Find change in screen and subtract it to get only changed component
	Present_Time = int((sum(x * int(t) for x, t in zip([3600, 60, 1, 1/1000000], Log_list[Log_Number][:-1].split(" _|_ ")[3:]))*1000)-Start_Time)
	print("Clicked at : ", Mouse_Location)
	print("Present Time : ", Present_Time+Start_Time, ":",Present_Time)
	vidcap = cv2.VideoCapture(Recorded_Video)								# Reading Video
	fps = vidcap.get(cv2.CAP_PROP_FPS)										# Getting the fps of video
	vidcap.set(cv2.CAP_PROP_POS_MSEC, (Present_Time))						# taking a frame at given Time from video
	success,image1 = vidcap.read()											# Searching for frame in Video
	if success:																# If the frame is found in Video
		cv2.imwrite(Frame_Name+"%d.png" % Present_Time, image1)				# save frame as PNG file-----------------------------
		Frame_Time = 100													# initilizing the Frame_Time as 100
		while(True):														# This keeps running until it gets something is the Subtracted Image
			vidcap.set(cv2.CAP_PROP_POS_MSEC,(Present_Time-Frame_Time))		# taking a frame at given Time - Frame_Time from video
			success,image2 = vidcap.read()									# Searching for frame in Video
			if success:														# If the frame is found in Video
				cv2.imwrite(Frame_Name+f'{int(Present_Time)}, ({Frame_Time}).png', image2)		# save frame as PNG file-----------
				image3 = image2 - image1									# subtracting the image pixel color values
				image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)
				if (cv2.countNonZero(image3) == 0):							# Checking if the Image is completely black or not
					Frame_Time += (1000/fps)								# If Complete Black, Taking 1 frame previous to it.
				else:														# If not completely Black, then save and return Image name
					cv2.imwrite(Frame_Name+"%d(sub).png" % Present_Time, image3)	# save Subtracted frame as PNG file--------------
					# cv2.imwrite('Icon_Image.png', image3)					# save Subtracted frame as PNG file
					return (Frame_Name+"%d(sub).png" % Present_Time)		# Returning the image's name
			else:															# If the frame not found in video, just continue the while loop--------------------------------------------------------------------------------
				continue													# continue
	else:																	# if frame not found in video, just pass
		return None															# Returns None type when not found


def main_function():														# The Driver Code
	datetime = get_present_date_time()
	text_file2_name = 'Train_Data/Unknown_'+datetime+'.txt'		# Giving a default file name with date and time
	text_file1 = open('Logs/All_Logs.txt','r')					# Reading The All_Logs file
	log_list = text_file1.readlines();							# Making a List of Strings from All_Logs.txt
	text_file2_name = get_file_name(log_list)					# Getting a name for the file to save the logs in All_Logs.txt
	text_file2 = open(text_file2_name,'w')						# Creating the file with the name of MainTask
	Log_Number = 0
	Mouse_Location = ['0','0']

	Start_Time = int(sum(x * int(t) for x, t in zip([3600, 60, 1, 1/1000000], [Log for Log in log_list if "Screen_Recorder" in Log][0][:-1].split(" _|_ ")[3:]))*1000)
	print("Start Time : ", Start_Time)

	while(len(log_list) > Log_Number):
		Temp_Mouse_Location = Mouse_Location
		if("Mouse" in log_list[Log_Number] and "Pressed" in log_list[Log_Number] and "Mouse" in log_list[Log_Number+1] and "Released" in log_list[Log_Number+1]):
			Mouse_Location = (str(log_list[Log_Number].split(" _|_ ")[2])[1:-1]).split(", ")			# Getting Mouse Locations
			print(Mouse_Location , Log_Number)
			print(Temp_Mouse_Location)
			if(int(Mouse_Location[0])<int(Temp_Mouse_Location[0])+2 and int(Mouse_Location[0])>int(Temp_Mouse_Location[0])-2 and int(Mouse_Location[1])<int(Temp_Mouse_Location[1])+2 and int(Mouse_Location[1])>int(Temp_Mouse_Location[1])-2):
				Log_Number+=1
				continue
			Subtracted_Image_Name = getting_subtracted_frames(log_list, Log_Number, Start_Time, Mouse_Location)
			print(Subtracted_Image_Name, "-------------getting_subtracted_frames")
			BW_Image_Name = convert_to_bw_image(Subtracted_Image_Name)
			print(BW_Image_Name, "-------------convert_to_bw_image")
			Grouped_Image_Name = Group_Dispersed_Objects(BW_Image_Name)
			print(Grouped_Image_Name, "------------Group_Dispersed_Objects")
			Bounding_Box_Coordinates = Find_Bounding_Box(Grouped_Image_Name, Mouse_Location)
			print(Bounding_Box_Coordinates, "-----------Find_Bounding_Box")
			Safe_Time = search_for_safe_time(log_list, Log_Number, Bounding_Box_Coordinates)
			print(Safe_Time-Start_Time, "--------------search_for_safe_time")
			Icon_Name, Icon_Correctness = crop_icon(Bounding_Box_Coordinates, (Safe_Time - (Start_Time + 200)), Grouped_Image_Name)			# Remove Start_Time+200 and put actual delay of that computer
			print(Icon_Name, "--------------crop_icon")
			Shaped_Icon_Name = get_icon_shape(Icon_Name)
			print(Shaped_Icon_Name, "--------------get_icon_shape")
			Insertion_Done = insert_icon_names(log_list, Log_Number, Icon_Name, Shaped_Icon_Name, Icon_Correctness)
			print(Insertion_Done, "--------------insert_icon_names")
		Log_Number+=1

	log_list = remove_waste_mouse_logs(log_list)				# Removing Moved mouse logs. we dont need all the mouse moved locations for replaying

	text_file2.writelines(log_list) 							# write words to the file

	text_file2.close() 											# don't forget to close the file
	text_file1.close() 											# don’t forget to close the file

# main_function()
