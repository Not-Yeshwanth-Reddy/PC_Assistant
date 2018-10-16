import os
from Data import strings

Train_Data_Location = strings.Train_Data_Location
Temp_Log_File_Name = strings.Temp_Log_File_Name


def find_trained_data(audio_note):  # Finds for file name with 'audio_note' in it's Name.
	temp_list = os.listdir(Train_Data_Location)
	for line in temp_list:
		if audio_note in line and ".txt" in line:
			audio_note = Train_Data_Location + line
			temp_file = open(Temp_Log_File_Name, 'w')
			temp_file.writelines(audio_note)
			temp_file.close()
			print("data found...")
			return True
	return False
