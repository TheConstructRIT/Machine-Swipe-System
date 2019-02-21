"""
Zachary Cook

Unit tests for the LockableBuffer module.
"""

import unittest

from Model import LockableBuffer


"""
Test the LockableBuffer class.
"""
class TestLockableBufferClass(unittest.TestCase):
	"""
	Tests the constructor.
	"""
	def test_constructor(self):
		CuT = LockableBuffer.LockableBuffer(3)
		self.assertEqual(CuT.getBufferString(),"","Buffer not empty.")

	"""
	Tests the append method.
	"""
	def test_append(self):
		CuT = LockableBuffer.LockableBuffer(3)
		CuT.append("1")
		self.assertEqual(CuT.getBufferString(),"1","Buffer is incorrect.")

		CuT.append("2")
		CuT.append("3")
		self.assertEqual(CuT.getBufferString(),"123","Buffer is incorrect.")

		CuT.append("4")
		self.assertEqual(CuT.getBufferString(),"234","Buffer is incorrect.")

	"""
	Tests the append method with non-characters.
	"""

	def test_appendCharacters(self):
		CuT = LockableBuffer.LockableBuffer(3)
		CuT.append("123")
		self.assertEqual(CuT.getBufferString(), "123", "Buffer is incorrect.")

		CuT.append("456")
		CuT.append("789")
		self.assertEqual(CuT.getBufferString(), "123456789", "Buffer is incorrect.")

		CuT.append("abc")
		self.assertEqual(CuT.getBufferString(), "456789abc", "Buffer is incorrect.")

	"""
	Tests the lock and unlock methods.
	"""
	def test_lockAndUnlock(self):
		CuT = LockableBuffer.LockableBuffer(3)
		CuT.append("1")
		CuT.append("2")
		self.assertEqual(CuT.getBufferString(),"12","Buffer is incorrect.")

		CuT.lock()
		CuT.append("3")
		self.assertEqual(CuT.getBufferString(),"12","Buffer is incorrect.")

		CuT.unlock()
		CuT.append("4")
		self.assertEqual(CuT.getBufferString(),"124","Buffer is incorrect.")

	"""
	Tests the clear method.
	"""
	def test_clear(self):
		CuT = LockableBuffer.LockableBuffer(3)
		CuT.append("1")
		CuT.append("2")
		CuT.clear()
		self.assertEqual(CuT.getBufferString(),"","Buffer not cleared.")



"""
Runs the unit tests.
"""
def main():
	unittest.main()

# Run the tests.
if __name__ == '__main__':
	main()