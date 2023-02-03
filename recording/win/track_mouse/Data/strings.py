import sys

User_Details_File_Name = 'DB/User_Details.txt'
Voice_Log_File_Name = 'DB/Logs/Voice_Logs.txt'
Process_Log_File_Name = 'DB/Logs/Process_Logs.txt'
All_Log_File_Name = 'DB/Logs/All_Logs.txt'
Mouse_Log_File_Name = 'DB/Logs/Mouse_Logs.txt'
Key_Log_File_Name = 'DB/Logs/Key_Logs.txt'
Temp_Log_File_Name = 'DB/Logs/temp.txt'
Train_Data_Location = 'DB/Train_Data/'
recording_start_wav_file = "DB/Logs/recording_start.wav"
recording_stop_wav_file = "DB/Logs/recording_stop.wav"

Temp_png_file = "DB/Logs/Temp_Icon_Finder.png"

Log_File_Name_Mouse = 'DB/Logs/Mouse_Logs.txt'
Log_File_Name_Keyboard = 'DB/Logs/Key_Logs.txt'

Recorded_Video_Location = 'DB/Logs/screen_record.mp4'
Final_Icon_Name = "DB/Icons/Icon"# %d.png
Frame_Name = "DB/Frames/Frame"
ScreenRecord_File_Name = 'DB/Logs/screen_record.mp4'


User_Name = "User"
Assistant_Name = "PC_AssistANT"

platform = sys.platform

if "linux" in platform:
	Call_Mouse_Tracker = "./recording/linux//track_mouse/dist/track_mouse/track_mouse &"
	Call_Keyboard_Tracker = "./recording/linux/track_keyboard/dist/track_keyboard/track_keyboard &"
elif "darwin" in platform:
	Call_Mouse_Tracker = "./recording/mac/track_mouse/dist/track_mouse/track_mouse &"
	Call_Keyboard_Tracker = "./recording/mac/track_keyboard/dist/track_keyboard/track_keyboard &"
elif "win32" in platform:
	Call_Mouse_Tracker = "START /B recording\\win\\track_mouse\\dist\\track_mouse\\track_mouse"
	Call_Keyboard_Tracker = "START  /B recording\\win\\track_keyboard\\dist\\track_keyboard\\track_keyboard"
