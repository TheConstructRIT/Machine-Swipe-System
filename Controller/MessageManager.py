"""
Zachary Cook

Manages messages displayed by the view.
"""

from Controller import Observer



# Message for the E-Stop being pressed.
EMERGENCY_STOP_PRESSED_WARNING = "Machine stopped"

# Message for a user being unregistered.
UNREGISTERED_USER_MESSAGE = "You aren't registered"

# Message for a user not being authorized.
UNAUTHORIZED_MESSAGE = "You aren't authorized"

# Message for telling the user to wait for the request to load.
PLEASE_WAIT_MESSAGE = "Please wait"



"""
Class representing an error manager.
"""
class MessageManager(Observer.Observable):
	"""
	Creates the error manager.
	"""
	def __init__(self):
		super().__init__()
		self.currentMessage = ""

	"""
	Sends a message.
	"""
	def sendMessage(self,message):
		self.currentMessage = message
		self.notify(message)

	"""
	Returns the current message.
	"""
	def getMessage(self):
		return self.currentMessage



# Create a single instance of the session manager.
staticMessageManager = MessageManager()

"""
Sends an error message.
"""
def sendMessage(message):
	staticMessageManager.sendMessage(message)

"""
Returns the current error message.
"""
def getMessage():
	return staticMessageManager.getMessage()

"""
Registers an observer.
"""
def register(observer):
	staticMessageManager.register(observer)

"""
Unregisters an observer.
"""
def unregister(observer):
	staticMessageManager.unregister(observer)