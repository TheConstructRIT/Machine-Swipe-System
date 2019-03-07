"""
Zachary Cook

Class representing the hardware emergency stop button.
"""

# Channel of the Emergency Stop button (Pin 11).
EMERGENCY_STOP_CHANNEL = 17



import threading
import time

from Controller import Observer

# RPi is only on the Raspberry Pi.
from RPi import GPIO



"""
Class representing an emergency stop button.
"""
class EmergencyStopButton(Observer.Observable):
	"""
	Creates the emergency stop button.
	"""
	def __init__(self):
		super().__init__()
		self.lastState = False

		# Set up the pins.
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(EMERGENCY_STOP_CHANNEL,GPIO.IN,pull_up_down=GPIO.PUD_UP)

		# Start polling the button pressing.
		self.startPolling()

	"""
	Returns if the button is pressed.
	"""
	def isPressed(self):
		return GPIO.input(EMERGENCY_STOP_CHANNEL)

	"""
	Starts the polling for the button presses.
	"""
	def startPolling(self):
		# Performs polling.
		def startPolling():
			while True:
				newButtonState = self.isPressed()

				# Notify the observers if the state changed.
				if newButtonState != self.lastState:
					self.lastState = newButtonState
					self.notify(newButtonState)

				# Add an artificial delay for polling.
				time.sleep(0.05)

		# Create and start a thread for pulling.
		threading.Thread(target=startPolling).start()