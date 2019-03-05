"""
Zachary Cook

Class representing the inactive system state.
"""

from Controller.States import SystemState
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
	def idSwiped(self,User):
		self.stateManager.setStateByName("Active")
		SessionManager.startSession(User)