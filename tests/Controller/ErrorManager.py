"""
Zachary Cook

Unit tests for the ErrorManager.
"""

import unittest
from Controller import MessageManager, Observer

"""
Test the ErrorManager class.
"""
class TestErrorManagerClass(unittest.TestCase):
	"""
	Tests the constructor.
	"""
	def test_constructor(self):
		MessageManager.MessageManager()

	"""
	Tests the getErrorMessage method.
	"""
	def test_getErrorMessage(self):
		CuT = MessageManager.MessageManager()
		self.assertEqual(CuT.getMessage(),"","Initial message is incorrect.")

	"""
	Tests the sendErrorMessage method.
	"""
	def test_sendErrorMessage(self):
		CuT = MessageManager.MessageManager()

		# Create an observer.
		class MessageObserver(Observer.Observer):
			def notify(self,*args):
				self.observedMessage = args[0]

			def getNotifiedMessage(self):
				return self.observedMessage

		observer = MessageObserver()
		CuT.register(observer)
		CuT.sendMessage("Test error")
		self.assertEqual(CuT.getMessage(),"Test error","Current error is incorrect.")
		self.assertEqual(observer.getNotifiedMessage(),"Test error","Current error is incorrect.")



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()