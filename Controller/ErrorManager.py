"""
Zachary Cook

Manages error messages displayed by the view.
"""

from Util import Observer



"""
Class representing an error manager.
"""
class ErrorManager(Observer.Observable):
	"""
	Creates the error manager.
	"""
	def __init__(self):
		super().__init__()
		self.currentErrorMessage = ""

	"""
	Sends an error message.
	"""
	def sendErrorMessage(self,message):
		self.currentErrorMessage = message
		self.notify(message)

	"""
	Returns the current error message.
	"""
	def getErrorMessage(self):
		return self.currentErrorMessage



# Create a single instance of the session manager.
staticErrorManager = ErrorManager()

"""
Returns the static error manager.
"""
def getErrorManager():
	return staticErrorManager