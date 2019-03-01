"""
Zachary Cook

Emulates the hardware for testing.
"""

import turtle
import time

from Controller import Observer
from Hardware import HardwareController
from Model import ScrollingText



# The id buttons to create.
SWIPE_IDS = [
	"000000001",
	"000000002",
]



"""
Mock class for the screen.
"""
class MockScreen():
	"""
	Creates the mock screen.
	"""
	def __init__(self):
		self.lines = [
			ScrollingText.ScrollingText("",self.getLineLength(),0.1,"*"),
			ScrollingText.ScrollingText("",self.getLineLength(),0.1," "),
			ScrollingText.ScrollingText("",self.getLineLength(),0.1," "),
			ScrollingText.ScrollingText("",self.getLineLength(),0.1," "),
		]

	"""
	Returns the max line length.
	"""
	def getLineLength(self):
		return 20

	"""
	Sets the text for a line.
	"""
	def setLineText(self,lineNumber,message):
		self.lines[lineNumber] = ScrollingText.ScrollingText(message,20,0.1,(lineNumber == 0 and "*" or " "))

	"""
	Returns all of the lines as text separated by lines.
	"""
	def getText(self):
		return self.lines[0].getCurrentText() + "\n" + self.lines[1].getCurrentText() + "\n" + self.lines[2].getCurrentText() + "\n" + self.lines[3].getCurrentText()

"""
Mock class for the LEDs.
"""
class MockLEDs():
	"""
	Creates the mock LEDs.
	"""
	def __init__(self):
		self.currentColor = "Yellow"

	"""
	Sets the color.
	"""
	def setColor(self,colorName):
		self.currentColor = colorName

	"""
	Returns the color.
	"""
	def getColor(self):
		return self.currentColor

"""
Mock class for the card reader.
"""
class MockCardReader(Observer.Observable):
	"""
	Swipes an id.
	"""
	def swipeId(self,id):
		self.notify(id)

"""
Mock class for the emergency stop.
"""
class MockEmergencyStopButton(Observer.Observable):
	"""
	Creates the mock button.
	"""
	def __init__(self):
		super().__init__()
		self.pressed = True

	"""
	Toggles the button.
  	"""
	def toggleButton(self):
		self.pressed = not self.pressed
		self.notify(self.pressed)

	"""
	Returns if the button is pressed.
	"""
	def isPressed(self):
		return self.pressed

"""
Window used for displaying the demo.
"""
class TestWindow():
	"""
	Creates the window.
	"""
	def __init__(self):
		# Create the window.
		self.window = turtle.Screen()
		self.window.screensize(400,200)
		self.window.tracer(0)

		# Set up the turtle.
		self.turtle = turtle.Turtle()
		self.turtle.hideturtle()
		self.turtle.up()

		# Set up clicking.
		self.clickRegions = []
		def onClick(x,y):
			# Iterate and invoke the regions.
			for regionData in self.clickRegions:
				posX,posY = regionData[0],regionData[1]
				sizeX,sizeY = regionData[2],regionData[3]

				# Invoke the callback if the mouse is in the region.
				if x >= posX and x <= posX + sizeX and y >= posY - sizeY and y <= posY:
					regionData[4]()

		self.window.onclick(onClick)

	"""
	Registers a click region.
	"""
	def registerClick(self,posX,posY,sizeX,sizeY,callback):
		self.clickRegions.append([posX,posY,sizeX,sizeY,callback])

	"""
	Updates the window.
	"""
	def update(self):
		self.window.update()

	"""
	Draws a rectangle.
	"""
	def drawRectangle(self,posX,posY,sizeX,sizeY,borderColor,backgroundColor):
		# Set the color.
		self.turtle.pencolor(borderColor)
		self.turtle.fillcolor(backgroundColor)

		# Draw the rectangle.
		self.turtle.goto(posX,posY)
		self.turtle.down()
		self.turtle.begin_fill()
		self.turtle.goto(posX + sizeX,posY)
		self.turtle.goto(posX + sizeX,posY - sizeY)
		self.turtle.goto(posX,posY - sizeY)
		self.turtle.goto(posX,posY)
		self.turtle.end_fill()
		self.turtle.up()

	"""
	Draws text.
	"""
	def drawText(self,text,posX,posY,color = "#000000"):
		# Set the color.
		self.turtle.pencolor(color)

		# Write the text.
		self.turtle.goto(posX,posY)
		self.turtle.down()
		self.turtle.write(text,font=("Courier New",24))
		self.turtle.up()

"""
Creates a GUI for emulating the hardware. The key switch is not
emulated because it has no interaction with the software.
"""
class Emulator():
	"""
	Creates the emulator.
	"""
	def __init__(self):
		# Create the mock hardware.
		mockScreen = MockScreen()
		self.mockScreen = mockScreen
		mockLEDs = MockLEDs()
		self.mockLEDs = mockLEDs
		mockCardReader = MockCardReader()
		self.mockCardReader = mockCardReader
		mockEmergencyStopButton = MockEmergencyStopButton()
		self.mockEmergencyStopButton = mockEmergencyStopButton

		# Create the hardware controller.
		controller = HardwareController.HardwareController(mockScreen,mockLEDs,mockCardReader,mockEmergencyStopButton)
		self.controller = controller

		# Create the display.
		self.createDisplay()

		# Start updating.
		self.startUpdateLoop()

	"""
	Initializes the display.
	"""
	def createDisplay(self):
		self.window = TestWindow()
		self.lastLEDColor = ""

		# Create the main display.
		self.lastText = ""
		self.window.drawRectangle(-400,200,800,400,"#000000","#FFFFFF")

		# Create the the emergency stop button.
		self.window.drawText("Toggle E-Stop",120,80)
		self.window.drawRectangle(160,80,160,160,"#FFFFFF","#FF0000")

		def emergencyStopPressed():
			self.mockEmergencyStopButton.toggleButton()
		self.window.registerClick(160,80,160,160,emergencyStopPressed)

		# Create the swipe buttons.
		i = -1
		for id in SWIPE_IDS:
			i += 1
			posX,posY = -160,-210 - (40 * i)

			# Create the button.
			self.window.drawRectangle(posX,posY,320,36,"#FFFFFF","#00FF00")
			self.window.drawText("Swipe " + id,posX + 20,posY - 36)

			# Create the callback.
			def swipeId():
				self.mockCardReader.swipeId(id)
			self.window.registerClick(posX,posY,320,36,swipeId)

	"""
	Updates the display.
	"""
	def updateDisplay(self):
		# Render the display if the text has changed.
		newText = self.mockScreen.getText()
		if newText != self.lastText:
			self.lastText = newText
			self.window.drawRectangle(-360,160,400,160,"#FFFFFF","#000000")
			self.window.drawText(newText,-350,8,"#0000FF")

		# Render the LEDs if the color has changed.
		newLEDColor = self.mockLEDs.getColor()
		if newLEDColor != self.lastLEDColor:
			self.lastLEDColor = newLEDColor
			self.window.drawRectangle(-310,-40,300,80,"#FFFFFF",newLEDColor)

		# Update the display.
		self.window.update()

	"""
	Continuously updates the display.
	"""
	def startUpdateLoop(self):
		while True:
			self.updateDisplay()
			time.sleep(0.05)



if __name__ == '__main__':
	Emulator()