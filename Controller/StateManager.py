"""
Zachary Cook

Manages states in the system.
"""

from Controller.States import Active
from Controller.States import Inactive
from Controller.States import Stopped
from Controller import Observer

"""
Class representing a state manager.
"""
class StateManager(Observer.Observable):
	"""
	Creates the state manager.
	"""
	def __init__(self):
		super().__init__()

		# Create the state objects.
		self.states = {
			"Active": Active.Active(self),
			"Inactive": Inactive.Inactive(self),
			"Stopped": Stopped.Stopped(self),
		}
		self.currentState = self.states["Stopped"]

	"""
	Returns the current state.
	"""
	def getState(self):
		return self.currentState

	"""
	Sets the current state.
	"""
	def setStateByName(self,stateName):
		self.currentState = self.states[stateName]
		self.notify(self.currentState)

	"""
	Invoked when the emergency stop button is pressed.
	"""
	def emergencyStopButtonPressed(self):
		self.getState().emergencyStopButtonPressed()

	"""
	Invoked when the emergency stop button is released.
	"""
	def emergencyStopButtonReleased(self):
		self.getState().emergencyStopButtonReleased()

	"""
	Invoked when a user swipes their id.
	"""
	def idSwiped(self,user):
		self.getState().idSwiped(user)



# Create a single instance of the state manager.
staticStateManager = StateManager()

"""
Returns the current state.
"""
def getState():
	return staticStateManager.getState()

"""
Sets the current state.
"""
def setStateByName(stateName):
	staticStateManager.setStateByName(stateName)

"""
Invoked when the emergency stop button is pressed.
"""
def emergencyStopButtonPressed():
	staticStateManager.emergencyStopButtonPressed()

"""
Invoked when the emergency stop button is released.
"""
def emergencyStopButtonReleased():
	staticStateManager.emergencyStopButtonReleased()

"""
Invoked when a user swipes their id.
"""
def idSwiped(user):
	staticStateManager.idSwiped(user)

"""
Registers an observer.
"""
def register(observer):
	staticStateManager.register(observer)

"""
Unregisters an observer.
"""
def unregister(observer):
	staticStateManager.unregister(observer)