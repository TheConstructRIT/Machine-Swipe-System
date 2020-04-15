"""
Zachary Cook

Manages calls to the databases.
"""

import sqlite3
from Controller import ConfigurationManager
from Model import User



"""
Class representing the database.
"""
class DatabaseManager:
	"""
	Creates a database manager.
	"""
	def __init__(self):
		self.database = sqlite3.connect("database.sqlite",check_same_thread=False)

		# Initialize the database.
		self.initializeTables()
		self.closeOldSessions()

	"""
	Initializes the tables if they aren't defined.
	"""
	def initializeTables(self):
		# Initialize the users table.
		try:
			self.database.execute("CREATE TABLE Users (Id char(9),Type STRING);")
			self.database.commit()
		except:
			pass

		# Initialize the users table.
		try:
			self.database.execute("CREATE TABLE Sessions (Id char(9),Start BIGINT,End BIGINT);")
			self.database.commit()
		except:
			pass

	"""
	Marks open sessions with a finish time of -1. This
	should only happen if there was power-lose during the operation
	of the system.
	"""
	def closeOldSessions(self):
		self.database.execute("UPDATE Sessions SET End = -1 WHERE END = 0;")
		self.database.commit()

	"""
	Returns the type of user.
	"""
	def getUserType(self,id):
		# Return the first result if it exists.
		results = self.database.execute("SELECT Type FROM Users WHERE Id = ?;",[id]).fetchall()
		if len(results) > 0:
			return results[0][0]

		# Return UNAUTHORIZED if there was no result.
		return "UNAUTHORIZED"

	"""
	Logs the session starting.
	"""
	def sessionStarted(self,session):
		self.database.execute("INSERT INTO Sessions VALUES (?,?,0);",[session.getUser().getId(),session.getStartTime()])
		self.database.commit()

	"""
	Logs the session ending.
	"""
	def sessionEnded(self,session):
		self.database.execute("UPDATE Sessions SET End = ? WHERE End = 0 AND Id = ? AND Start = ?;",[session.getEndTime(),session.getUser().getId(),session.getStartTime()])
		self.database.commit()





# Create a single instance of the database manager.
staticDatabaseManager = DatabaseManager()



"""
Returns the User for the given id (non-hash). If
there is no registered User, None is returned.
"""
def getUser(id):
	return User.User(id,ConfigurationManager.getDefaultSessionTime())

"""
Registers a session being started.
"""
def sessionStarted(session):
	staticDatabaseManager.sessionStarted(session)

"""
Registers a session ended.
"""
def sessionEnded(session):
	staticDatabaseManager.sessionEnded(session)