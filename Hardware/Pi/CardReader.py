"""
Zachary Cook

Class representing a card reader. Handles "key presses"
from the card ready.
"""

import select
import sys
import re

from Controller import Observer



"""
Class representing a card reader. Reads using stdin.
"""
class CardReader(Observer.Observable):
	"""
	Swipes an id.
	"""
	def swipeId(self,id):
		self.notify(id)

	"""
	Starts the update loop for reading swipes.
	"""
	def startPolling(self):
		while True:
			# Get the next line.
			if select.select([sys.stdin,],[],[],0.0)[0]:
				swipeInput = sys.stdin.readline()

				# Get the first id.
				entries = re.findall("\d+",swipeInput)
				if len(entries) >= 1:
					self.swipeId(entries[0])