import cv2

Frame_Name = "Frames/Frame"
Recorded_Video = "Logs/screen_record.mp4"


def get_frames(log_list, log_number, start_time, mouse_location):							# Find change in screen and subtract it to get only changed component
	present_time = int((sum(x * int(t) for x, t in zip([3600, 60, 1, 1 / 1000000], log_list[log_number][:-1].split(" _|_ ")[3:])) * 1000) - start_time)
	print("Clicked at : ", mouse_location)
	print("Present Time : ", present_time + start_time, ":", present_time)
	captured_video = cv2.VideoCapture(Recorded_Video)										# Reading Video
	fps = captured_video.get(cv2.CAP_PROP_FPS)												# Getting the fps of video
	captured_video.set(cv2.CAP_PROP_POS_MSEC, present_time)									# taking a frame at given Time from video
	success, image1 = captured_video.read()													# Searching for frame in Video
	if success:																		# If the frame is found in Video
		cv2.imwrite(Frame_Name + "%d.png" % present_time, image1)					# save frame as PNG file-----------------------------
		frame_time = 100															# initialising the frame_time as 100
		while True:																	# This keeps running until it gets something is the Subtracted Image
			captured_video.set(cv2.CAP_PROP_POS_MSEC, (present_time - frame_time))			# taking a frame at given Time - frame_time from video
			success, image2 = captured_video.read()											# Searching for frame in Video
			if success:  # If the frame is found in Video
				cv2.imwrite(Frame_Name + f'{int(present_time)}, ({frame_time}).png',
							image2)  # save frame as PNG file-----------
				image3 = image2 - image1  # subtracting the image pixel color values
				image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)
				if cv2.countNonZero(image3) == 0:  # Checking if the Image is completely black or not
					frame_time += (1000 / fps)  # If Complete Black, Taking 1 frame previous to it.
				else:  # If not completely Black, then save and return Image name
					cv2.imwrite(Frame_Name + "%d(sub).png" % present_time,
								image3)  # save Subtracted frame as PNG file--------------
					# cv2.imwrite('Icon_Image.png', image3)					# save Subtracted frame as PNG file
					return Frame_Name + "%d(sub).png" % present_time  # Returning the image's name
			else:  # If the frame not found in video, just continue the while loop--------------------------------------------------------------------------------
				continue  # continue
	else:  # if frame not found in video, just pass
		return None  # Returns None type when not found
