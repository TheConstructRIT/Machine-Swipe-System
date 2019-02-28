"""
Zachary Cook

Manages starting and maintaining sessions.
"""

import threading
import time

from Controller import DatabaseManager
from Model import Session
from Util import Observer



"""
Thread that terminates sessions if they expire.
"""
class SessionThread(threading.Thread):
	"""
	Creates the thread.
	"""
	def __init__(self,sessionManager):
		super().__init__()
		self.sessionManager = sessionManager
		self.currentSession = sessionManager.getCurrentSession()

	"""
	Logic for the thread.
	"""
	def run(self):
		# Wait for the session to be overridden or the session to expire.
		while self.sessionManager.getCurrentSession() == self.currentSession and self.currentSession.getRemainingTime() > 0:
			time.sleep(0.1)

		# If the session expired, end the session.
		if self.sessionManager.getCurrentSession() == self.currentSession and self.currentSession.getRemainingTime() < 0:
			self.sessionManager.endSession()

"""
Class representing a session manager.
"""
class SessionManager(Observer.Observable):
	"""
	Creates the state manager.
	"""
	def __init__(self):
		super().__init__()
		self.currentSession = None

	"""
	Returns the current session. If there is
	no current session, None is returned.
	"""
	def getCurrentSession(self):
		return self.currentSession

	"""
	Starts a new session.
	"""
	def startSession(self,user):
		# Log the session being ended if the id is changing.
		if self.currentSession is not None and self.currentSession.getUser().getHashedId() != user.getHashedId():
			DatabaseManager.sessionEnded(self.currentSession)

		# Set the session.
		newSession = Session.startSession(user)
		self.currentSession = newSession
		self.notify(newSession)
		DatabaseManager.sessionStarted(newSession)

		# Start a thread to expire the session.
		sessionThread = SessionThread(self)
		sessionThread.start()

	"""
	Ends the current session.
	"""
	def endSession(self):
		# Log the session ending.
		DatabaseManager.sessionEnded(self.currentSession)

		# End the session.
		self.currentSession = None
		self.notify(None)



# Create a single instance of the session manager.
staticSessionManager = SessionManager()

"""
Returns the static session manager.
"""
def getSessionManager():
	return staticSessionManager