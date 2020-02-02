import sys
sys.path.append('./')

from advanced_led_control.models.leds import *
from advanced_led_control.models.ValueIndication import *
from advanced_led_control.models.Indicator       import *
from advanced_led_control.models.Procedure       import *

import logging

import psutil

logging.basicConfig(level=logging.INFO)
def indic1_func():
	cpu = psutil.cpu_percent()

	val = ValueIndication('yellow', NO_FLICKER)
	if cpu <= 40:
		val.col = 'green'
	elif cpu <= 60:
		val.col = 'orange'
	elif cpu <= 80:
		val.col = 'red'
		val.flicker = 1
	elif cpu > 80:
		val.col = 'red'
		val.flicker = cpu - 80

	return val

def indic2_func():
	virt_mem = psutil.virtual_memory()
	mem = virt_mem.percent

	val = ValueIndication('yellow', NO_FLICKER)
	if mem <= 40:
		val.col = 'green'
	elif mem <= 60:
		val.col = 'orange'
	elif mem <= 80:
		val.col = 'red'
		val.flicker = 1
	elif mem > 80:
		val.col = 'red'
		val.flicker = mem - 80

	return val

indic1 = Indicator(m_col='aqua', func=indic1_func, brightness = 0.1, i_time=4)
indic2 = Indicator(m_col='orchid', func=indic2_func, brightness = 0.1, i_time=4)

stick = blinkstick.find_first()
procedure = Procedure(stick=stick, mode_led=LED_2, quiet=10, sync_duration=0)

procedure.indicators.append(indic1)
procedure.indicators.append(indic2)

procedure.run()

