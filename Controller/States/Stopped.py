"""
Zachary Cook

Class representing the stopped system state.
"""

from Controller.States import SystemState
from Controller import MessageManager



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
	def emergencyStopButtonReleased(self):
		self.stateManager.setStateByName("Inactive")

	"""
	Invoked when a user swipes their id.
	"""
	def idSwiped(self,user):
		if user.getAccessType() == "ADMIN":
			self.stateManager.setStateByName("ToggleAccessTypePrompt")
		else:
			MessageManager.sendMessage(MessageManager.EMERGENCY_STOP_PRESSED_WARNING)