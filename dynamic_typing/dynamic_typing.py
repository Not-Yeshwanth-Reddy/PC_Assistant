"""
Written By	- Yeshwanth Reddy
NnY_Packages
"""
import pyautogui
import speech_recognition as sr
import random
import time
import os
import sys

recording_start_wav_file = "db/Logs/recording_start.wav"
recording_stop_wav_file = "db/Logs/recording_stop.wav"

platform = sys.platform


def delay(delay_in_sec):										# time.sleep function
	if delay_in_sec == "short":
		time.sleep(0.025)
	elif delay_in_sec == "medium":
		time.sleep(0.1)
	elif delay_in_sec == "long":
		time.sleep(0.3)
	else:
		time.sleep(int(delay_in_sec))


def speek_it(text_note):								# Speaks text_note passed as argument
	print("speaking = ", text_note) 					#----------------------------------------------
	if "linux" in platform:
		os.system('google_speech "' + text_note + '"')		# Using this to make it speak
	elif "darwin" in platform:
		os.system('say "' + text_note + '"')
	elif "win32" in platform:
		os.system('voice.exe "' + text_note + '"')
	delay("short")										# without this sleep time, it is assigning text_note to audio_note


def hear_it():											# Just Listens to voice command and stores in heard
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
			speek_it(
				random.choice([
							"Can you repeat it?",
							"I didn't hear you properly.",
							"Pardon Me.",
							"what did you say?",
							"What was that?",
							"I didn't get you"]))		# handling un recognised speech
			continue										# Re-calling the same function to listen properly
		break
	return heard


def find_integer(type_text):
	s = [int(s) for s in type_text.split() if s.isdigit()]
	if not s:
		if "one" in type_text:
			s = [1]
		elif "two" in type_text:
			s = [2]
		elif "three" in type_text:
			s = [3]
		else:
			s = [1]
	return s[0]


def type_it(type_text):
	if "tab space" in type_text:
		pyautogui.press('tab')
	elif "go to next line" in type_text:
		pyautogui.press('enter')
	elif "delete" in type_text and "character" in type_text:
		s = find_integer(type_text)
		while not s == 0:
			pyautogui.press('backspace')
			time.sleep(0.025)
			s -= 1
	elif "delete"in type_text and "word" in type_text:
		s = find_integer(type_text)
		while not s == 0:
			pyautogui.keyDown('ctrl')
			pyautogui.keyDown('shift')
			pyautogui.press('left')
			pyautogui.keyUp('shift')
			pyautogui.keyUp('ctrl')
			pyautogui.keyDown('backspace')
			pyautogui.keyUp('backspace')
			s -= 1
	elif "delete"in type_text and "line" in type_text:
		s = find_integer(type_text)
		while not s == 0:
			pyautogui.keyDown('shift')
			pyautogui.keyDown('home')
			pyautogui.keyUp('home')
			pyautogui.keyUp('shift')
			pyautogui.keyDown('backspace')
			pyautogui.keyUp('backspace')
			s -= 1
	else:
		pyautogui.keyDown('space')
		pyautogui.keyUp('space')
		for char in type_text:
			pyautogui.typewrite(char)


def main_function():
	speek_it("Dynamic Typing Activated")
	speek_it("Please start narrating")
	heard = hear_it()
	while "stop typing" not in heard:
		type_it(heard)
		heard = hear_it()
	speek_it("Exiting Typing mode")

# main_function()
