"""
Zachary Cook

Class representing the active system state.
"""

from Controller.States import SystemState



"""
Class for the active state.
"""
class Active(SystemState.SystemState):
	"""
	Returns the name of the state.
	"""
	def getName(self):
		return "Active"

	"""
	Invoked when the emergency stop button is pressed.
	"""
	def emergencyStopButtonPressed(self):
		# TODO: Terminate session
		# TODO: Stop system
		pass

	"""
	Invoked when a user swipes their id.
	"""
	def idSwiped(self, User):
		# TODO: Override session
		pass