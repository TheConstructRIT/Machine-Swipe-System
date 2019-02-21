"""
Zachary Cook

Class representing the inactive system state.
"""

from Controller.States import SystemState



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
		# TODO: Stop system
		pass

	"""
	Invoked when a user swipes their id.
	"""
	def idSwiped(self, User):
		# TODO: Start session
		pass