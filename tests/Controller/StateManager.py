"""
Zachary Cook

Unit tests for the StateManager.
"""

import unittest
from Controller import StateManager
from Model import User
from Util import Observer


"""
Test the User class.
"""
class TestStateManagerClass(unittest.TestCase):
	"""
	Sets up the unit test.
	"""
	def setUp(self):
		self.testUser = User.User("TestHash","Test Name",20)

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
Test the static methods.
"""
class TestStaticMethods(unittest.TestCase):
	"""
	Test the getStateManager method.
	"""
	def test_startSession(self):
		CuT = StateManager.getStateManager()
		self.assertTrue(isinstance(CuT,StateManager.StateManager),"Wrong type of object returned.")



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()