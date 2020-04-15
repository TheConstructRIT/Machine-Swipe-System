"""
Zachary Cook

Unit tests for the StateManager.
"""

import unittest
import time
from Controller import StateManager, Observer
from Model import User

"""
Test the SessionManager class.
"""
class TestStateManagerClass(unittest.TestCase):
	"""
	Sets up the unit test.
	"""
	def setUp(self):
		self.testUser = User.User("000000000",1)

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
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()