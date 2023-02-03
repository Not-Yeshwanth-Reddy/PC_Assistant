from Data import strings

Voice_Log_File_Name = strings.Voice_Log_File_Name


def append(log):  # Appending Logs to .txt File
	print(log)
	f = open(Voice_Log_File_Name, 'a')  # Saving things in Log_file
	f.write(log)
	f.close()  # Flushing the buffer and saving file
