"""
Zachary Cook

Class representing a session for a user.
"""

class Session():
	"""
	Creates a session for the given user.
	"""
	def __init__(self,user):
		self.user = user

	"""
	Returns the user.
	"""
	def getUser(self):
		return self.user