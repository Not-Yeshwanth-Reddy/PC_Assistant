import os
import datetime
from Data import strings
from tasks import add_delay
from database_manager import append_log

platform = strings.platform


def say(text_note):								# Speaks text_note passed as argument
	print("speaking = ", text_note) 					#----------------------------------------------
	if "linux" in platform:
		os.system('google_speech "' + text_note + '"')		# Using this to make it speak
	elif "darwin" in platform:
		os.system('say "' + text_note + '"')
	elif "win32" in platform:
		os.system('voice.exe "' + text_note + '"')
	add_delay.delay("short")										# without this sleep time, it is assigning text_note to audio_note


def say_n_save(local_step_name, local_text_note):  # Speaks local_text_note passed as argument
	local_now = datetime.datetime.now()  # 'local_now' will have the present date and time
	log = 'Voice_C _|_ ' + str(local_step_name) + " _|_ " + str(local_text_note) + ' _|_ ' + str(local_now.hour) + ' _|_ ' + str(
		local_now.minute) + ' _|_ ' + str(local_now.second) + ' _|_ ' + str(local_now.microsecond) + '\n'
	append_log.append(log)
	say(local_text_note)
