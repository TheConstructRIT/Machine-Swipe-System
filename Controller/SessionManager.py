"""
Zachary Cook

Manages starting and maintaining sessions.
"""

import threading
import time

from Controller import DatabaseManager
from Controller import Observer
from Model import Session

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
		# Wait for the session to finish.
		time.sleep(self.currentSession.getRemainingTime())

		# If the session expired and active, end the session.
		if self.sessionManager.currentSession == self.currentSession and self.currentSession.getRemainingTime() <= 0:
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
		# End the session if the session is invalid.
		if self.currentSession is not None and self.currentSession.getRemainingTime() <= 0:
			self.endSession()

		# Return the current session.
		return self.currentSession

	"""
	Starts a new session.
	"""
	def startSession(self,user):
		# Log the session being ended if the id is changing.
		if self.currentSession is not None and self.currentSession.getUser().getId() != user.getId():
			DatabaseManager.sessionEnded(self.currentSession)

		# Set the session.
		newSession = Session.startSession(user)
		self.currentSession = newSession
		self.notify(newSession)
		DatabaseManager.sessionStarted(newSession)

		# Start a thread to expire the session.
		sessionThread = SessionThread(self)
		sessionThread.daemon = True
		sessionThread.start()

	"""
	Ends the current session.
	"""
	def endSession(self):
		# Log the session ending.
		if self.currentSession is not None:
			DatabaseManager.sessionEnded(self.currentSession)

			# End the session.
			self.currentSession = None
			self.notify(None)



# Create a single instance of the session manager.
staticSessionManager = SessionManager()

"""
Returns the current session. If there is
no current session, None is returned.
"""
def getCurrentSession():
	return staticSessionManager.getCurrentSession()

"""
Starts a new session.
"""
def startSession(user):
	staticSessionManager.startSession(user)

"""
Ends the current session.
"""
def endSession():
	staticSessionManager.endSession()

"""
Registers an observer.
"""
def register(observer):
	staticSessionManager.register(observer)

"""
Unregisters an observer.
"""
def unregister(observer):
	staticSessionManager.unregister(observer)