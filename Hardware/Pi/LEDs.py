"""
Zachary Cook

Class representing a set of hardware LEDs.
"""

# Channel of the Red LEDs (Pin 15).
LED_CHANNEL_RED = 22
# Channel of the Green LEDs (Pin 16).
LED_CHANNEL_GREEN = 23



# RPi is only on the Raspberry Pi.
from RPi import GPIO



"""
Class representing a set of LEDs.
"""
class LEDs():
	"""
	Creates the LEDs.
	"""
	def __init__(self):
		# Set up the pins.
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(LED_CHANNEL_RED,GPIO.OUT,initial=GPIO.LOW)
		GPIO.setup(LED_CHANNEL_GREEN,GPIO.OUT,initial=GPIO.LOW)

		# Set up the color.
		self.currentColor = "Red"
		self.setColor(self.currentColor)

	"""
	Sets the color of the LEDs.
	"""
	def setColor(self,newColor):
		self.currentColor = newColor

		# Update the pins.
		if newColor.lower() == "green":
			GPIO.setup(LED_CHANNEL_RED,GPIO.OUT,initial=GPIO.LOW)
			GPIO.setup(LED_CHANNEL_GREEN,GPIO.OUT,initial=GPIO.HIGH)
		elif newColor.lower() == "yellow":
			GPIO.setup(LED_CHANNEL_RED,GPIO.OUT,initial=GPIO.HIGH)
			GPIO.setup(LED_CHANNEL_GREEN,GPIO.OUT,initial=GPIO.HIGH)
		else:
			GPIO.setup(LED_CHANNEL_RED,GPIO.OUT,initial=GPIO.HIGH)
			GPIO.setup(LED_CHANNEL_GREEN,GPIO.OUT,initial=GPIO.LOW)