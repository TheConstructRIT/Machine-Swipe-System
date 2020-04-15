"""
Zachary Cook

Unit tests for the User module.
"""

import unittest

from Model import User


"""
Test the User class.
"""
class TestUserClass(unittest.TestCase):
	"""
	Tests the constructor.
	"""
	def test_constructor(self):
		User.User("TestHash",100)

	"""
	Tests the getHashedId method.
	"""
	def test_getHashedId(self):
		CuT = User.User("TestHash",100)
		self.assertEqual(CuT.getHashedId(),"TestHash","Incorrect hash stored.")

	"""
	Tests the getSessionTime method.
	"""
	def test_getSessionTime(self):
		CuT = User.User("TestHash",100)
		self.assertEqual(CuT.getSessionTime(),100,"Incorrect max session time stored.")


"""
Test the static methods.
"""
class TestStaticMethods(unittest.TestCase):
	"""
	Test the getHashFromId method.
	"""
	def test_getHashFromId(self):
		self.assertEqual(User.getHashFromId(565000953),"b63205aee6692d81a2f326682c2e4aea370aec10d34e79231ef63e75f6614226","Hash is incorrect.")



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()