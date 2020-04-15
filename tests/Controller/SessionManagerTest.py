"""
Zachary Cook

Unit tests for the SessionManager.
"""

import unittest
import time
from Controller import SessionManager, Observer
from Model import User

"""
Test the SessionManager class.
"""
class TestSessionManagerClass(unittest.TestCase):
	"""
	Sets up the unit test.
	"""
	def setUp(self):
		self.testUser1 = User.User("000000000",1)
		self.testUser2 = User.User("000000001",1)

	"""
	Tests the constructor.
	"""
	def test_constructor(self):
		SessionManager.SessionManager()

	"""
	Tests the getCurrentSession method.
	"""
	def test_getCurrentSession(self):
		CuT = SessionManager.SessionManager()
		self.assertEqual(CuT.getCurrentSession(),None,"Initial session is incorrect.")

	"""
	Tests the startSession method.
	"""
	def test_startSession(self):
		CuT = SessionManager.SessionManager()

		# Create an observer.
		class SessionObserver(Observer.Observer):
			def notify(self,*args):
				self.observedSession = args[0]

			def getNotifiedSession(self):
				return self.observedSession

		observer = SessionObserver()
		CuT.register(observer)
		CuT.startSession(self.testUser1)
		self.assertEqual(CuT.getCurrentSession().getUser(),self.testUser1,"Current session is incorrect.")
		self.assertEqual(observer.getNotifiedSession().getUser(),self.testUser1,"Current session is incorrect.")
		CuT.startSession(self.testUser2)
		self.assertEqual(CuT.getCurrentSession().getUser(),self.testUser2,"Current session is incorrect.")
		self.assertEqual(observer.getNotifiedSession().getUser(),self.testUser2,"Current session is incorrect.")

	"""
	Tests the endSession method.
	"""
	def test_setSession(self):
		CuT = SessionManager.SessionManager()

		# Create an observer.
		class SessionObserver(Observer.Observer):
			def notify(self,*args):
				self.observedSession = args[0]

			def getNotifiedSession(self):
				return self.observedSession

		observer = SessionObserver()
		CuT.register(observer)
		CuT.startSession(self.testUser1)
		CuT.endSession()
		self.assertEqual(CuT.getCurrentSession(),None,"Current session is incorrect.")
		self.assertEqual(observer.getNotifiedSession(),None,"Current session is incorrect.")

	"""
	Tests that sessions can expire.
	"""
	def test_sessionExpires(self):
		CuT = SessionManager.SessionManager()

		# Create an observer.
		class SessionObserver(Observer.Observer):
			def notify(self, *args):
				self.observedSession = args[0]

			def getNotifiedSession(self):
				return self.observedSession

		observer = SessionObserver()
		CuT.register(observer)
		CuT.startSession(self.testUser1)
		CuT.getCurrentSession().sessionStart = 0
		time.sleep(0.2)
		self.assertEqual(CuT.getCurrentSession(),None,"Current session is incorrect.")
		self.assertEqual(observer.getNotifiedSession(),None,"Current session is incorrect.")



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()