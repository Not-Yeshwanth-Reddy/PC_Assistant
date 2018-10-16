import time


def delay(delay_time):  # time.sleep function.
	if delay_time == "short":
		time.sleep(0.1)
	elif delay_time == "medium":
		time.sleep(0.3)
	elif delay_time == "long":
		time.sleep(0.5)
	else:
		time.sleep(int(delay_time))
