def search(log_list, log_number, bounding_box_coordinates):	# Searching for a time when the mouse is not in the frame
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
				print("Safe time : ", safe_time)								# Printing Safe time
				print("Mouse_Location at safe_time : ", x1, y1)					# Printing Mouse location at this time
				print("left, top, right, bottom :", left, top, right, bottom)	# Printing Frame Boundaries
				return safe_time												# Returning safe_time
		# else:
		# 	break
