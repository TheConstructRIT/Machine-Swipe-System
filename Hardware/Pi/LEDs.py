"""
Zachary Cook

Class representing a set of hardware LEDs.
"""

# Channel of the Red LEDs (Pin 15).
LED_CHANNEL_RED = 22
# Channel of the Green LEDs (Pin 16).
LED_CHANNEL_GREEN = 23

# The time the LEDs is on when pulsed.
LEDS_ON_TIME = 0.075



import threading
import time

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
	Pulses the LEDs.
	"""
	def pulseColor(self,newColor,pulseCount=1,delay=0.1):
		# Pulses the color.
		def pulse():
			for _ in range(0,pulseCount):
				originalColor = self.currentColor
				self.setColor(newColor)
				time.sleep(LEDS_ON_TIME)
				self.setColor(originalColor)
				time.sleep(delay - LEDS_ON_TIME)

		# Create and start the thread.
		threading.Thread(target=pulse).start()

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