"""
Zachary Cook

Class representing the stopped system state.
"""

from Controller.States import SystemState



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
	Invoked when a user swipes their id.
	"""
	def idSwiped(self, User):
		# TODO: Display an error
		pass