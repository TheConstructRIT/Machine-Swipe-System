"""
Zachary Cook

Controls the hardware and makes interactions with the system.
"""

import threading
import time

from Controller import ConfigurationManager
from Controller import Observer
from Controller import MessageManager
from Controller import SessionManager
from Controller import StateManager
from Controller import SwipeManager
from Model import Time



# Duration for error messages.
MESSAGE_DURATION = 5



"""
Observer for the card reader.
"""
class CardReaderObserver(Observer.Observer):
	"""
	Creates the observer.
	"""
	def __init__(self,hardwareController):
		self.hardwareController = hardwareController

	"""
	Notifies an observer.
	"""
	def notify(self,*args):
		self.hardwareController.idSwiped(args[0])

"""
Observer for the emergency stop button.
"""
class EmergencyStopButtonObserver(Observer.Observer):
	"""
	Creates the observer.
	"""
	def __init__(self,hardwareController):
		self.hardwareController = hardwareController

	"""
	Notifies an observer.
	"""
	def notify(self,*args):
		self.hardwareController.emergencyStopChanged(args[0])

"""
Observer for state changes.
"""
class StateObserver(Observer.Observer):
	"""
	Creates the observer.
	"""
	def __init__(self,hardwareController):
		self.hardwareController = hardwareController

	"""
	Notifies an observer.
	"""
	def notify(self,*args):
		self.hardwareController.stateChanged(args[0])

"""
Observer for message changes.
"""
class MessageObserver(Observer.Observer):
	"""
	Creates the observer.
	"""
	def __init__(self,hardwareController):
		self.hardwareController = hardwareController

	"""
	Notifies an observer.
	"""
	def notify(self,*args):
		self.hardwareController.messageChanged(args[0])

"""
Observer for session changes.
"""
class SessionObserver(Observer.Observer):
	"""
	Creates the observer.
	"""
	def __init__(self,hardwareController):
		self.hardwareController = hardwareController

	"""
	Notifies an observer.
	"""
	def notify(self,*args):
		self.hardwareController.sessionChanged(args[0])

"""
Thread for updating the time.
"""
class SessionTimer(threading.Thread):
	"""
	Creates the timer.
	"""
	def __init__(self,hardwareController):
		super().__init__()
		self.hardwareController = hardwareController
		self.lastTimeLeft = 0
		self.buzzerStartTime = ConfigurationManager.getWarningAlarmActivationTime()

	"""
	Updates the timer.
	"""
	def updateTime(self,session):
		if session is not None:
			# Update the remaining time.
			timeLeft = session.getRemainingTime()
			self.hardwareController.screen.setLineText(2,Time.formatTime(timeLeft) + " Remaining")

			# Display the time limit warning.
			currentTimeBelowLimit = timeLeft < self.buzzerStartTime
			lastTimeBelowLimit = self.lastTimeLeft < self.buzzerStartTime
			if lastTimeBelowLimit == False and currentTimeBelowLimit == True:
				self.hardwareController.displayMessage("Session expiring soon, extend session!",10)
				self.hardwareController.buzzer.pulseBuzzer(5,1)
				self.hardwareController.leds.pulseColor("Red",5,1)

			self.lastTimeLeft = timeLeft
		else:
			self.lastTimeLeft = 0



	"""
	Loop for the timer.
	"""
	def run(self):
		while True:
			self.updateTime(self.hardwareController.currentSession)
			time.sleep(0.5)

"""
Removes the current message after a given period of time.
"""
class MessageTimer(threading.Thread):
	"""
	Create the timer.
	"""
	def __init__(self,hardwareController,message,duration):
		super().__init__()
		self.hardwareController = hardwareController
		self.message = message
		self.duration = duration

	"""
	Removes the message if it hasn't changed.
	"""
	def run(self):
		time.sleep(self.duration)
		if self.hardwareController.currentMessage == self.message:
			self.hardwareController.messageChanged("")



"""
Class for the hardware controller.
"""
class HardwareController():
	"""
	Creates the hardware controller.
	"""
	def __init__(self,screen,leds,cardReader,emergencyStopButton,buzzer,relay):
		# Store the hardware.
		self.screen = screen
		self.leds = leds
		self.cardReader = cardReader
		self.emergencyStopButton = emergencyStopButton
		self.buzzer = buzzer
		self.relay = relay

		# Set up the observers.
		self.cardReader.register(CardReaderObserver(self))
		self.emergencyStopButton.register(EmergencyStopButtonObserver(self))
		StateManager.register(StateObserver(self))
		SessionManager.register(SessionObserver(self))
		MessageManager.register(MessageObserver(self))

		# Send the initial state for the e-stop.
		if self.emergencyStopButton.isPressed():
			StateManager.emergencyStopButtonPressed()
		else:
			StateManager.emergencyStopButtonReleased()

		# Set up the rest of the initial states.
		self.currentSession = None
		self.stateChanged(StateManager.getState())
		self.sessionChanged(None)
		self.messageChanged("")

		# Set up the timer threads.
		self.sessionTimerThread = SessionTimer(self)
		self.sessionTimerThread.start()

	"""
	Displays a message.
	"""
	def displayMessage(self,message,time=MESSAGE_DURATION):
		self.currentMessage = message

		# Set the message.
		self.screen.setLineText(3,message)

		# Create a timer to remove the message.
		if message != "":
			MessageTimer(self,message,time).start()

	"""
	Handles the state being changed.
	"""
	def stateChanged(self,newState):
		# Get the name of the state.
		stateName = newState.getName().upper()

		# Set the text.
		self.screen.setLineText(0,stateName)
		if stateName == "STOPPED":
			self.screen.setLineText(1,"E-Stop is active")
			self.screen.setLineText(2,"")
		elif stateName == "INACTIVE":
			self.screen.setLineText(1,"Ready to swipe")
			self.screen.setLineText(2,"")

		# Set the LED color.
		if stateName == "STOPPED":
			self.leds.setColor("Red")
		elif stateName == "INACTIVE":
			self.leds.setColor("Yellow")
		elif stateName == "ACTIVE":
			self.leds.setColor("Green")

	"""
	Handles the session being changed.
	"""
	def sessionChanged(self,newSession):
		lastSession = self.currentSession
		self.currentSession = newSession

		# Set the text if the session exists.
		if newSession is not None:
			self.screen.setLineText(1,ConfigurationManager.getMachineName())
			self.sessionTimerThread.updateTime(newSession)

			# Display the started or extended message.
			if lastSession is None:
				self.messageChanged("Started session")
				self.buzzer.pulseBuzzer(2)
				self.leds.pulseColor("Red",2)
			else:
				if lastSession.getUser().getHashedId() == newSession.getUser().getHashedId():
					self.messageChanged("Extended session")
					self.buzzer.pulseBuzzer(2)
					self.leds.pulseColor("Yellow",2)
				else:
					self.messageChanged("Started session")
					self.buzzer.pulseBuzzer(2)
					self.leds.pulseColor("Yellow",2)

			# Set the relay as active.
			self.relay.setActive(True)
		else:
			self.relay.setActive(False)

	"""
	Handles the message being changed.
	"""
	def messageChanged(self,newMessage):
		self.displayMessage(newMessage)

		# Handle the message being changed.
		if newMessage == MessageManager.EMERGENCY_STOP_PRESSED_WARNING or newMessage == MessageManager.UNREGISTERED_USER_MESSAGE or newMessage == MessageManager.UNAUTHORIZED_MESSAGE:
			self.buzzer.pulseBuzzer(3)
			self.leds.pulseColor("Red",3)

	"""
	Handles an id being swiped.
	"""
	def idSwiped(self,id):
		SwipeManager.idSwiped(id)

	"""
	Handles the emergency stop being pressed or released.
	"""
	def emergencyStopChanged(self,pressed):
		if pressed:
			StateManager.emergencyStopButtonPressed()
		else:
			StateManager.emergencyStopButtonReleased()
