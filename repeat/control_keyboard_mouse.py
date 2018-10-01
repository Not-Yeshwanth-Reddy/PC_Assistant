"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""
import time

from dynamic_typing import dynamic_typing
from image_processing import template_search
import pyautogui

Temp_Log_File_Name = 'Logs/temp.txt'
Duration = 0.3


def key_press(log_list, log_number):					# This Function presses the key on the keyboard.
	line = log_list[log_number]
	key = (str(line.split(" _|_ ")[2]))
	if "'" in key:
		key = key[1:-1]
		pyautogui.keyDown(key)
		# print("pressed - ",key)
	elif "Key.cmd" in line:
		pyautogui.keyDown('winleft')
	elif "Key" in key:
		key = key.split(".")[1]
		pyautogui.keyDown(key)
		# print("KeyDown : "+key)
	else:
		if "Key.home" in line:
			pyautogui.keyDown('home')
		elif "Key.backspace" in line:
			pyautogui.keyDown('backspace')
		elif "Key.space" in line:
			pyautogui.keyDown('space')
		elif "Key.tab" in line:
			pyautogui.keyDown('tab')
		elif "Key.enter" in line:
			pyautogui.keyDown('enter')
		elif "Key.alt" in line:
			pyautogui.keyDown('alt')
		elif "Key.ctrl" in line:
			pyautogui.keyDown('ctrl')
		elif "Key.shift" in line:
			pyautogui.keyDown('shift')
		elif "Key.up" in line:
			pyautogui.keyDown('up')
		elif "Key.down" in line:
			pyautogui.keyDown('down')
		elif "Key.left" in line:
			pyautogui.keyDown('left')
		elif "Key.right" in line:
			pyautogui.keyDown('right')
		else:
			pass
			# key = (str(line.split(" _|_ ")[2]))
			# print("Unknown value - ",key)


def key_release(log_list, log_number):					# This Function releases the key on the keyboard.
	line = log_list[log_number]
	key = (str(line.split(" _|_ ")[2]))

	if "'" in key:
		key = key[1:-1]
		pyautogui.keyUp(key)
		# print("released - ",key)
	elif "Key.cmd" in line:
		pyautogui.keyUp('winleft')
	elif "Key" in key:
		key = key.split(".")[1]
		pyautogui.keyUp(key)
		# print("KeyUp : "+key)
	else:
		if "Key.backspace" in line:
			pyautogui.keyUp('backspace')
		elif "Key.enter" in line:
			pyautogui.keyUp('enter')
		elif "Key.tab" in line:
			pyautogui.keyUp('tab')
		elif "Key.alt" in line:
			pyautogui.keyUp('alt')
		elif "Key.cmd" in line:
			pyautogui.keyUp('winleft')
		elif "Key.space" in line:
			pyautogui.keyUp('space')
		elif "Key.up" in line:
			pyautogui.keyUp('up')
		elif "Key.down" in line:
			pyautogui.keyUp('down')
		elif "Key.left" in line:
			pyautogui.keyUp('left')
		elif "Key.right" in line:
			pyautogui.keyUp('right')
		elif "Key.home" in line:
			pyautogui.keyUp('home')
		elif "Key.ctrl" in line:
			pyautogui.keyUp('ctrl')
		elif "Key.shift" in line:
			pyautogui.keyUp('shift')
		else:
			pass
			# key = (str(line.split(" _|_ ")[2]))
			# print("Unknown value - ",key)


def mouse_press(log_list, log_number):					# Clicks the Mouse Buttons.
	line = log_list[log_number]
	if "Button.left" in line:
		(x, y) = (str(line.split(" _|_ ")[2])[1:-1]).split(", ")			# Getting Mouse Locations
		if not (int(x), int(y)) == pyautogui.position():					# Check if the mouse is in the correct position or not
			pyautogui.moveTo(int(x), int(y), duration=Duration)		# if no, then Move it to that Location.
		pyautogui.mouseDown(button='left')								# Click the left button
	elif "Button.right" in line:
		(x, y) = (str(line.split(" _|_ ")[2])[1:-1]).split(", ")			# Getting Mouse Locations
		if not (int(x), int(y)) == pyautogui.position():					# Check if the mouse is in the correct position or not
			pyautogui.moveTo(int(x), int(y), duration=Duration)		# if no, then Move it to that Location.
		pyautogui.mouseDown(button='right')								# Click the right button


def mouse_release(log_list, log_number):				# Releases the Buttons checking the Location.
	line = log_list[log_number]
	if "Button.left" in line:
		(x, y) = (str(line.split(" _|_ ")[2])[1:-1]).split(", ")			# Getting Mouse Locations
		if not (int(x), int(y)) == pyautogui.position():					# Check if the mouse is in the correct position or not
			pyautogui.moveTo(int(x), int(y), duration=Duration)		# if no, then Move it to that Location.
		pyautogui.mouseUp(button='left')								# Release the left button
	elif "Button.right" in line:
		(x, y) = (str(line.split(" _|_ ")[2])[1:-1]).split(", ")			# Getting Mouse Locations
		if not (int(x), int(y)) == pyautogui.position():					# Check if the mouse is in the correct position or not
			pyautogui.moveTo(int(x), int(y), duration=Duration)		# if no, then Move it to that Location.
		pyautogui.mouseUp(button='right')								# Release the right button


def mouse_scroll(log_list, log_number):					# Scrolls the mouse Vertically and Horizontally.
	line = log_list[log_number]
	try:
		(x, y) = (str(line.split(" _|_ ")[2])[1:-1]).split(", ")			# Getting Mouse Location
		pyautogui.hscroll(int(x))										# For Horizontal Scroll. Only linux and OSX support Horizontal Scroll
		pyautogui.scroll(int(y))										# For normal Scroll.
	except AttributeError:
		pass


def mouse_move(log_list, log_number):					# Used to move mouse from one place to another. Basically, not needed.
	line = log_list[log_number]
	(x, y) = (str(line.split(" _|_ ")[2])[1:-1]).split(", ")				# Getting Mouse Location
	pyautogui.moveTo(int(x), int(y), duration=0.5)


def search_for_icon_on_screen(log_list, log_number):	# Takes screenshot and searches for the icon in it.
	icon_state = (log_list[log_number]).split(" _|_ ")
	line = log_list[log_number]
	try:
		if icon_state[9] == "Icon_Not_Found":
			return False
		else:
			icon_location, found_status = template_search.search(log_list, log_number)
			mouse_location = (((icon_location[0][0]+icon_location[1][0])/2), (icon_location[0][1]+icon_location[1][1])/2)
			if "Button.left" in line and found_status:
				(x, y) = mouse_location
				if (int(x), int(y)) != pyautogui.position():					# Check if the mouse is in the correct position or not
					pyautogui.moveTo(int(x), int(y), duration=Duration)		# if no, then Move it to that Location.
				pyautogui.click(button='left')									# Click the left button
			elif "Button.right" in line and found_status:
				(x, y) = mouse_location
				if (int(x), int(y)) != pyautogui.position():					# Check if the mouse is in the correct position or not
					pyautogui.moveTo(int(x), int(y), duration=Duration)		# if no, then Move it to that Location.
				pyautogui.click(button='right')									# Click the right button
			time.sleep(0.7)
			return found_status
	except IndexError:
		return False


def main_function():										# The Driver Code
	# platform = sys.platform
	# The Manager.py Saves the name of Log file to be played in temp.txt
	# we open the file and take the Log file's name into file_name variable
	temp_file = open(Temp_Log_File_Name, 'r')								# opening temp.txt
	train_data_file_name = temp_file.readlines()							# reading and assigning it to file_name
	train_data_file_name = train_data_file_name[0]							# filtering the file_name (As there was \n appended to it)

	log_file = open(train_data_file_name, 'r')
	log_list = log_file.readlines()
	log_number = 0

	while log_number < len(log_list):
		if "Keyboard" in log_list[log_number] and "Pressed" in log_list[log_number]:
			key_press(log_list, log_number)

		elif "Keyboard" in log_list[log_number] and "Released" in log_list[log_number]:
			key_release(log_list, log_number)

		# elif("Mouse" in line and "Moved" in line):						# Mouse_Move is not required
		# 	Mouse_Move(log_list, log_number)								# Mouse Pressed and Released can take care of the movement also

		elif "Scrolled" in log_list[log_number]:
			mouse_scroll(log_list, log_number)

		elif "Mouse" in log_list[log_number] and "Pressed" in log_list[log_number]:
			found_status = search_for_icon_on_screen(log_list, log_number)
			if not found_status:
				mouse_press(log_list, log_number)
			else:
				log_number += 1

		elif "Mouse" in log_list[log_number] and "Released" in log_list[log_number]:
			mouse_release(log_list, log_number)

		elif "Dynamic_Typing" in log_list[log_number]:
			dynamic_typing.main_function()

		log_number += 1

# search()
