"""
Zachary Cook

Handles requests for getting a user from a hash.
"""

import json

from Controller import ConfigurationManager
from Model.HttpRequest import HttpRequest
from Model import User



"""
Class for getting users.
"""
class GetUserFromHash(HttpRequest.HttpRequest):
	"""
	Creates the http request.
	"""
	def __init__(self,hashedId):
		self.hashedId = hashedId

		# Create the http request.
		url = ConfigurationManager.getServerEndpoint() + "/query?request=GetMachineUser&machine=" +ConfigurationManager.getMachineInternalName() + "&hashedid=" + str(hashedId)
		default = "{\"name\":\"(Server offline)\",\"maxSessionTime\":" + str(ConfigurationManager.getDefaultSessionTime()) + "}"
		super().__init__("GET",url,default)

	"""
	Returns the result.
	"""
	def getResponse(self):
		# Get and parse the request.
		jsonResponse = super().getResponse()
		response = json.loads(jsonResponse)

		# Return a user if one exists.
		if "name" in response and "maxSessionTime" in response:
			return User.User(self.hashedId,response["name"],response["maxSessionTime"])