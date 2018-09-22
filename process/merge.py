"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""
from operator import itemgetter


def main_function():
	# open the file
	text_file1 = open('Logs/Key_Logs.txt','r')
	text_file2 = open('Logs/Voice_Logs.txt','r')
	text_file3 = open('Logs/Mouse_Logs.txt','r')
	temp_file = open('Logs/temp.txt','w')
	output = open("Logs/All_Logs.txt", 'w')

	# initialize an empty list
	temp_list= []

	# get the list of line
	line_list1 = text_file1.readlines()
	line_list2 = text_file2.readlines()
	line_list3 = text_file3.readlines()

	# for each line from the list, print the line
	for line in line_list3:
		# print(line)
		temp_list.append(line) #append to the list

	for line in line_list2:
		# print(line)
		temp_list.append(line) #append to the list

	for line in line_list1:
		# print(line)
		temp_list.append(line) #append to the list

	temp_file.writelines(temp_list) #write words to the file

	# temp_file.close() #don't forget to close the file
	text_file3.close() #don't forget to close the file
	text_file2.close() #don't forget to close the file
	text_file1.close() #don’t forget to close the file
	temp_file.close() #don’t forget to close the file

	lines = []

	for line in temp_list:

		line = line.split(' _|_ ')

		if int(line[3])<10:
			line[3] = "0" + line[3]

		if int(line[4])<10:
			line[4] = "0" + line[4]

		if int(line[5])<10:
			line[5] = "0" + line[5]

		if int(line[6])<100000:
			for var in range(7-len(line[6])):
				line[6] = "0" + line[6]

		lines.append(line)
	for line in sorted(lines, key = itemgetter(3, 4, 5, 6)):
		output.write(' _|_ '.join(line))

	output.close() #don’t forget to close the file


# main_function()
