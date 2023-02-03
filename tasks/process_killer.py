import os
from Data import strings

process_log_file_name = strings.Process_Log_File_Name		# Getting Variables
platform = strings.platform									# Knowing which Operating System is this


def the_killer(process_list):  								# Kills all the other Learning_Mode except PC_AssistANT
	leave_id = os.getpid()
	if "win32" in platform:
		os.system('TASKLIST > ' + str(process_log_file_name))
		with open(process_log_file_name) as f:
			array = []
			i = 0
			for line in f:
				for Process in process_list:
					if Process in line:
						array.append(line)
						kill_id = [int(Kill_ID) for Kill_ID in array[i].split() if Kill_ID.isdigit()]
						kill_id = kill_id[0]
						if not leave_id == kill_id:
							print("Killing - python(" + str(kill_id) + ")")
							kill = "taskkill /PID " + str(kill_id) + " /F"
							os.system(kill)
							print(kill)
						i += 1
	elif "darwin" in platform or "linux" in platform:
		os.system('ps -A > ' + str(process_log_file_name))
		with open(process_log_file_name) as f:
			for line in f:
				line2 = line.lstrip()
				for Process in process_list:
					if Process in line:
						line3 = str(line2).split(' ')
						kill_id = int(line3[0])
						if kill_id != leave_id:
							os.system('kill ' + str(kill_id))
							print("Killed - " + str(kill_id))

