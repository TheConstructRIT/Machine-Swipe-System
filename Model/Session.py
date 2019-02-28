"""
Zachary Cook

Class representing a session for a user.
"""

from Model import Time

"""
Class for a session.
"""
class Session():
	"""
	Constructor for a session.
	"""
	def __init__(self,user,sessionStart):
		self.user = user
		self.sessionStart = sessionStart

	"""
	Returns the user.
	"""
	def getUser(self):
		return self.user

	"""
	Returns the length of the session.
	"""
	def getSessionTime(self):
		return self.getUser().getSessionTime()

	"""
	Returns the start time of the session.
	"""
	def getStartTime(self):
		return self.sessionStart

	"""
	Returns the end time of the session.
	"""
	def getEndTime(self):
		return self.getStartTime() + self.getSessionTime()

	"""
	Returns the remaining time.
	"""
	def getRemainingTime(self):
		return self.getEndTime() - Time.getCurrentTimestamp()



"""
Creates a session for a user at the current time.
"""
def startSession(user):
	return Session(user, Time.getCurrentTimestamp())