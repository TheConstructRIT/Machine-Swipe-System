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
	def __init__(self,id,maxSessionTime,accessType="UNAUTHORIZED"):
		self.id = id
		self.accessType = accessType
		self.maxSessionTime = maxSessionTime
	"""
	Returns the user's id.
	"""
	def getId(self):
		return self.id

	"""
	Returns the access type of the user.
	"""
	def getAccessType(self):
		return self.accessType

	"""
	Returns the max session time.
	"""
	def getSessionTime(self):
		return self.maxSessionTime