"""
Zachary Cook

Class representing the toggle access type prompt system state.
"""

from Controller.States import SystemState

"""
Class for the toggle access type prompt state.
"""
class ToggleAccessTypePrompt(SystemState.SystemState):
    """
    Creates the system state.
    """
    def __init__(self,stateManager):
        super().__init__(stateManager)
        self.stateManager = stateManager

    """
    Returns the name of the state.
    """
    def getName(self):
        return "ToggleAccessTypePrompt"

    """
    Invoked when the emergency stop button is released.
    """
    def emergencyStopButtonReleased(self):
        self.stateManager.states["ToggleAccessType"].currentUser = None
        self.stateManager.setStateByName("ToggleAccessType")

    """
    Invoked when a user swipes their id.
    """
    def idSwiped(self,user):
        self.stateManager.setStateByName("Stopped")