"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""
import sys
import os
import pyautogui

ScreenRecord_File_Name	= 'Logs/screen_record.mp4'


def main_function():
	(x,y) = pyautogui.size()			# Getting Screen Size

	platform = sys.platform				# Getting System Platform

	if "linux" in platform:
		terminal_command = ("ffmpeg -video_size "+ str(x) + "x" + str(y) + " -framerate 100 -f x11grab -i :0.0+0,0 -qp 0 " + str(ScreenRecord_File_Name) + " -y -loglevel panic &")
		os.system(terminal_command)							# Terminal command for screen Recording
	elif "darwin" in platform:
		pass
	elif "win32" in platform:
		terminal_command = ("ffmpeg -rtbufsize 1500M -f dshow -i video=\"UScreenCapture\" -r 100 -vcodec libx264 -qp 0 " + str(ScreenRecord_File_Name) + " -y -loglevel panic &")
		os.system(terminal_command)							# Terminal command for screen Recording
	else:
		print("Sorry, platform not supported")

# main_function()
