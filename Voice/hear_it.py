import speech_recognition as sr
import os
import random
from Data import strings
from Voice import speak_it

recording_start_wav_file = strings.recording_start_wav_file
recording_stop_wav_file = strings.recording_stop_wav_file


def hear():											# Just Listens to voice command and stores in heard
	while True:
		try:
			r = sr.Recognizer()									# "listens for heard"
			with sr.Microphone() as source:						# Source - Microphone
				r.pause_threshold = 1							# minimum length of silence after phrase
				r.adjust_for_ambient_noise(source, duration=1)
				os.system("ffplay -autoexit " + str(recording_start_wav_file) + " -nodisp -loglevel panic")
				print("hearing...")								#----------------------------------------------
				audio = r.listen(source, 10, 5)					# (source, timeout, phrase_time_limit)
				os.system("ffplay -autoexit " + str(recording_stop_wav_file) + " -nodisp -loglevel panic")
				print("recognizing...")							#----------------------------------------------
				heard = r.recognize_google(audio).lower()
				print("heard = ", heard)
		except (sr.UnknownValueError, sr.WaitTimeoutError) as e:
			os.system("ffplay -autoexit " + str(recording_stop_wav_file) + " -nodisp -loglevel panic")
			print(e)
			speak_it.say(
				random.choice([
							"Can you repeat it?",
							"I didn't hear you properly.",
							"Pardon Me.",
							"what did you say?",
							"What was that?",
							"I didn't get you"]))		# handling un recognised speech
			continue										# Re-calling the same function to listen properly
		except sr.RequestError as e:
			print(e)
			continue
		break
	return heard


def listen():  # Just Listens to voice command and stores in herd
	while True:  # Doesn't speak anything if didn't hear anything
		try:
			r = sr.Recognizer()  # "listens for herd"
			with sr.Microphone() as source:  # Source - Microphone
				r.pause_threshold = 1  # minimum length of silence after phrase
				r.adjust_for_ambient_noise(source, duration=1)
				# print("hearing...")								#----------------------------------------------
				audio = r.listen(source, 4, 4)  # (source, timeout, phrase_time_limit)
				# print("recognizing...")
				herd = r.recognize_google(audio).lower()
				print("herd = ", herd)  # ----------------------------------------------
		except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError) as e:
			print(e)
			continue  # Re-calling the same function to listen properly
		break
	return herd
