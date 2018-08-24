"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""
import datetime

from pynput.mouse import Listener as MListener

Log_File_Name = 'Logs/Mouse_Logs.txt'


def on_move(x, y):
    now = datetime.datetime.now()
    f = open(Log_File_Name, 'a')
    log = "Mouse _|_ Moved _|_ ({0}, {1}) ".format(int(x), int(y)) + "_|_ " + str(now.hour) + ' _|_ ' + str(
        now.minute) + ' _|_ ' + str(now.second) + ' _|_ ' + str(now.microsecond) + '\n'
    # print(log)
    f.write(log)
    f.close()


def on_click(x, y, button, pressed):
    now = datetime.datetime.now()
    f = open(Log_File_Name, 'a')
    log = "Mouse _|_ {0}.{1} _|_ {2} ".format('Pressed' if pressed else 'Released', button, (x, y)) + "_|_ " + str(
        now.hour) + ' _|_ ' + str(now.minute) + ' _|_ ' + str(now.second) + ' _|_ ' + str(now.microsecond) + '\n'
    # print(log)
    f.write(log)
    f.close()


def on_scroll(dx, dy):
    now = datetime.datetime.now()
    f = open(Log_File_Name, 'a')
    log = "Mouse _|_ Scrolled _|_ {0} ".format((int(dx), int(dy))) + "_|_ " + str(now.hour) + ' _|_ ' + str(
        now.minute) + ' _|_ ' + str(now.second) + ' _|_ ' + str(now.microsecond) + '\n'
    # print(log)
    f.write(log)
    f.close()


# Collect events until released
with MListener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
) as m_listener:
    m_listener.join()
