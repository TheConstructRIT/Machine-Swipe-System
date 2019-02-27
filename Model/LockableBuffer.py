"""
Zachary Cook

Class representing a buffer that can be locked to prevent inputs.
"""



"""
Lockable buffer class.
"""
class LockableBuffer():
	"""
	Constructor of the lockable buffer.
	"""
	def __init__(self,maxSize):
		self.maxSize = maxSize
		self.buffer = []
		self.locked = False

	"""
	Adds a character or string to the buffer if it isn't locked.
	"""
	def append(self,string):
		if not self.locked:
			self.buffer.append(string)

			# Remove the first character if it is too long.
			if len(self.buffer) > self.maxSize:
				self.buffer.pop(0)

	"""
	Locks the buffer.
	"""
	def lock(self):
		self.locked = True

	"""
	Unlocks the buffer.
	"""
	def unlock(self):
		self.locked = False

	"""
	Clears the buffer.
	"""
	def clear(self):
		self.buffer = []

	"""
	Returns if the buffer is locked.
	"""
	def isLocked(self):
		return self.locked

	"""
	Concatenates the strings stored in the buffer.
	"""
	def getBufferString(self):
		finalString = ""

		# Create the string.
		for string in self.buffer:
			finalString += string

		# Return the string.
		return finalString