"""
Zachary Cook

Handles requests for a session ending.
"""

import threading

from Controller import ConfigurationManager
from Model.HttpRequest import HttpRequest



"""
Class for logging sessions ending.
"""
class SessionEnded(HttpRequest.HttpRequest):
	"""
	Creates the http request.
	"""
	def __init__(self,hashedId):
		self.hashedId = hashedId

		# Create the http request.
		url = ""
		super().__init__("POST",url)

	"""
	Sends the request in a thread. Nothing is returned.
	"""
	def getResponse(self):
		threading.Thread(target=super().getResponse).start()