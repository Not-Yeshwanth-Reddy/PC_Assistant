"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""
from pynput.mouse import Listener as MListener
import sys
import datetime

Log_File_Name='Logs/Mouse_Logs.txt'

def on_move(x, y):
	now = datetime.datetime.now()
	f = open(Log_File_Name, 'a')
	Log = "Mouse _|_ Moved _|_ ({0}, {1}) ".format(int(x),int(y)) +"_|_ " +str(now.hour)+' _|_ '+str(now.minute)+' _|_ '+str(now.second)+' _|_ '+str(now.microsecond)+'\n'
	# print(Log)
	f.write(Log)
	f.close()

def on_click(x, y, button, pressed):
	now = datetime.datetime.now()
	f = open(Log_File_Name, 'a')
	Log = "Mouse _|_ {0}.{1} _|_ {2} ".format('Pressed' if pressed else 'Released', button, (x,y)) +"_|_ " +str(now.hour)+' _|_ '+str(now.minute)+' _|_ '+str(now.second)+' _|_ '+str(now.microsecond)+'\n'
	# print(Log)
	f.write(Log)
	f.close()

def on_scroll(x, y, dx, dy):
	now = datetime.datetime.now()
	f = open(Log_File_Name, 'a')
	Log = "Mouse _|_ Scrolled _|_ {0} ".format((int(dx),int(dy))) +"_|_ " +str(now.hour)+' _|_ '+str(now.minute)+' _|_ '+str(now.second)+' _|_ '+str(now.microsecond)+'\n'
	# print(Log)
	f.write(Log)
	f.close()

# Collect events until released
with MListener(
		on_move=on_move,
		on_click=on_click,
		on_scroll=on_scroll
		) as mlistener:
	mlistener.join()
