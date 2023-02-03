"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""
import datetime
import os
import random
import inflect
from fuzzywuzzy import fuzz

from dynamic_typing import dynamic_typing
from recording import screen_recorder
from repeat import control_keyboard_mouse
from tasks import understand, process_killer, add_delay
from database_manager import combine_logs, append_log
from Data import strings
from Voice import speak_it, hear_it
from tasks.open_application import *

# ToDO - Change Find_Train_Data Location in Windows
User_Details_File_Name = strings.User_Details_File_Name
Voice_Log_File_Name = strings.Voice_Log_File_Name
Process_Log_File_Name = strings.Process_Log_File_Name
All_Log_File_Name = strings.All_Log_File_Name
Mouse_Log_File_Name = strings.Mouse_Log_File_Name
Key_Log_File_Name = strings.Key_Log_File_Name
Temp_Log_File_Name = strings.Temp_Log_File_Name
Train_Data_Location = strings.Train_Data_Location
recording_start_wav_file = strings.recording_start_wav_file
recording_stop_wav_file = strings.recording_stop_wav_file

User_Name = strings.User_Name
Assistant_Name = strings.Assistant_Name
step_number = 0  # initializing step as int(0)
step_name = None  # initializing step_name as str(main task)
audio_note = None  # initializing audio_note as None
text_note = None  # initializing text_note as None
heard = None  # initializing text_note as None
temp = False  # declaring a temp variable for multi-purpose use
platform = strings.platform  # Knowing which Operating System is this

Call_Mouse_Tracker = strings.Call_Mouse_Tracker
Call_Keyboard_Tracker = strings.Call_Keyboard_Tracker

# def save_log_to_file(log):  # Appending Logs to .txt File
# 	print(log)
# 	f = open(Voice_Log_File_Name, 'a')  # Saving things in Log_file
# 	f.write(log)
# 	f.close()  # Flushing the buffer and saving file


def read_user_details():  # Opens the User_Details file and returns the User_Name and Assistant's name
	global User_Name, Assistant_Name
	f = open(User_Details_File_Name, 'r')
	lines = f.readlines()
	for line in lines:
		if "User_Name" in line:
			line = line.split(" : ")
			User_Name = line[1][:-1]
		if "Assistant_Name" in line:
			line = line.split(" : ")
			Assistant_Name = line[1][:-1]
	return User_Name, Assistant_Name


def change_user_details(user_name, assistant_name, local_heard):
	if "my" in local_heard:
		speak_it.say("Your name has been recorded as " + str(user_name))
		speak_it.say("What is your New User Name")
		user_name = hear_it.hear()
	elif "your" in local_heard:
		speak_it.say("You named me as " + str(assistant_name))
		speak_it.say("What is My New Name")
		assistant_name = hear_it.hear()
	f = open(User_Details_File_Name, 'w')
	log = "user_name : " + str(user_name) + "\n"
	f.write(log)
	log = "assistant_name : " + str(assistant_name) + "\n"
	f.write(log)
	f.close()
	speak_it.say("Changed successfully")
	speak_it.say("Changes will apply after restart")


# def speak_n_save(local_step_name, local_text_note):  # Speaks local_text_note passed as argument
# 	local_now = datetime.datetime.now()  # 'local_now' will have the present date and time
# 	log = 'Voice_C _|_ ' + str(local_step_name) + " _|_ " + str(local_text_note) + ' _|_ ' + str(local_now.hour) + ' _|_ ' + str(
# 		local_now.minute) + ' _|_ ' + str(local_now.second) + ' _|_ ' + str(local_now.microsecond) + '\n'
# 	save_log_to_file(log)
# 	speak_it.say(local_text_note)

#
# def the_killer(process_list):  								# Kills all the other Learning_Mode except PC_AssistANT
# 	leave_id = os.getpid()
# 	if "win32" in platform:
# 		os.system('TASKLIST > ' + str(Process_Log_File_Name))
# 		with open(Process_Log_File_Name) as f:
# 			array = []
# 			i = 0
# 			for line in f:
# 				for Process in process_list:
# 					if Process in line:
# 						array.append(line)
# 						kill_id = [int(Kill_ID) for Kill_ID in array[i].split() if Kill_ID.isdigit()]
# 						kill_id = kill_id[0]
# 						if not leave_id == kill_id:
# 							print("Killing - python(" + str(kill_id) + ")")
# 							kill = "taskkill /PID " + str(kill_id) + " /F"
# 							os.system(kill)
# 							print(kill)
# 						i += 1
# 	elif "darwin" in platform or "linux" in platform:
# 		os.system('ps -A > ' + str(Process_Log_File_Name))
# 		with open(Process_Log_File_Name) as f:
# 			for line in f:
# 				line2 = line.lstrip()
# 				for Process in process_list:
# 					if Process in line:
# 						line3 = str(line2).split(' ')
# 						kill_id = int(line3[0])
# 						if kill_id != leave_id:
# 							os.system('kill ' + str(kill_id))
# 							print("Killed - " + str(kill_id))

#
# def hear_it():  # Just Listens to voice command and stores in local_heard
# 	while True:
# 		try:
# 			r = sr.Recognizer()  # "listens for local_heard"
# 			with sr.Microphone() as source:  # Source - Microphone
# 				print("hearing...")  # ----------------------------------------------
# 				r.pause_threshold = 1  # minimum length of silence after phrase
# 				r.adjust_for_ambient_noise(source, duration=1)
# 				os.system("ffplay -autoexit " + str(recording_start_wav_file) + " -nodisp -loglevel panic")
# 				audio = r.listen(source, 10, 5)  # (source, timeout, phrase_time_limit)
# 				os.system("ffplay -autoexit " + str(recording_stop_wav_file) + " -nodisp -loglevel panic")
# 				print("recognizing...")  # ----------------------------------------------
# 				local_heard = r.recognize_google(audio).lower()
# 				print("local_heard = ", local_heard)
# 		except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
# 			# os.system("ffplay -autoexit "+ str(recording_stop_wav_file)+" -nodisp -loglevel panic")
# 			speak_it.say(
# 				random.choice([
# 					"Can you repeat it?",
# 					"I didn't hear you properly.",
# 					"what was it?",
# 					"what did you say?",
# 					"What was that?",
# 					"I didn't get you"]))  # handling un recognised speech
# 			continue  # Re-calling the same function to listen properly
# 		state = special_functions(local_heard)
# 		if state:
# 			continue
# 		else:
# 			return local_heard


def special_functions(herd):  # bla bla
	if "shut down" in herd or "exit" in herd:
		process_killer.the_killer(["K_Tracker", "M_Tracker", "ffmpeg"])
		speak_it.say("Exiting PC Assistant")
		exit()
	elif "suspend" in herd or "go to sleep" in herd:
		suspend()
		return True
	elif "what" in herd and "my" in herd and "name" in herd:
		speak_it.say("Your name has been recorded as " + User_Name)
		return True
	elif "what" in herd and "your" in herd and "name" in herd:
		speak_it.say("My name is " + Assistant_Name)
		return True
	elif "change" in herd and "name" in herd and ("your" in herd or "my" in herd):
		change_user_details(User_Name, Assistant_Name, herd)
		return True
	else:
		return False

#
# def just_listen():  # Just Listens to voice command and stores in herd
# 	while True:  # Doesn't speek anything if didnt hear anything
# 		r = sr.Recognizer()  # "listens for herd"
# 		try:
# 			with sr.Microphone() as source:  # Source - Microphone
# 				r.pause_threshold = 1  # minimum length of silence after phrase
# 				r.adjust_for_ambient_noise(source, duration=1)
# 				# print("hearing...")								#----------------------------------------------
# 				audio = r.listen(source, 4, 4)  # (source, timeout, phrase_time_limit)
# 				# print("recognizing...")
# 				herd = r.recognize_google(audio).lower()
# 				print("herd = ", herd)  # ----------------------------------------------
# 		except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError) as e:
# 			print(e)
# 			continue  # Re-calling the same function to listen properly
# 		break
# 	return herd


def note_it(local_step_name):  # Listens to command and logs it with local_step_name
	local_audio_note = hear_it.hear()
	local_now = datetime.datetime.now()  # 'local_now' has the current time stamp
	log = 'Voice_U _|_ ' + str(local_step_name) + " _|_ " + str(local_audio_note) + ' _|_ ' + str(local_now.hour) + ' _|_ ' + str(
		local_now.minute) + ' _|_ ' + str(local_now.second) + ' _|_ ' + str(local_now.microsecond) + '\n'
	append_log.append(log)
	speak_it.say('Noted..')
	return local_audio_note


def note_it_n_confirm(local_step_name):  # Listens to command and logs it with local_step_name
	while True:
		local_audio_note = hear_it.hear()
		speak_it.say('did you just say ' + local_audio_note)
		local_heard = hear_it.hear()
		if "yes" in local_heard or "yeah" in local_heard:
			local_now = datetime.datetime.now()  # 'local_now' has the current time stamp
			log = 'Voice_U _|_ ' + str(local_step_name) + " _|_ " + str(local_audio_note) + ' _|_ ' + str(local_now.hour) + ' _|_ ' + str(
				local_now.minute) + ' _|_ ' + str(local_now.second) + ' _|_ ' + str(local_now.microsecond) + '\n'
			append_log.append(log)
			speak_it.say('Noted..')
			return local_audio_note
		elif "no" in local_heard:
			speak_it.say("Then Tell it again Clearly")
			continue
		else:
			speak_it.say("reply Yes or No..!")


def inflecting(local_step_number):  # Converting int(1) to Str(First)...
	p = inflect.engine()  # If input is 1
	str_step = p.ordinal(local_step_number) + " step"
	return str_step  # Output 1st


def call_process(process_name):  # function used to call a Learning_Mode
	process_name.main_function()
	print("Called " + str(process_name))  # This will call the MainFunction() from the python Modules


def find_trained_data(local_audio_note):  # Finds for file name with 'local_audio_note' in it's Name.
	temp_list = os.listdir(Train_Data_Location)
	app_to_open, max_ratio = '', 0
	for line in temp_list:
		if fuzz.token_sort_ratio(line, local_audio_note) > max_ratio and ".txt" in line:
			app_to_open = line
			max_ratio = fuzz.token_sort_ratio(line, local_audio_note)

	if max_ratio > 50:
		local_audio_note = Train_Data_Location + app_to_open
		temp_file = open(Temp_Log_File_Name, 'w')
		temp_file.writelines(local_audio_note)
		temp_file.close()
		print("data found...")
		return True
	return False
# def find_trained_data(local_audio_note):  # Finds for file name with 'local_audio_note' in it's Name.
# 	temp_list = os.listdir(Train_Data_Location)
# 	for line in temp_list:
# 		if local_audio_note in line and ".txt" in line:
# 			local_audio_note = Train_Data_Location + line
# 			temp_file = open(Temp_Log_File_Name, 'w')
# 			temp_file.writelines(local_audio_note)
# 			temp_file.close()
# 			print("data found...")
# 			return True
# 	return False


def clear_logs():  # This will clean all the log files for fresh use.
	print("Cleaning Key_Logs")
	open(Key_Log_File_Name, 'w').close()  # Cleaning key_logs of previous task
	add_delay.delay(0.05)
	print("Cleaning Mouse_Logs")
	open(Mouse_Log_File_Name, 'w').close()  # Cleaning mouse_logs of previous task
	add_delay.delay(0.05)
	print("Cleaning Voice_Logs")
	open(Voice_Log_File_Name, 'w').close()  # Cleaning voice_logs of previous task
	add_delay.delay(0.05)
	print("Cleaning All_Logs")
	open(All_Log_File_Name, 'w').close()  # Cleaning all_logs of previous task
	add_delay.delay(0.05)
	print("Cleaning Process_Logs")
	open(Process_Log_File_Name, 'w').close()  # Cleaning process_logs of previous task
	add_delay.delay(0.05)


def suspend():  # Using busy waiting until wake keyword is herd.
	herd = ""
	# say(
	# 	random.choice([
	# 		"I'm going to sleep",
	# 		"Taking a nap",
	# 		"Sleeping",
	# 		"Good Night"]))

	while "assistant" not in herd and Assistant_Name not in herd:  # Busy Waiting
		herd = hear_it.listen()

	# say("Activating...")
	speak_it.say(  # 'How can I help You' kinda Statement
		random.choice([
			"Yes " + User_Name,
			# "How can i help you "+User_Name,
			# "Can I help you "+User_Name,
			# "How do I help you "+User_Name,
			"Hey, " + User_Name]))


# -----------------------------------------------------MAIN CODE------------------------------------------------------------

if "linux" in platform or "win32" in platform or "darwin" in platform:  # For Linux Mac and Windows Machines

	try:
		(User_Name, Assistant_Name) = read_user_details()
	except UnboundLocalError:
		pass

	speak_it.say(  # 'Hello' kinda Statments
		random.choice([
			"Hey " + User_Name + ".",
			"Hi " + User_Name,
			"Hello " + User_Name]))
	speak_it.say(  # 'How can I help You' kinda Statment
		random.choice([
			"How can I help You?",
			"What can I do for You?",
			"Can I help you?",
			"Do you need any help?",
			"How do I help you."]))

	while True:
		audio_note = hear_it.hear()

		# -------------------------------------------------------------LEARNING
		# ------------------------------------------------------------

		if ("learn" in audio_note) or ("teach" in audio_note and "you" in audio_note):  # Learning_Mode Code
			clear_logs()
			speak_it.say(
				random.choice([
					"Learning Mode Activated",
					"""I'm Ready to Learn""",
					"Getting Ready to Learn",
					"Lets get started"]))
			speak_it.say_n_save("Main Task", "Whats the Main Task")
			note_it_n_confirm("Main Task")

			now = datetime.datetime.now()
			call_process(screen_recorder)
			Log = 'Screen_Recorder _|_ Main Task _|_ Blank Field _|_ ' + str(now.hour) + ' _|_ ' + str(now.minute) + ' _|_ ' + str(now.second) + ' _|_ ' + str(now.microsecond) + '\n'
			append_log.append(Log)
			heard = ""
			while "task complete" not in heard:
				step_number += 1
				vstep = inflecting(step_number)
				text_note = "Whats the " + vstep
				speak_it.say_n_save(vstep, text_note)
				audio_note = note_it(vstep)

				if "dynamic" in audio_note and "typing" in audio_note:
					now = datetime.datetime.now()
					Log = 'Dynamic_Typing _|_ ' + str(vstep) + ' _|_ Some bla bla text _|_ ' + str(
						now.hour) + ' _|_ ' + str(now.minute) + ' _|_ ' + str(now.second) + ' _|_ ' + str(
						now.microsecond) + '\n'
					append_log.append(Log)
					call_process(dynamic_typing)
					speak_it.say("is there a next step?")
					heard = hear_it.hear()
					if "no" in heard:
						break
					else:
						continue

				else:
					os.system(Call_Keyboard_Tracker)
					os.system(Call_Mouse_Tracker)
					speak_it.say("Mouse and Keyboard are being Tracked.")
					heard = ""
					speak_it.say("Please show me how to do it.")
					while "complete" not in heard:
						heard = hear_it.listen()
					process_killer.the_killer(["track_keyboard", "track_mouse"])  # Stopping the trackers.

			speak_it.say("Exiting Learning Mode")
			process_killer.the_killer(["track_keyboard", "track_mouse", "ffmpeg"])  # Stopping the trackers.
			speak_it.say("Please wait a second while I Understand what you taught.")
			step_number = 0  # Resetting step_number to '0'
			add_delay.delay("medium")
			call_process(combine_logs)  # Call Merger
			add_delay.delay("long")
			call_process(understand)  # Call Understanding
			speak_it.say("Done..!")
			suspend()

		# ---------------------------------------------------------DYNAMIC
		# TYPING------------------------------------------------------

		elif ("start" in audio_note or "activate" in audio_note) and "typing" in audio_note:
			call_process(dynamic_typing)
			suspend()

		# ---------------------------------------------------------WHAT CAN YOU
		# DO-----------------------------------------------------

		elif "what can you do" in audio_note:
			speak_it.say(
				random.choice([
					"I can do a lot of things",
					"I can learn what you teach",
					"I can learn.",
					"I can sing a song.",
					# "What do you want me to do?",
					"I can do what ever you teach me"]))

				# # -----------------------------------------------------------SING A SONG-------------------------------------------------------
		#
		elif "sing" in audio_note and "song" in audio_note:
			speak_it.say(
				random.choice([
					"""Humpty Dumpty sat on a wall, Humpty dumpty fell from the wall, Humpty Dumpty Broke his ball, Humpty Dumpty died in the fall.""",
					"""Twinkle, twinkle, little star, How I wonder what you are! Up above the world so high, Like a diamond in the sky. When the blazing sun is gone, When he nothing shines upon, Then you show your little light, Twinkle, twinkle, all the night. """,
					"""Jack and Jill went up the hill. To fetch a pail of water; Jack fell down and broke his crown, and Jill came tumbling after. Up Jack got, and home did trot, As fast as he could caper, To old Dame Dob, who patched his nob, With vinegar and brown paper.""",
					"""Baa, baa, black sheep. Have you any wool?. Yes sir, yes sir, three bags full. One for the master, And one for the dame, And one for the little boy, Who lives down the lane.""",
					"""One two, pickup my shoe. three four, shut the door. five six, pick up the sticks. seven eight, lay them straight. nine ten, Big Fat Hen.""",
					# """Suffer suffer scream in pain. Blood is spilling from your brain. Zombies gnaaw you like a plum. Piercing cries and you succumb."""
					]))
			suspend()

		# ------------------------------------------------------------Open Application------------------------------------------------
		
		elif "open" in audio_note:
			open_status = open_app(audio_note)
			if open_status:
				speak_it.say("Opening application")
			else:
				speak_it.say("App Not Found")
			suspend()


		# ------------------------------------------------------------Search in DATABASE----------------------------------------------

		elif find_trained_data(audio_note):  # If training data is found
			speak_it.say("At your Service")
			call_process(control_keyboard_mouse)  # Calling MK_control if file is found
			speak_it.say("Task Completed")
			suspend()

		# ------------------------------------------------------------Search in DATABASE----------------------------------------------

		elif not find_trained_data(audio_note):  # If training data not found
			speak_it.say(
				random.choice([
					"""I don't know how to do it. Can you teach me""",
					"You never taught me how to do it",
					"I would surely do it if I had known how to do it",
					# "Sorry. But Fuck off",
					"I cant do it. You have to teach me"]))
		# "No. I Won't do it. why don't you do it yourself",
		# "First teach me how to do it. Idiot",

		else:
			speak_it.say("bla bla bla")  # this can never be spoken due to the above 2 elif conditions

# ------------------------------------------END OF Linux, Mac, Windows-----------------------------------------------------

else:
	print(" > This Software doesn't work on your Platform.\n > The Developers are still working on it.")
	print(" > * Available Platforms - linux (Linux)")
	print("   *                     - win32 (Windows)")
	print("   *                     - darwin (Mac)\n")
	print(" > Your Platform         -", platform)

speak_it.say("Exiting PC Assistant")
