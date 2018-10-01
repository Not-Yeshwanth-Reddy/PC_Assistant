def insert(log_list, log_number, icon_name, shaped_icon_name, icon_correctness):
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
