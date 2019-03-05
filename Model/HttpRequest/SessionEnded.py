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
		url = ConfigurationManager.getServerEndpoint() + "/query"
		urlArgs = "request=MachineSessionEnded&machine=" + ConfigurationManager.getMachineInternalName() + "&hashedid=" + str(hashedId)
		super().__init__("POST", url, urlArgs=urlArgs)

	"""
	Sends the request in a thread. Nothing is returned.
	"""
	def getResponse(self):
		print("ENDED")
		threading.Thread(target=super().getResponse).start()