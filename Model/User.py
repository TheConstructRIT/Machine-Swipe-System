"""
Zachary Cook

Class representing a lab user.
"""

import hashlib



"""
Class for a user.
"""
class User():
	"""
	Constructor for the user.
	"""
	def __init__(self,hashedId,name,maxSessionTime):
		self.hashedId = hashedId
		self.name = name
		self.maxSessionTime = maxSessionTime

	"""
	Returns the hash of the user's id.
	"""
	def getHashedId(self):
		return self.hashedId

	"""
	Returns the name of the user.
	"""
	def getName(self):
		return self.name

	"""
	Returns the max session time.
	"""
	def getSessionTime(self):
		return self.maxSessionTime



"""
Returns the hashed id for a user.
"""
def getHashFromId(userId):
	return hashlib.sha256(str(userId).encode("UTF-8")).hexdigest()