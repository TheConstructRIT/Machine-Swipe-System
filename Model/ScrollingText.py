"""
Zachary Cook

Class representing text that scrolls if it is too long.
"""

from Util import Time



"""
Class for scrolling text.
"""
class ScrollingText():
	"""
	Creates the scrolling text.
	"""
	def __init__(self,text,maxLength,shiftTime):
		self.text = text
		self.maxLength = maxLength
		self.shiftTime = shiftTime
		self.startTime = Time.getCurrentTimestamp()

	"""
	Returns if the text fits.
	"""
	def textFits(self):
		return len(self.text) <= self.maxLength

	"""
	Returns the current text offset.
	"""
	def getCurrentOffset(self):
		if self.textFits():
			return 0
		else:
			return int(((Time.getCurrentTimestamp() - self.startTime)/self.shiftTime) % (len(self.text) + 1))

	"""
	Returns the current string to display.
	"""
	def getCurrentText(self):
		if self.textFits():
			return self.text
		else:
			doubleText = self.text + " " + self.text
			offset = self.getCurrentOffset()
			return doubleText[offset:offset + self.maxLength]