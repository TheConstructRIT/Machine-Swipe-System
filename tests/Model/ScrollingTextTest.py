"""
Zachary Cook

Unit tests for the ScrollingText module.
"""

import unittest
import time

from Model import ScrollingText



"""
Test the ScrollingText class.
"""
class TestScrollingTextClass(unittest.TestCase):
	"""
	Tests the constructor.
	"""
	def test_constructor(self):
		ScrollingText.ScrollingText("Test",4,0.05)
		ScrollingText.ScrollingText("TestTest",4,0.05)

	"""
	Tests the constructor with centering.
	"""
	def test_constructorCentering(self):
		CuT = ScrollingText.ScrollingText("Test",8,0.05,"=")
		self.assertEqual(CuT.getCurrentText(),"==Test==","Message isn't centered.")

	"""
	Tests the textFits method.
	"""
	def test_textFits(self):
		CuT1 = ScrollingText.ScrollingText("Test",4,0.05)
		CuT2 = ScrollingText.ScrollingText("TestTest",4,0.05)

		self.assertTrue(CuT1.textFits(),"Text does not fit.")
		self.assertFalse(CuT2.textFits(),"Text does fit.")

	"""
	Tests the getCurrentOffset method.
	"""
	def test_getCurrentOffset(self):
		CuT1 = ScrollingText.ScrollingText("Test",4,0.05)
		CuT2 = ScrollingText.ScrollingText("TestTest",4,0.05)

		self.assertEqual(CuT1.getCurrentOffset(),0,"Offset is incorrect.")
		self.assertEqual(CuT2.getCurrentOffset(),0,"Offset is incorrect.")

		time.sleep(0.05)
		self.assertEqual(CuT1.getCurrentOffset(),0,"Offset is incorrect.")
		self.assertEqual(CuT2.getCurrentOffset(),1,"Offset is incorrect.")

		time.sleep(0.05)
		self.assertEqual(CuT1.getCurrentOffset(),0,"Offset is incorrect.")
		self.assertEqual(CuT2.getCurrentOffset(),2,"Offset is incorrect.")

		time.sleep(0.05)
		self.assertEqual(CuT1.getCurrentOffset(),0,"Offset is incorrect.")
		self.assertEqual(CuT2.getCurrentOffset(),3,"Offset is incorrect.")



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()