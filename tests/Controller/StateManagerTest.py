"""
Zachary Cook

Unit tests for the StateManager.
"""

import unittest
import time
from Controller import DatabaseManager,MessageManager,StateManager,Observer
from Model import User

"""
Test the SessionManager class.
"""
class TestStateManagerClass(unittest.TestCase):
    """
    Sets up the unit test.
    """
    def setUp(self):
        DatabaseManager.staticDatabaseManager = DatabaseManager.DatabaseManager(":memory:")
        DatabaseManager.setUserAccessType("000000000","AUTHORIZED")
        DatabaseManager.setUserAccessType("000000001","UNAUTHORIZED")
        DatabaseManager.setUserAccessType("000000002","ADMIN")
        self.testUser = User.User("000000000",1,"AUTHORIZED")
        self.testUnauthorizedUser = User.User("000000001",0,"UNAUTHORIZED")
        self.testAdminUser = User.User("000000002",1,"ADMIN")

    """
    Tests the constructor.
    """
    def test_constructor(self):
        StateManager.StateManager()

    """
    Tests the getState method.
    """
    def test_getState(self):
        CuT = StateManager.StateManager()
        self.assertEqual(CuT.getState().getName(),"Stopped","Initial state is incorrect.")

    """
    Tests the setStateByName method.
    """
    def test_setStateByName(self):
        CuT = StateManager.StateManager()

        # Create an observer.
        class StateObserver(Observer.Observer):
            def notify(self,*args):
                self.observedState = args[0]

            def getNotifiedState(self):
                return self.observedState

        observer = StateObserver()
        CuT.register(observer)
        CuT.setStateByName("Inactive")
        self.assertEqual(CuT.getState().getName(),"Inactive","Initial state is incorrect.")
        self.assertEqual(observer.getNotifiedState().getName(),"Inactive","Initial state is incorrect.")

    """
    Test the Emergency Stop Button being pressed during the Stopped state.
    """
    def test_stoppedEmergencyButtonPressed(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Stopped")
        CuT.emergencyStopButtonPressed()
        self.assertEqual(CuT.getState().getName(),"Stopped","State is incorrect.")

    """
    Test the Emergency Stop Button being released during the Stopped state.
    """
    def test_stoppedEmergencyButtonReleased(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Stopped")
        CuT.emergencyStopButtonReleased()
        self.assertEqual(CuT.getState().getName(),"Inactive","State is incorrect.")

    """
    Test an id being swiped during the Stopped state.
    """
    def test_stoppedIdSwiped(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Stopped")
        CuT.idSwiped(self.testUser)
        self.assertEqual(CuT.getState().getName(),"Stopped","State is incorrect.")

    """
    Test an admin id being swiped during the Stopped state.
    """
    def test_stoppedAdminIdSwiped(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Stopped")
        CuT.idSwiped(self.testAdminUser)
        self.assertEqual(CuT.getState().getName(),"ToggleAccessTypePrompt","State is incorrect.")

    """
    Test the Emergency Stop Button being pressed during the Inactive state.
    """
    def test_inactiveEmergencyButtonPressed(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Inactive")
        CuT.emergencyStopButtonPressed()
        self.assertEqual(CuT.getState().getName(),"Stopped","State is incorrect.")

    """
    Test the Emergency Stop Button being released during the Inactive state.
    """
    def test_inactiveEmergencyButtonReleased(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Inactive")
        CuT.emergencyStopButtonReleased()
        self.assertEqual(CuT.getState().getName(),"Inactive","State is incorrect.")

    """
    Test an id being swiped during the Inactive state.
    """
    def test_inactiveIdSwiped(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Inactive")
        CuT.idSwiped(self.testUser)
        self.assertEqual(CuT.getState().getName(),"Active","State is incorrect.")

    """
    Test an unauthorized id being swiped during the Inactive state.
    """
    def test_inactiveUnauthorizedIdSwiped(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Inactive")
        CuT.idSwiped(self.testUnauthorizedUser)
        self.assertEqual(MessageManager.getMessage(),MessageManager.UNAUTHORIZED_MESSAGE,"Message is incorrect.")
        self.assertEqual(CuT.getState().getName(),"Inactive","State is incorrect.")

    """
    Test the Emergency Stop Button being pressed during the Active state.
    """
    def test_activeEmergencyButtonPressed(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Active")
        CuT.emergencyStopButtonPressed()
        self.assertEqual(CuT.getState().getName(),"Stopped","State is incorrect.")

    """
    Test the Emergency Stop Button being released during the Active state.
    """
    def test_activeEmergencyButtonReleased(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Active")
        CuT.emergencyStopButtonReleased()
        self.assertEqual(CuT.getState().getName(),"Active","State is incorrect.")

    """
    Test an id being swiped during the Active state.
    """
    def test_activeIdSwiped(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Active")
        CuT.idSwiped(self.testUser)
        self.assertEqual(CuT.getState().getName(),"Active","State is incorrect.")

    """
    Test an unauthorized id being swiped during the Active state.
    """
    def test_activeUnauthorizedIdSwiped(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Active")
        CuT.idSwiped(self.testUnauthorizedUser)
        self.assertEqual(MessageManager.getMessage(),MessageManager.UNAUTHORIZED_MESSAGE,"Message is incorrect.")
        self.assertEqual(CuT.getState().getName(),"Active","State is incorrect.")

    """
    Tests that the correct state is set if the session expires.
    """
    def test_sessionExpires(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("Active")
        CuT.idSwiped(self.testUser)
        self.assertEqual(CuT.getState().getName(),"Active","State is incorrect.")
        time.sleep(2)
        self.assertEqual(CuT.getState().getName(),"Inactive","State is incorrect.")

    """
    Test the Emergency Stop Button being pressed during the Toggle Access Type Prompt state.
    """
    def test_toggleAccessTypePromptEmergencyButtonPressed(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("ToggleAccessTypePrompt")
        CuT.emergencyStopButtonPressed()
        self.assertEqual(CuT.getState().getName(),"ToggleAccessTypePrompt","State is incorrect.")

    """
    Test the Emergency Stop Button being released during the Toggle Access Type Prompt state.
    """
    def test_toggleAccessTypePromptEmergencyButtonReleased(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("ToggleAccessTypePrompt")
        CuT.emergencyStopButtonReleased()
        self.assertEqual(CuT.getState().getName(),"ToggleAccessType","State is incorrect.")

    """
    Test an id being swiped during the Toggle Access Type Prompt state.
    """
    def test_toggleAccessTypePromptIdSwiped(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("ToggleAccessTypePrompt")
        CuT.idSwiped(self.testUser)
        self.assertEqual(CuT.getState().getName(),"Stopped","State is incorrect.")

    """
    Test the Emergency Stop Button being pressed during the Toggle Access Type state.
    """
    def test_toggleAccessTypeEmergencyButtonPressed(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("ToggleAccessType")
        CuT.emergencyStopButtonPressed()
        self.assertEqual(CuT.getState().getName(),"Stopped","State is incorrect.")

    """
    Test the Emergency Stop Button being released during the Toggle Access Type state.
    """
    def test_toggleAccessTypeEmergencyButtonReleased(self):
        CuT = StateManager.StateManager()

        CuT.setStateByName("ToggleAccessType")
        CuT.emergencyStopButtonReleased()
        self.assertEqual(CuT.getState().getName(),"ToggleAccessType","State is incorrect.")

    """
    Test an id being swiped during the Toggle Access Type state.
    """
    def test_toggleAccessTypeIdSwiped(self):
        CuT = StateManager.StateManager()

        # Set the initial state.
        state = CuT.states["ToggleAccessType"]
        CuT.setStateByName("ToggleAccessType")
        self.assertEqual(state.currentUser,None,"Initial user is incorrect.")

        # Swipe an id and assert the user and access type are correct.
        CuT.idSwiped(self.testUser)
        self.assertEqual(CuT.getState().getName(),"ToggleAccessType","State is incorrect.")
        self.assertEqual(state.currentUser,self.testUser.getId(),"User is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000000").getAccessType(),"AUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000001").getAccessType(),"UNAUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000002").getAccessType(),"ADMIN","User access type is incorrect.")
        self.testUser = DatabaseManager.getUser(self.testUser.getId())

        # Swipe an id and assert the user and access type are correct.
        CuT.idSwiped(self.testUser)
        self.assertEqual(CuT.getState().getName(),"ToggleAccessType","State is incorrect.")
        self.assertEqual(state.currentUser,self.testUser.getId(),"User is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000000").getAccessType(),"ADMIN","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000001").getAccessType(),"UNAUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000002").getAccessType(),"ADMIN","User access type is incorrect.")
        self.testUser = DatabaseManager.getUser(self.testUser.getId())

        # Swipe an id and assert the user and access type are correct.
        CuT.idSwiped(self.testUser)
        self.assertEqual(CuT.getState().getName(),"ToggleAccessType","State is incorrect.")
        self.assertEqual(state.currentUser,self.testUser.getId(),"User is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000000").getAccessType(),"UNAUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000001").getAccessType(),"UNAUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000002").getAccessType(),"ADMIN","User access type is incorrect.")
        self.testUser = DatabaseManager.getUser(self.testUser.getId())

        # Swipe an id and assert the user and access type are correct.
        CuT.idSwiped(self.testUser)
        self.assertEqual(CuT.getState().getName(),"ToggleAccessType","State is incorrect.")
        self.assertEqual(state.currentUser,self.testUser.getId(),"User is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000000").getAccessType(),"AUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000001").getAccessType(),"UNAUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000002").getAccessType(),"ADMIN","User access type is incorrect.")
        self.testUser = DatabaseManager.getUser(self.testUser.getId())

        # Swipe an id and assert the user and access type are correct.
        CuT.idSwiped(self.testUnauthorizedUser)
        self.assertEqual(CuT.getState().getName(),"ToggleAccessType","State is incorrect.")
        self.assertEqual(state.currentUser,self.testUnauthorizedUser.getId(),"User is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000000").getAccessType(),"AUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000001").getAccessType(),"UNAUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000002").getAccessType(),"ADMIN","User access type is incorrect.")

        # Swipe an id and assert the user and access type are correct.
        CuT.idSwiped(self.testAdminUser)
        self.assertEqual(CuT.getState().getName(),"ToggleAccessType","State is incorrect.")
        self.assertEqual(state.currentUser,self.testAdminUser.getId(),"User is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000000").getAccessType(),"AUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000001").getAccessType(),"UNAUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000002").getAccessType(),"ADMIN","User access type is incorrect.")

        # Swipe an id and assert the user and access type are correct.
        CuT.idSwiped(self.testAdminUser)
        self.assertEqual(CuT.getState().getName(),"ToggleAccessType","State is incorrect.")
        self.assertEqual(state.currentUser,self.testAdminUser.getId(),"User is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000000").getAccessType(),"AUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000001").getAccessType(),"UNAUTHORIZED","User access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000002").getAccessType(),"UNAUTHORIZED","User access type is incorrect.")



"""
Runs the unit tests.
"""
def main():
    unittest.main()

# Run the tests.
if __name__ == '__main__':
    main()