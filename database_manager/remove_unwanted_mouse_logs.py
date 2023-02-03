def remove(log_list):									# Removing Extra MouseMoved Logs
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
