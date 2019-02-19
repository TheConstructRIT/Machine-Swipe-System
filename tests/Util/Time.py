"""
Zachary Cook

Unit tests for the Timemodule.
"""

import unittest

from Util import Time



"""
Test the static methods.
"""
class TestStringMethods(unittest.TestCase):
	"""
	Test the formatTime method.
	"""
	def test_formatTime(self):
		self.assertEqual(Time.formatTime((0 * 60 * 60) + (0 * 60) + 0),"00:00:00","Time is incorrect.")
		self.assertEqual(Time.formatTime((0 * 60 * 60) + (0 * 60) + 5),"00:00:05","Time is incorrect.")
		self.assertEqual(Time.formatTime((0 * 60 * 60) + (5 * 60) + 15),"00:05:15","Time is incorrect.")
		self.assertEqual(Time.formatTime((5 * 60 * 60) + (15 * 60) + 15),"05:15:15","Time is incorrect.")



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()