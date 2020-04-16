"""
Zachary Cook

Class representing the toggle access type system state.
"""

from Controller import DatabaseManager
from Controller import Observer
from Controller.States import SystemState

"""
Class for the toggle access type state.
"""
class ToggleAccessType(SystemState.SystemState,Observer.Observable):
    """
    Creates the system state.
    """
    def __init__(self,stateManager):
        SystemState.SystemState.__init__(self,stateManager)
        Observer.Observable.__init__(self)
        self.stateManager = stateManager
        self.currentUser = None

    """
    Returns the name of the state.
    """
    def getName(self):
        return "ToggleAccessType"

    """
    Invoked when the emergency stop button is pressed.
    """
    def emergencyStopButtonPressed(self):
        self.stateManager.setStateByName("Stopped")

    """
    Invoked when a user swipes their id.
    """
    def idSwiped(self,user):
        # Swap the current user.
        lastUser = self.currentUser
        self.currentUser = user.getId()

        # Set the access type if the swiped user hasn't changed. The first swipe is used to show the current status.
        accessType = user.getAccessType()
        if self.currentUser == lastUser:
            if accessType == "UNAUTHORIZED":
                accessType = "AUTHORIZED"
            elif accessType == "AUTHORIZED":
                accessType = "ADMIN"
            else:
                accessType = "UNAUTHORIZED"
            DatabaseManager.setUserAccessType(self.currentUser,accessType)

        # Invoke the observers.
        self.notify(self.currentUser,accessType)