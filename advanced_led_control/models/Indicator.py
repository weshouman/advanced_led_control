from .colors import *
from .modes import *

import time
import logging

NO_FLICKER = 1001
FLICKER_MAX = 1000
MIN_FLICKER_DURATION = 30 # ms, consists of both on and off time
													# 24 fps is the maximum we can easily notice
													# 1000ms/24fps ~= 40ms, we picked 30 to be even more

class Indicator:
	""" Indicator class. """
	def __init__(self, m_col=GREEN, speed=1, brightness=1, func=None, i_time=4):
		self.m_col      = m_col # mode color
		self.speed      = speed
		self.brightness = brightness
		self.func       = func
		self.i_time     = i_time # indication time in seconds


	def indicate(self, stick, mode_led, active_time):
		col = self.m_col
		val_led = 1-mode_led

		curr_col = stick.get_color()
		if curr_col != col:
			stick.set_color(index=mode_led, red=col[0], green=col[1], blue=col[2])

		# Run the callback
		value_indication = self.func()
		col = value_indication.col
		flicker = value_indication.flicker

		logging.debug("Indication Callback returned color: %s, flicker: %d",
									col, flicker)

		flicker_time = float(FLICKER_MAX)/flicker # in ms as FLICKER_MAX is 1000
		flicker_time = max(flicker_time, MIN_FLICKER_DURATION) # set minimum

		# Use if we want to even flicker as long as we didn't reach the maximum
		# Most probably will get the led earlier to EOL B-)
		if (flicker >= NO_FLICKER):
		# Use if we want to stop flickering as long before even reaching the maximum
		# but rather based on the MIN_FLICKER_DURATION
		#if (flicker > FLICKER_MAX or flicker_time == MIN_FLICKER_DURATION):
			logging.info("Fixed for %1.2fs", active_time)
			stick.set_color(index=val_led, red=col[0], green=col[1], blue=col[2])
			time.sleep(active_time)

		else:
			one_flicker  = flicker_time / 2	# a pulse is defined by the delay of either on or off

			active_time_ms = active_time*1000
			logging.info("Flickering for %1.2fs", active_time)
			repeats = active_time_ms/flicker_time

			repeats = max(repeats, 1) # minimum is one repeat

			# TODO:start pulsing in a different thread and stop it when exact active_time is over
			logging.debug("Flickering for %d times, with duration %dms each on and each off",
										repeats, one_flicker)
			stick.pulse(index=val_led, red=col[0], green=col[1], blue=col[2],
									repeats=int(repeats), duration=int(one_flicker), steps=10)
