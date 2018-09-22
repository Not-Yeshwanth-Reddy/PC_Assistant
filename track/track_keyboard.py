"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""
import datetime

from pynput.keyboard import Listener as KListener

Log_File_Name = 'DataBase/Logs/Key_Logs.txt'


def on_press(key):  # this function is called whenever any key is pressed and key contains the value of key pressed
	now = datetime.datetime.now()
	f = open(Log_File_Name, 'a')
	log = "Keyboard _|_ Pressed _|_ " + str(key) + " _|_ " + str(now.hour) + ' _|_ ' + str(now.minute) + ' _|_ ' + str(
		now.second) + ' _|_ ' + str(now.microsecond) + '\n'
	# print(log)
	f.write(log)
	f.close()


def on_release(key):  # this function is called whenever any key is RELEASED and key contains the value of key RELEASED
	now = datetime.datetime.now()
	f = open(Log_File_Name, 'a')
	log = "Keyboard _|_ Released _|_ " + str(key) + " _|_ " + str(now.hour) + " _|_ " + str(now.minute) + ' _|_ ' + str(
		now.second) + ' _|_ ' + str(now.microsecond) + '\n'
	# print(log)
	f.write(log)
	f.close()


with KListener(
		on_press=on_press,
		on_release=on_release
		) as k_listener:
	k_listener.join()
