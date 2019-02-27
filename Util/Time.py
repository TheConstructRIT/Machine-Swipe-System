"""
Zachary Cook

Handles time utilities.
"""

import time



# Returns the current timestamp as a float.
def getCurrentTimestamp():
	return time.time()

# Formats seconds to a time string a H:MM:SS.
def formatTime(seconds):
	seconds = int(seconds)

	# Calculate the individual hours, minutes, and seconds.
	hours = int(seconds / 3600)
	minutes = int(seconds / 60) % 60
	seconds = seconds % 60

	# Format the hours, minutes, and seconds.
	formattedSeconds = str(seconds).zfill(2)
	formattedMinutes = str(minutes).zfill(2)
	formattedHours = str(hours).zfill(2)

	# Format the time.
	return formattedHours + ":" + formattedMinutes + ":" + formattedSeconds