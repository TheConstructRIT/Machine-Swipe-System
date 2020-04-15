"""
Zachary Cook

Unit tests for the ScrollingText module.
"""

import unittest
from Model import ScrollingText



"""
Class that mocks the Time module.
"""
class MockTime:
	"""
	Creates the mock time.
	"""
	def __init__(self):
		self.time = 0

	# Returns the current timestamp as a float.
	def getCurrentTimestamp(self):
		return self.time

"""
Test the ScrollingText class.
"""
class TestScrollingTextClass(unittest.TestCase):
	"""
	Tests the constructor.
	"""
	def test_constructor(self):
		ScrollingText.ScrollingText("Test",4,0.2)
		ScrollingText.ScrollingText("TestTest",4,0.2)

	"""
	Tests the constructor with centering.
	"""
	def test_constructorCentering(self):
		CuT = ScrollingText.ScrollingText("Test",8,0.2,"=")
		self.assertEqual(CuT.getCurrentText(),"==Test==","Message isn't centered.")

	"""
	Tests the textFits method.
	"""
	def test_textFits(self):
		CuT1 = ScrollingText.ScrollingText("Test",4,0.2)
		CuT2 = ScrollingText.ScrollingText("TestTest",4,0.2)

		self.assertTrue(CuT1.textFits(),"Text does not fit.")
		self.assertFalse(CuT2.textFits(),"Text does fit.")

	"""
	Tests the getCurrentOffset method.
	"""
	def test_getCurrentOffset(self):
		ScrollingText.Time = MockTime()
		CuT1 = ScrollingText.ScrollingText("Test",4,0.2)
		CuT2 = ScrollingText.ScrollingText("TestTest",4,0.2)

		self.assertEqual(CuT1.getCurrentOffset(),0,"Offset is incorrect.")
		self.assertEqual(CuT2.getCurrentOffset(),0,"Offset is incorrect.")

		ScrollingText.Time.time = 0.25
		self.assertEqual(CuT1.getCurrentOffset(),0,"Offset is incorrect.")
		self.assertEqual(CuT2.getCurrentOffset(),1,"Offset is incorrect.")

		ScrollingText.Time.time = 0.45
		self.assertEqual(CuT1.getCurrentOffset(),0,"Offset is incorrect.")
		self.assertEqual(CuT2.getCurrentOffset(),2,"Offset is incorrect.")

		ScrollingText.Time.time = 0.65
		self.assertEqual(CuT1.getCurrentOffset(),0,"Offset is incorrect.")
		self.assertEqual(CuT2.getCurrentOffset(),3,"Offset is incorrect.")

	"""
	Tests the getCurrentText method.
	"""
	def test_getCurrentText(self):
		ScrollingText.Time = MockTime()
		CuT1 = ScrollingText.ScrollingText("Test",6,0.2,"*")
		CuT2 = ScrollingText.ScrollingText("Test1Test2",6,0.2," ",scrollingSpacing=2)

		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"Test1T","Text is incorrect.")

		ScrollingText.Time.time = 0.25
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"est1Te","Text is incorrect.")

		ScrollingText.Time.time = 0.45
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"st1Tes","Text is incorrect.")

		ScrollingText.Time.time = 0.65
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"t1Test","Text is incorrect.")

		ScrollingText.Time.time = 0.85
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"1Test2","Text is incorrect.")

		ScrollingText.Time.time = 1.05
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"Test2 ","Text is incorrect.")

		ScrollingText.Time.time = 1.25
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"est2  ","Text is incorrect.")

		ScrollingText.Time.time = 1.45
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"st2  T","Text is incorrect.")

		ScrollingText.Time.time = 1.65
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"t2  Te","Text is incorrect.")

		ScrollingText.Time.time = 1.85
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"2  Tes","Text is incorrect.")

		ScrollingText.Time.time = 2.05
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"  Test","Text is incorrect.")

		ScrollingText.Time.time = 2.25
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText()," Test1","Text is incorrect.")

		ScrollingText.Time.time = 2.45
		self.assertEqual(CuT1.getCurrentText(),"*Test*","Text is incorrect.")
		self.assertEqual(CuT2.getCurrentText(),"Test1T","Text is incorrect.")



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()