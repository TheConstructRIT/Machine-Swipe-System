"""
Zachary Cook

Class representing the active system state.
"""

from Controller.States import SystemState
from Controller import SessionManager, Observer

"""
Observer for session changes.
"""
class SessionObserver(Observer.Observer):
	"""
	Creates the observer.
	"""
	def __init__(self,stateMachine):
		self.stateMachine = stateMachine

	"""
	Notified when the session changes.
	"""
	def notify(self,*args):
		# Get the current session and state.
		newSession = args[0]
		currentlyActive = self.stateMachine.getState().getName() == "Active"

		# Set the state to inactive if there is no active session.
		if newSession is None and currentlyActive:
			self.stateMachine.setStateByName("Inactive")

"""
Class for the active state.
"""
class Active(SystemState.SystemState):
	"""
	Creates the system state.
	"""
	def __init__(self,stateManager):
		super().__init__(stateManager)
		self.stateManager = stateManager

		# Set up the observer for session changes.
		observer = SessionObserver(stateManager)
		SessionManager.getSessionManager().register(observer)

	"""
	Returns the name of the state.
	"""
	def getName(self):
		return "Active"

	"""
	Invoked when the emergency stop button is pressed.
	"""
	def emergencyStopButtonPressed(self):
		SessionManager.getSessionManager().endSession()
		self.stateManager.setStateByName("Stopped")

	"""
	Invoked when a user swipes their id.
	"""
	def idSwiped(self,User):
		SessionManager.getSessionManager().startSession(User)