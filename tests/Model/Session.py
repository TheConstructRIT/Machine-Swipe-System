"""
Zachary Cook

Unit tests for the Session module.
"""

import unittest

from Model import User
from Model import Session



"""
Test the Session class.
"""
class TestSessionClass(unittest.TestCase):
	"""
	Sets up the unit test.
	"""
	def setUp(self):
		self.testUser = User.User("TestHash","Test Name",20)

	"""
	Tests the constructor.
	"""
	def test_constructor(self):
		Session.Session(self.testUser,50)

	"""
	Tests the getSessionTime method.
	"""
	def test_getSessionTime(self):
		CuT = Session.Session(self.testUser,50)
		self.assertEqual(CuT.getSessionTime(),20,"Session time is incorrect.")

	"""
	Tests the getStartTime method.
	"""
	def test_getStartTime(self):
		CuT = Session.Session(self.testUser,50)
		self.assertEqual(CuT.getStartTime(),50,"Start time is incorrect.")

	"""
	Tests the getSessionTime method.
	"""
	def test_getEndTime(self):
		CuT = Session.Session(self.testUser,50)
		self.assertEqual(CuT.getEndTime(),70,"End time is incorrect.")



"""
Test the static methods.
"""
class TestStaticMethods(unittest.TestCase):
	"""
	Sets up the unit test.
	"""
	def setUp(self):
		self.testUser = User.User("TestHash", "Test Name", 20)

	"""
	Test the startSession method.
	"""
	def test_startSession(self):
		CuT = Session.startSession(self.testUser)
		self.assertEqual(CuT.getUser(),self.testUser,"User is incorrect.")
		self.assertNotEqual(CuT.getStartTime(),0,"Start time is incorrect.")
		self.assertAlmostEqual(CuT.getEndTime() - CuT.getStartTime(),20,"Delta time is incorrect.",0.1)



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()