"""
Zachary Cook

Unit tests for the ErrorManager.
"""

import unittest
from Controller import ErrorManager
from Util import Observer


"""
Test the ErrorManager class.
"""
class TestErrorManagerClass(unittest.TestCase):
	"""
	Tests the constructor.
	"""
	def test_constructor(self):
		ErrorManager.ErrorManager()

	"""
	Tests the getErrorMessage method.
	"""
	def test_getErrorMessage(self):
		CuT = ErrorManager.ErrorManager()
		self.assertEqual(CuT.getErrorMessage(),"","Initial error message is incorrect.")

	"""
	Tests the sendErrorMessage method.
	"""
	def test_sendErrorMessage(self):
		CuT = ErrorManager.ErrorManager()

		# Create an observer.
		class MessageObserver(Observer.Observer):
			def notify(self,*args):
				self.observedMessage = args[0]

			def getNotifiedMessage(self):
				return self.observedMessage

		observer = MessageObserver()
		CuT.register(observer)
		CuT.sendErrorMessage("Test error")
		self.assertEqual(CuT.getErrorMessage(),"Test error","Current error is incorrect.")
		self.assertEqual(observer.getNotifiedMessage(),"Test error","Current error is incorrect.")



"""
Test the static methods.
"""
class TestStaticMethods(unittest.TestCase):
	"""
	Test the getErrorManager method.
	"""
	def test_getErrorManager(self):
		CuT = ErrorManager.getErrorManager()
		self.assertTrue(isinstance(CuT,ErrorManager.ErrorManager),"Wrong type of object returned.")



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()