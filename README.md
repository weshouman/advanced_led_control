### About
A package to ease the control of the [blinkstick nano](https://www.blinkstick.com/products/blinkstick-nano)

Source code is at [https://github.com/weshouman/advanced_led_control](https://github.com/weshouman/advanced_led_control)

### Example
Save this example as ```test.py``` then run it as in the [Usage](#Usage) section below
```python
import advanced_led_control.models.colors as c
from advanced_led_control.models.leds import *
from advanced_led_control.models.ValueIndication import *
from advanced_led_control.models.Indicator       import *
from advanced_led_control.models.Procedure       import *

def indic1_func():
	# Indication values are best shown between 1 and 10
	value_indication = ValueIndication(c.RED, 10)
	return value_indication

def indic2_func():
	value_indication = ValueIndication(c.BLUE, NO_FLICKER)
	return value_indication

indic1 = Indicator(m_col=c.GREEN, func=indic1_func, i_time=4)
indic2 = Indicator(m_col=c.GREEN, func=indic2_func, i_time=4)

stick = blinkstick.find_first()
procedure = Procedure(stick=stick, mode_led=LED_2, quiet=10, sync_duration=10)

# Append all indicators to be run
procedure.indicators.append(indic1)
procedure.indicators.append(indic2)

# Run the specified procedure
procedure.run()
```

### Usage
This utility needs ```sudo``` to execute, as required by the ```blinkstick``` package.
If you are using a virtualenv, run
```
virtualenv -p python3 venv
pip install advanced-led-control
source venv/bin/activate
# Follow this [answer](https://stackoverflow.com/a/50335946/2730737) for why we need to use fully qualified path with sudo
sudo venv/bin/python test.py
```
If you are using sudo natively, run ```sudo -E python test.py```

#### Configuration
##### Indicator Params
- ```m_col```: the indication mode color, based on any of the color types defined below  
- ```func```: a callback that will be called to evaluate the color and flickering for the value led.
- ```brightness```: a value in range [0, 1] that gets multiplied by both the mode and value indication.
- ```i_time```: indication time, is how much time is allocated for this mode.

##### Indicator Callback
Returns
- ```color```: the indication value color, based on any of the color types defined below  
     NOTE: CSS names don't work with flickering, follow this [report](https://forums.blinkstick.com/t/python-api-colornames-not-working-with-pulse/1311?u=eng.walidshouman)
- ```flickering```: an integer that shows the speed of flickering of this color,
     the higher the value the faster the flickering.
     Recommended Values are in range [1, 20].
     Use ```NO_FLICKER``` or ```1001``` to set the led on without flickering.

##### Color Type
An indication color is either one of the 3 types
- ```RGB```: a list of 3 vals in RGB ie. [0, 10, 0].
- ```HEX```: a string ie. '#00ffff'.
- ```CSS_NAME```: a string ie. 'aliceblue'.

##### Procedure Params
- ```mode_led```: Choose between ```LED_1``` and ```LED_2```, currently ```LED_1``` isn't supported
     as the blinkstick doesn't allow flickering the second led
     while the first is set constantly.  
     Follow this [report](https://forums.blinkstick.com/t/cant-pulse-second-led-and-keep-first-on/1310?u=eng.walidshouman).

- ```quiet```: A percentage to be taken from the indication time for the stick to shutdown.  
     Setting ```quiet=0``` will disable this feature,
     and force all the indications to run consecutively.  
     Setting ```quiet=100``` is useless, as it will take all the indication time as a break!

- ```sync_duration```: Allows starting the procedure at a specific second,
    as this package is made to run for multiple machines/RPis that are working separately,
    and to avoid using communication to control the led,
    we allow sync based on real time.  
    Use a ```sync_duration``` of at least 1.2 total indication time to count for the
    delay the pulses make, and if it's less than the total indication time,
    it will be almost useless.  
    NOTE: Set ```sync_duration=0``` to disable this feature.  
    NOTE: Setting ```sync_duration``` to say 8 will start at every eighth second,
          In example, [0, 8, 16, 24, 32 ...]

### Notes
- This project was inspired by the [Pi Dramble](https://github.com/geerlingguy/raspberry-pi-dramble)
