import time
import datetime
import math

def start_at_sync_seconds(sync_seconds=10):
	t = datetime.datetime.today()
	newsecond = roundup(t.second, sync_seconds)

	future = datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,rounddown(t.second, sync_seconds))

	if newsecond >= 60:
		future = jump_minute(future)
	else:
		future = datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,newsecond)
		if (future < t):
			newsecond = newsecond + sync_seconds
			if newsecond >= 60:
				future = jump_minute(future)
			else:
				future = datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,newsecond)

	rem_seconds = (future-t).seconds
	rem_milliseconds = (future-t).microseconds / 1000000.0

	# Enable only for debugging
	if False:
		print("future is ", future)
		print("t is ", t)
		print(rem_seconds + rem_milliseconds)

	time.sleep(rem_seconds + rem_milliseconds)

def jump_minute(t):
	t += datetime.timedelta(minutes=1)
	return datetime.datetime(t.year,t.month,t.day,t.hour,t.minute,0)

def roundup(x, nearest):
	return int(math.ceil(x / float(nearest))) * nearest

def rounddown(x, nearest):
	return int(math.floor(x / float(nearest))) * nearest

