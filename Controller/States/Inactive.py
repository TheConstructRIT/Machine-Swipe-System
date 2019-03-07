"""
Zachary Cook

Class representing the inactive system state.
"""

from Controller.States import SystemState
from Controller import MessageManager
from Controller import SessionManager



"""
Class for the inactive state.
"""
class Inactive(SystemState.SystemState):
	"""
	Returns the name of the state.
	"""
	def getName(self):
		return "Inactive"

	"""
	Invoked when the emergency stop button is pressed.
	"""
	def emergencyStopButtonPressed(self):
		self.stateManager.setStateByName("Stopped")

	"""
	Invoked when a user swipes their id.
	"""
	def idSwiped(self,user):
		# Display an error if the user isn't authorized (session time is 0).
		if user.getSessionTime() <= 0:
			MessageManager.sendMessage(MessageManager.UNAUTHORIZED_MESSAGE)
			return

		# Start the session.
		self.stateManager.setStateByName("Active")
		SessionManager.startSession(user)