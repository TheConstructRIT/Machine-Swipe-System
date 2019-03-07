"""
Zachary Cook

Initializes the system for the hardware deployment on a Raspberry Pi.
"""

from Hardware.Pi import Buzzer
from Hardware.Pi import CardReader
from Hardware.Pi import EmergencyStopButton
from Hardware.Pi import LCDScreen
from Hardware.Pi import LEDs
from Hardware.Pi import Relay
from Hardware import HardwareController



# Create the hardware objects.
screen = LCDScreen.Display()
leds = LEDs.LEDs()
cardReader = CardReader.CardReader()
emergencyStopButton = EmergencyStopButton.EmergencyStopButton()
buzzer = Buzzer.Buzzer()
relay = Relay.Relay()

# Create the controller.
hardwareController = HardwareController.HardwareController(screen,leds,cardReader,emergencyStopButton,buzzer,relay)

# Set up the swipe reader.
cardReader.startPolling()