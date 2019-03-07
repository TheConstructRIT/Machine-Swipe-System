"""
Zachary Cook

Class representing an I2C device.
Modified from: http://hardware-libre.fr/2014/03/en-raspberry-pi-using-a-4x20-characters-display/
"""

# Delay time for sending I2C signals.
I2C_SIGNAL_DELAY = 0.0001



import smbus
import time



"""
Class representing an I2C device.
"""
class I2C():
	"""
	Creates the I2C device.
	"""
	def __init__(self,address,port=1):
		self.address = address
		self.bus = smbus.SMBus(port)

	"""
	Writes a command.
	"""
	def writeCommand(self,command):
		self.bus.write_byte(self.address,command)
		time.sleep(I2C_SIGNAL_DELAY)

	"""
	Writes a command with arguments.
	"""
	def writeCommandAndArguments(self,command,data):
		self.bus.write_byte_data(self.address,command,data)
		time.sleep(I2C_SIGNAL_DELAY)

	"""
	Write a block of data.
	"""
	def writeBlockData(self,command,data):
		self.bus.write_block_data(self.address,command,data)
		time.sleep(I2C_SIGNAL_DELAY)

	"""
	Reads a byte of data.
	"""
	def read(self):
		return self.bus.read_byte(self.address)

	"""
	Reads data.
	"""
	def readData(self,command):
		return self.bus.read_byte_data(self.address,command)

	"""
	Reads a block of data.
	"""
	def readBlockData(self,command):
		return self.bus.read_block_data(self.address,command)