"""
Zachary Cook

Class representing the stopped system state.
"""

from Controller.States import SystemState
from Controller import ErrorManager



"""
Class for the stopped state.
"""
class Stopped(SystemState.SystemState):
	"""
	Returns the name of the state.
	"""
	def getName(self):
		return "Stopped"

	"""
	Invoked when the emergency stop button is released.
	"""
	def emergencyStopReleased(self):
		self.stateManager.setStateByName("Inactive")

	"""
	Invoked when a user swipes their id.
	"""
	def idSwiped(self, User):
		ErrorManager.getErrorManager().sendErrorMessage("Machine stopped")