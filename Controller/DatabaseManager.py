"""
Zachary Cook

Manages calls to the databases.
"""

import sqlite3
from Controller import ConfigurationManager
from Model import Time,User



"""
Class representing the database.
"""
class DatabaseManager:
	"""
	Creates a database manager.
	"""
	def __init__(self,location="database.sqlite"):
		self.database = sqlite3.connect(location,check_same_thread=False)

		# Initialize the database.
		self.initializeTables()
		self.closeOldSessions()

	"""
	Initializes the tables if they aren't defined.
	"""
	def initializeTables(self):
		# Initialize the users table.
		try:
			self.database.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
			self.database.commit()
		except:
			pass

		# Initialize the users table.
		try:
			self.database.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
			self.database.commit()
		except:
			pass

	"""
	Marks open sessions with a finish time of -1. This
	should only happen if there was power-lose during the operation
	of the system.
	"""
	def closeOldSessions(self):
		self.database.execute("UPDATE Sessions SET EndTime = -1 WHERE EndTime = 0;")
		self.database.commit()

	"""
	Returns the type of user.
	"""
	def getUserAccessType(self,id):
		# Return the first result if it exists.
		results = self.database.execute("SELECT AccessType FROM Users WHERE Id = ?;",[id]).fetchall()
		if len(results) > 0:
			return results[0][0]

		# Return UNAUTHORIZED if there was no result.
		return "UNAUTHORIZED"

	"""
	Sets the access type of a user.
	"""
	def setUserAccessType(self,id,accessType):
		# If the access type is unauthorized, remove the user.
		if accessType == "UNAUTHORIZED":
			self.database.execute("DELETE FROM Users WHERE Id = ?;",[id])
			self.database.commit()
			return

		# Add or update the type if a record exists.
		if len(self.database.execute("SELECT * FROM Users WHERE Id = ?",[id]).fetchall()) > 0:
			self.database.execute("UPDATE Users SET AccessType = ? WHERE Id = ?;",[accessType,id])
		else:
			self.database.execute("INSERT INTO Users VALUES (?,?);",[id,accessType])
		self.database.commit()

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
		self.database.execute("UPDATE Sessions SET EndTime = ? WHERE EndTime = 0 AND Id = ? AND StartTime = ?;",[Time.getCurrentTimestamp(),session.getUser().getId(),session.getStartTime()])
		self.database.commit()



staticDatabaseManager = None

"""
Returns the static database instance.
"""
def getDatabase():
	# Create the static instance.
	global staticDatabaseManager
	if staticDatabaseManager is None:
		staticDatabaseManager = DatabaseManager()

	# Return the static database.
	return staticDatabaseManager


"""
Returns the User for the given id (non-hash). If
there is no registered User, None is returned.
"""
def getUser(id):
	accessType = getDatabase().getUserAccessType(id)
	if accessType == "UNAUTHORIZED":
		return User.User(id,0,accessType)
	else:
		return User.User(id,ConfigurationManager.getDefaultSessionTime(),accessType)

"""
Sets the access type of a user.
"""
def setUserAccessType(id,accessType):
	getDatabase().setUserAccessType(id,accessType)

"""
Registers a session being started.
"""
def sessionStarted(session):
	getDatabase().sessionStarted(session)

"""
Registers a session ended.
"""
def sessionEnded(session):
	getDatabase().sessionEnded(session)