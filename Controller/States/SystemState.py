"""
Zachary Cook

Class representing a system state.
"""



"""
Abstract class for a system state.
"""
class SystemState():
	"""
	Creates the system state.
	"""
	def __init__(self,stateManager):
		self.stateManager = stateManager

	"""
	Returns the name of the state.
	"""
	def getName(self):
		return "UNKNOWN"

	"""
	Invoked when the emergency stop button is pressed.
	"""
	def emergencyStopButtonPressed(self):
		pass

	"""
	Invoked when the emergency stop button is released.
	"""
	def emergencyStopButtonReleased(self):
		pass

	"""
	Invoked when a user swipes their id.
	"""
	def idSwiped(self,User):
		pass