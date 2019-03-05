"""
Zachary Cook

Manages ids being swiped.
"""

import threading

from Controller import DatabaseManager
from Controller import MessageManager
from Controller import StateManager



"""
Handles an id being swiped. Will either start a
session with the current state or display an error
if the User doesn't exist.
"""
def idSwiped(id):
	# Swipes the id.
	def swipe():
		# Display an error of the machine is stopped.
		if StateManager.getState().getName() == "Stopped":
			MessageManager.sendMessage(MessageManager.EMERGENCY_STOP_PRESSED_WARNING)
			return

		# Display a "Please wait" message.
		MessageManager.sendMessage(MessageManager.PLEASE_WAIT_MESSAGE)

		# Get the user.
		user = DatabaseManager.getUser(id)

		# Display an error if the user isn't registered.
		if user is None:
			MessageManager.sendMessage(MessageManager.UNREGISTERED_USER_MESSAGE)
			return

		# Start the session.
		StateManager.idSwiped(user)

	# Start the swipe in a thread.
	threading.Thread(target=swipe).start()