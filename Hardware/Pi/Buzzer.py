"""
Zachary Cook

Class representing a buzzer.
"""

# Channel of the buzzer (Pin 13).
BUZZER_CHANNEL = 27

# The time the buzzer is on when pulsed.
BUZZER_ON_TIME = 0.025



import time
import threading

# RPi is only on the Raspberry Pi.
from RPi import GPIO



"""
Class representing a buzzer.
"""
class Buzzer():
	"""
	Sets up the buzzer.
	"""
	def __init__(self):
		# Set up the pins.
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(BUZZER_CHANNEL,GPIO.OUT,initial=GPIO.LOW)

	"""
	Pulses the buzzer.
	"""
	def pulseBuzzer(self,pulseCount = 1,delay = 0.1):
		# Pulses the buzzer.
		def pulse():
			for _ in range(0,pulseCount):
				GPIO.output(BUZZER_CHANNEL,GPIO.HIGH)
				time.sleep(BUZZER_ON_TIME)
				GPIO.output(BUZZER_CHANNEL,GPIO.LOW)
				time.sleep(delay - BUZZER_ON_TIME)

		# Create and start the thread.
		threading.Thread(target=pulse).start()