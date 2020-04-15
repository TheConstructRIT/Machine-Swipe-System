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
		User.User("000000000",100)

	"""
	Tests the getId method.
	"""
	def test_getHashedId(self):
		CuT = User.User("000000000",100)
		self.assertEqual(CuT.getId(),"000000000","Incorrect id stored.")

	"""
	Tests the getSessionTime method.
	"""
	def test_getSessionTime(self):
		CuT = User.User("000000000",100)
		self.assertEqual(CuT.getSessionTime(),100,"Incorrect max session time stored.")



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()