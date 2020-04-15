"""
Zachary Cook

Class representing a lab user.
"""



"""
Class for a user.
"""
class User():
	"""
	Constructor for the user.
	"""
	def __init__(self,id,maxSessionTime):
		self.id = id
		self.maxSessionTime = maxSessionTime

	"""
	Returns the user's id.
	"""
	def getId(self):
		return self.id

	"""
	Returns the max session time.
	"""
	def getSessionTime(self):
		return self.maxSessionTime