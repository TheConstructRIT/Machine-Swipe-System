"""
Zachary Cook

Class representing the LCD screen.
If there is a FileNotFoundError, make sure that I2C is enabled
using "sudo raspi-config" > "5 Interfacing Options" > Enable SPI and I2C

Modified from: http://hardware-libre.fr/2014/03/en-raspberry-pi-using-a-4x20-characters-display/
"""

import time
import threading

from Hardware.Pi.LowLevel import I2C
from Model import ScrollingText



# LCD Address
ADDRESS = 0x27

# Commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Flags for display entry mode.
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Flags for display on/off control.
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# Flags for display/cursor shift.
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# Flags for function set.
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Flags for backlight control.
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100 # Enable bit
Rw = 0b00000010 # Read/Write bit
Rs = 0b00000001 # Register select bit

"""
Class representing a 20x4 LCD display.
"""
class LCD:
	"""
	Creates the LCD display.
	"""
	def __init__(self):
		self.lcdDevice = I2C.I2C(ADDRESS)
		self.lines = ["","","",""]

		self.lcdWrite(0x03)
		self.lcdWrite(0x03)
		self.lcdWrite(0x03)
		self.lcdWrite(0x02)

		self.lcdWrite(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
		self.lcdWrite(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
		self.lcdWrite(LCD_CLEARDISPLAY)
		self.lcdWrite(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
		time.sleep(0.2)

	"""
	Strobes the display.
	"""
	def lcdStrobe(self, data):
		self.lcdDevice.writeCommand(data | En | LCD_BACKLIGHT)
		time.sleep(0.0005)
		self.lcdDevice.writeCommand(((data & ~En) | LCD_BACKLIGHT))
		time.sleep(0.0001)

	"""
	Writes 4 bits to the LCD.
	"""
	def lcdWriteFourBits(self,data):
		self.lcdDevice.writeCommand(data | LCD_BACKLIGHT)
		self.lcdStrobe(data)

	"""
	Writes a command to the LCD.
	"""
	def lcdWrite(self,command,mode=0):
		self.lcdWriteFourBits(mode | (command & 0xF0))
		self.lcdWriteFourBits(mode | ((command << 4) & 0xF0))

	"""
	Writes a string.
	"""
	def lcdDisplayString(self,message,line):
		# Adjust the message.
		message = str(message) + (" " * 20)
		message = message[:20]

		# Write the line to change.
		if line == 1:
			self.lcdWrite(0x80)
		elif line == 2:
			self.lcdWrite(0xC0)
		elif line == 3:
			self.lcdWrite(0x94)
		elif line == 4:
			self.lcdWrite(0xD4)

		# Write the character.
		for char in message:
			self.lcdWrite(ord(char),Rs)

	"""
	Clears the screen.
	"""
	def lcdClear(self):
		self.lcdWrite(LCD_CLEARDISPLAY)
		self.lcdWrite(LCD_RETURNHOME)

	"""
	Displays the lines.
	"""
	def writeLines(self):
		for line,message in enumerate(self.lines):
			self.lcdDisplayString(message,line + 1)




"""
Class representing a display.
"""
class Display():
	"""
	Creates a display instance.
	"""
	def __init__(self):
		# Set up the hardware.
		self.lcd = LCD()
		self.lcd.lcdClear()

		# Set up the messages.
		self.lines = [
			ScrollingText.ScrollingText("",self.getLineLength(),0.1,"*",10),
			ScrollingText.ScrollingText("",self.getLineLength(),0.1,"*",10),
			ScrollingText.ScrollingText("",self.getLineLength(),0.1,"*",10),
			ScrollingText.ScrollingText("",self.getLineLength(),0.1,"*",10),
		]

		# Set up the queue.
		self.lastLinesWritten = ["","","",""]

		# Start updating the screen.
		self.startUpdating()

	"""
	Returns the line length for the screen.
	"""
	def getLineLength(self):
		return 20

	"""
	Sets the text for the given line.
	"""
	def setLineText(self,lineNumber,message):
		# Set the line.
		scrollingMessage = ScrollingText.ScrollingText(message,self.getLineLength(),0.1,(lineNumber == 0 and "*" or " "),10)
		self.lines[lineNumber] = scrollingMessage

		# Update the lines.
		# self.lcd.lcdDisplayString(scrollingMessage.getCurrentText(),lineNumber + 1)
		# self.update()

	"""
	Updates the displayed line. Does not force update it
	if the line hasn't changed.
	"""
	def updateLine(self,lineNumber):
		# Determine the previous and new line.
		previousLine = self.lastLinesWritten[lineNumber]
		newLine = self.lines[lineNumber].getCurrentText()

		# Update the line if it has changed.
		if previousLine != newLine:
			self.lastLinesWritten[lineNumber] = newLine
			self.lcd.lcdDisplayString(newLine,lineNumber + 1)

	"""
	Updates what is displayed.
	"""
	def update(self):
		self.lcd.lines = [
			self.lines[0].getCurrentText(),
			self.lines[1].getCurrentText(),
			self.lines[2].getCurrentText(),
			self.lines[3].getCurrentText(),
		]
		self.lcd.writeLines()

	"""
	Starts a thread for running the update queue.
	"""
	def startUpdating(self):
		# Runs the update loop.
		def startUpdateLoop():
			while True:
				# Update the lines if the update is queued.
				for lineNumber in range(0,4):
					self.updateLine(lineNumber)

				# Sleep for a bit.
				time.sleep(0.1)

		# Create and start a thread.
		threading.Thread(target=startUpdateLoop).start()