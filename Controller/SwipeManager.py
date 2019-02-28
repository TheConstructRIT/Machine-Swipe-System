"""
Zachary Cook

Manages ids being swiped.
"""

from Controller import DatabaseManager
from Controller import ErrorManager
from Controller import StateManager



"""
Handles an id being swiped. Will either start a
session with the current state or display an error
if the User doesn't exist.
"""
def idSwiped(id):
	# Get the user.
	user = DatabaseManager.getUser(id)

	# Display an error if the user isn't registered.
	if user is None:
		ErrorManager.getErrorManager().sendErrorMessage("You aren't registered")
		return

	# Start the session.
	StateManager.getStateManager().idSwiped(user)