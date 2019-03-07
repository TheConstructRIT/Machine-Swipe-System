"""
Zachary Cook

Class representing a hardware relay.
"""

# Channel of the relay (Pin 7).
RELAY_CHANNEL = 4



# RPi is only on the Raspberry Pi.
from RPi import GPIO



"""
Class representing a relay.
"""
class Relay():
	"""
	Creates a relay.
	"""
	def __init__(self):
		# Set up the pins.
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(RELAY_CHANNEL,GPIO.OUT,initial=GPIO.HIGH)

		# Set up the initial state.
		self.setActive(False)

	"""
	Sets the relay being active.
	"""
	def setActive(self,active):
		if active:
			GPIO.output(RELAY_CHANNEL,GPIO.LOW)
		else:
			GPIO.output(RELAY_CHANNEL,GPIO.HIGH)