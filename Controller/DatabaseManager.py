"""
Zachary Cook

Manages calls to the databases.
"""

from Model.HttpRequest import GetUserFromHash
from Model.HttpRequest import SessionStarted
from Model.HttpRequest import SessionEnded
from Model import User



"""
Returns the User for the given id (non-hash). If
there is no registered User, None is returned.
"""
def getUser(id):
	# Hash the id.
	hashedId = User.getHashFromId(id)

	# Create the request and return the user.
	request = GetUserFromHash.GetUserFromHash(hashedId)
	return request.getResponse()

"""
Registers a session being started.
"""
def sessionStarted(Session):
	request = SessionStarted.SessionStarted(Session.getUser().getHashedId())
	request.getResponse()

"""
Registers a session ended.
"""
def sessionEnded(Session):
	request = SessionEnded.SessionEnded(Session.getUser().getHashedId())
	request.getResponse()