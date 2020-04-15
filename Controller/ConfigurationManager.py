"""
Zachary Cook

Manages reads to the configuration. Does not have a class implementation.
"""

import os
import json


# The location of the configuration file.
BASE_DIRECTORY = os.path.realpath(__file__) + "/../../"
CONFIGURATION_FILE_LOCATION = os.path.realpath(BASE_DIRECTORY + "configuration.json")



"""
Reads and parses the JSON configuration.
"""
def getJSONConfiguration():
	# Read the file.
	file = open(CONFIGURATION_FILE_LOCATION)
	lines = file.read()
	file.close()

	# Parse the JSON.
	return json.loads(lines)

"""
Reads a configuration setting.
"""
def readSetting(settingName):
	return getJSONConfiguration()[settingName]



"""
Returns the display name for the machine.
"""
def getMachineName():
	return readSetting("DisplayName")

"""
Returns the default session time.
"""
def getDefaultSessionTime():
	return readSetting("DefaultSessionTime")

"""
Returns the time (in seconds) left in a session for the buzzer
to alarm. If the time is less than 0, the alarm will be disabled.
If the time is 0, then the alarm will be played when a session
expired. If the time is greater than the session time, the alarm
will be activated at the start of the session.
"""
def getWarningAlarmActivationTime():
	return readSetting("AlarmActivationTime")