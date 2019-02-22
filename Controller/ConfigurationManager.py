"""
Zachary Cook

Manages reads to the configuration. Does not have a class implementation.
"""

# The location of the configuration file.
CONFIGURATION_FILE_LOCATION = "../configuration.json"



import json



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
Returns the internal name for the machine. This is used for interfacing
with the databases for determining the length of sessions.
"""
def getMachineInternalName():
	return readSetting("InternalName")

"""
Returns the display name for the machine.
"""
def getMachineName():
	return readSetting("DisplayName")

"""
Returns the default session time. This is used when the server is
unreachable. If it is less than or equal to 0, the machine will
be disabled when the server is unreachable.
"""
def getDefaultSessionTime():
	return readSetting("DefaultSessionTime")

"""
Returns the server endpoint.
"""
def getServerEndpoint():
	return readSetting("ServerEndpoint")

"""
Returns the time (in seconds) left in a session for the buzzer
to alarm. If the time is less than 0, the alarm will be disabled.
If the time is 0, then the alarm will be played when a session
expired. If the time is greater than the session time, the alarm
will be activated at the start of the session.
"""
def getWarningAlarmActivationTime():
	return readSetting("AlarmActivationTime")