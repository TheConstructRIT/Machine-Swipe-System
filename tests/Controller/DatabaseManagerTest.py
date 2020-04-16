"""
Zachary Cook

Unit tests for the DatabaseManager.
"""

import unittest
import tempfile
import sqlite3
from Controller import DatabaseManager
from Model import Session,User

"""
Test the DatabaseManager class.
"""
class TestDatabaseManagerClass(unittest.TestCase):
    """
    Sets up the unit test.
    """
    def setUp(self):
        # Create a temporary file for the database.
        databaseFile = tempfile.TemporaryFile()
        self.databaseFile = databaseFile.name
        databaseFile.close()
        del databaseFile

        # Create the database.
        self.initialDatabase = sqlite3.connect(self.databaseFile)

    """
    Tests the constructor with an uninitialized database.
    """
    def test_uninitializedDatabase(self):
        # Close the initial database.
        self.initialDatabase.close()

        # Create the database and assert the tables exist by running queries without errors.
        CuT = DatabaseManager.DatabaseManager(self.databaseFile)
        CuT.database.execute("SELECT * FROM Users;")
        CuT.database.execute("SELECT * FROM Sessions;")

    """
    Tests the constructor with an initialized database.
    """
    def test_initializedDatabase(self):
        # Initialize and close the initial database.
        self.initialDatabase.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
        self.initialDatabase.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
        self.initialDatabase.commit()
        self.initialDatabase.close()

        # Create the database and assert the tables exist by running queries without errors.
        CuT = DatabaseManager.DatabaseManager(self.databaseFile)
        CuT.database.execute("SELECT * FROM Users;")
        CuT.database.execute("SELECT * FROM Sessions;")

    """
    Tests the constructor with an initialized database with sessions.
    """
    def test_initializedDatabaseWithSessions(self):
        # Initialize and close the initial database.
        self.initialDatabase.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
        self.initialDatabase.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
        self.initialDatabase.execute("INSERT INTO Sessions VALUES (\"000000001\",100,105);")
        self.initialDatabase.execute("INSERT INTO Sessions VALUES (\"000000002\",106,109);")
        self.initialDatabase.execute("INSERT INTO Sessions VALUES (\"000000002\",109,0);")
        self.initialDatabase.commit()
        self.initialDatabase.close()

        # Create the database and assert sessions are correct.
        CuT = DatabaseManager.DatabaseManager(self.databaseFile)
        sessions = CuT.database.execute("SELECT * FROM Sessions;").fetchall()
        self.assertEqual(sessions[0],("000000001",100,105),"Session is incorrect.")
        self.assertEqual(sessions[1],("000000002",106,109),"Session is incorrect.")
        self.assertEqual(sessions[2],("000000002",109,-1),"Session is incorrect.")

    """
    Tests the getUserAccessType method.
    """
    def test_getUserAccessType(self):
        # Initialize and close the initial database.
        self.initialDatabase.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
        self.initialDatabase.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
        self.initialDatabase.execute("INSERT INTO Users VALUES (\"000000001\",\"AUTHORIZED\");")
        self.initialDatabase.execute("INSERT INTO Users VALUES (\"000000002\",\"ADMIN\");")
        self.initialDatabase.commit()
        self.initialDatabase.close()

        # Create the database and assert the user types are correct.
        CuT = DatabaseManager.DatabaseManager(self.databaseFile)
        self.assertEqual(CuT.getUserAccessType("000000001"),"AUTHORIZED","Type is incorrect.")
        self.assertEqual(CuT.getUserAccessType("000000002"),"ADMIN","Type is incorrect.")
        self.assertEqual(CuT.getUserAccessType("000000003"),"UNAUTHORIZED","Type is incorrect.")

    """
    Tests the setUserAccessType method.
    """
    def test_setUserAccessType(self):
        # Initialize and close the initial database.
        self.initialDatabase.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
        self.initialDatabase.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
        self.initialDatabase.commit()
        self.initialDatabase.close()

        # Set a new user type and assert the entries are correct.
        CuT = DatabaseManager.DatabaseManager(self.databaseFile)
        CuT.setUserAccessType("000000001","AUTHORIZED")
        users = CuT.database.execute("SELECT * FROM Users;").fetchall()
        self.assertEqual(users[0],("000000001","AUTHORIZED"),"User is incorrect.")

        # Set a new user type and assert the entries are correct.
        CuT.setUserAccessType("000000002","ADMIN")
        users = CuT.database.execute("SELECT * FROM Users;").fetchall()
        self.assertEqual(users[0],("000000001","AUTHORIZED"),"User is incorrect.")
        self.assertEqual(users[1],("000000002","ADMIN"),"User is incorrect.")

        # Set a new user type and assert the entries are correct.
        CuT.setUserAccessType("000000001","ADMIN")
        users = CuT.database.execute("SELECT * FROM Users;").fetchall()
        self.assertEqual(users[0],("000000001","ADMIN"),"User is incorrect.")
        self.assertEqual(users[1],("000000002","ADMIN"),"User is incorrect.")

        # Set a new user type and assert the entries are correct.
        CuT.setUserAccessType("000000001","UNAUTHORIZED")
        users = CuT.database.execute("SELECT * FROM Users;").fetchall()
        self.assertEqual(users[0],("000000002","ADMIN"),"User is incorrect.")

    """
    Tests the sessionStarted method.
    """
    def test_sessionStarted(self):
        # Initialize and close the initial database.
        self.initialDatabase.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
        self.initialDatabase.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
        self.initialDatabase.commit()
        self.initialDatabase.close()

        # Create the database, start sessions, and assert the sessions are correct.
        CuT = DatabaseManager.DatabaseManager(self.databaseFile)
        CuT.sessionStarted(Session.Session(User.User("000000001",10),5))
        CuT.sessionStarted(Session.Session(User.User("000000002",10),8))
        CuT.sessionStarted(Session.Session(User.User("000000001",10),15))
        sessions = CuT.database.execute("SELECT * FROM Sessions;").fetchall()
        self.assertEqual(sessions[0],("000000001",5,0),"Session is incorrect.")
        self.assertEqual(sessions[1],("000000002",8,0),"Session is incorrect.")
        self.assertEqual(sessions[2],("000000001",15,0),"Session is incorrect.")

    """
    Tests the sessionStarted method.
    """
    def test_sessionEnded(self):
        # Mock the Time module.
        currentTime = 0
        class MockTimeModule:
            def getCurrentTimestamp(self):
                return currentTime
        DatabaseManager.Time = MockTimeModule()

        # Initialize and close the initial database.
        self.initialDatabase.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
        self.initialDatabase.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
        self.initialDatabase.commit()
        self.initialDatabase.close()

        # Create the database, start and end sessions, and assert the sessions are correct.
        CuT = DatabaseManager.DatabaseManager(self.databaseFile)
        CuT.sessionStarted(Session.Session(User.User("000000001",10),5))
        currentTime = 7
        CuT.sessionEnded(Session.Session(User.User("000000001",10),5))
        CuT.sessionStarted(Session.Session(User.User("000000002",10),8))
        currentTime = 9
        CuT.sessionEnded(Session.Session(User.User("000000002",10),8))
        CuT.sessionStarted(Session.Session(User.User("000000001",10),15))
        sessions = CuT.database.execute("SELECT * FROM Sessions;").fetchall()
        self.assertEqual(sessions[0],("000000001",5,7),"Session is incorrect.")
        self.assertEqual(sessions[1],("000000002",8,9),"Session is incorrect.")
        self.assertEqual(sessions[2],("000000001",15,0),"Session is incorrect.")

"""
Test the static methods.
"""
class TestStaticMethods(unittest.TestCase):
    """
    Sets up the unit test.
    """
    def setUp(self):
        # Create a temporary file for the database.
        databaseFile = tempfile.TemporaryFile()
        self.databaseFile = databaseFile.name
        databaseFile.close()
        del databaseFile

        # Create the database.
        self.initialDatabase = sqlite3.connect(self.databaseFile)

    """
    Tests the getUser method.
    """
    def test_getUser(self):
        # Initialize and close the initial database.
        self.initialDatabase.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
        self.initialDatabase.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
        self.initialDatabase.execute("INSERT INTO Users VALUES (\"000000001\",\"AUTHORIZED\");")
        self.initialDatabase.execute("INSERT INTO Users VALUES (\"000000002\",\"ADMIN\");")
        self.initialDatabase.commit()
        self.initialDatabase.close()

        # Set the static database and assert the users are correct.
        DatabaseManager.staticDatabaseManager = DatabaseManager.DatabaseManager(self.databaseFile)
        self.assertEqual(DatabaseManager.getUser("000000001").getId(),"000000001","Id is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000001").getAccessType(),"AUTHORIZED","Access type is incorrect.")
        self.assertNotEqual(DatabaseManager.getUser("000000001").getSessionTime(),0,"Session time is zero.")
        self.assertEqual(DatabaseManager.getUser("000000002").getId(),"000000002","Id is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000002").getAccessType(),"ADMIN","Access type is incorrect.")
        self.assertNotEqual(DatabaseManager.getUser("000000002").getSessionTime(),0,"Session time is zero.")
        self.assertEqual(DatabaseManager.getUser("000000003").getId(),"000000003","Id is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000003").getAccessType(),"UNAUTHORIZED","Access type is incorrect.")
        self.assertEqual(DatabaseManager.getUser("000000003").getSessionTime(),0,"Session time is non-zero.")

    """
    Tests the setUserAccessType method.
    """
    def test_setUserAccessType(self):
        # Initialize and close the initial database.
        self.initialDatabase.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
        self.initialDatabase.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
        self.initialDatabase.commit()
        self.initialDatabase.close()

        # Set a new user type and assert the entries are correct.
        DatabaseManager.staticDatabaseManager = DatabaseManager.DatabaseManager(self.databaseFile)
        DatabaseManager.setUserAccessType("000000001", "AUTHORIZED")
        users = DatabaseManager.staticDatabaseManager.database.execute("SELECT * FROM Users;").fetchall()
        self.assertEqual(users[0], ("000000001", "AUTHORIZED"), "User is incorrect.")

        # Set a new user type and assert the entries are correct.
        DatabaseManager.setUserAccessType("000000002", "ADMIN")
        users = DatabaseManager.staticDatabaseManager.database.execute("SELECT * FROM Users;").fetchall()
        self.assertEqual(users[0], ("000000001", "AUTHORIZED"), "User is incorrect.")
        self.assertEqual(users[1], ("000000002", "ADMIN"), "User is incorrect.")

        # Set a new user type and assert the entries are correct.
        DatabaseManager.setUserAccessType("000000001", "ADMIN")
        users = DatabaseManager.staticDatabaseManager.database.execute("SELECT * FROM Users;").fetchall()
        self.assertEqual(users[0], ("000000001", "ADMIN"), "User is incorrect.")
        self.assertEqual(users[1], ("000000002", "ADMIN"), "User is incorrect.")

        # Set a new user type and assert the entries are correct.
        DatabaseManager.setUserAccessType("000000001", "UNAUTHORIZED")
        users = DatabaseManager.staticDatabaseManager.database.execute("SELECT * FROM Users;").fetchall()
        self.assertEqual(users[0], ("000000002", "ADMIN"), "User is incorrect.")

    """
    Tests the sessionStarted method.
    """
    def test_sessionStarted(self):
        # Initialize and close the initial database.
        self.initialDatabase.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
        self.initialDatabase.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
        self.initialDatabase.commit()
        self.initialDatabase.close()

        # Set the static database, start sessions, and assert the sessions are correct.
        DatabaseManager.staticDatabaseManager = DatabaseManager.DatabaseManager(self.databaseFile)
        DatabaseManager.sessionStarted(Session.Session(User.User("000000001",10),5))
        DatabaseManager.sessionStarted(Session.Session(User.User("000000002",10),8))
        DatabaseManager.sessionStarted(Session.Session(User.User("000000001",10),15))
        sessions = DatabaseManager.staticDatabaseManager.database.execute("SELECT * FROM Sessions;").fetchall()
        self.assertEqual(sessions[0], ("000000001",5,0), "Session is incorrect.")
        self.assertEqual(sessions[1], ("000000002",8,0), "Session is incorrect.")
        self.assertEqual(sessions[2], ("000000001",15,0), "Session is incorrect.")

    """
    Tests the sessionEnded method.
    """
    def test_sessionEnded(self):
        # Mock the Time module.
        currentTime = 0

        class MockTimeModule:
            def getCurrentTimestamp(self):
                return currentTime

        DatabaseManager.Time = MockTimeModule()

        # Initialize and close the initial database.
        self.initialDatabase.execute("CREATE TABLE Users (Id char(9),AccessType STRING);")
        self.initialDatabase.execute("CREATE TABLE Sessions (Id char(9),StartTime BIGINT,EndTime BIGINT);")
        self.initialDatabase.commit()
        self.initialDatabase.close()

        # Set the static database, start and end sessions, and assert the sessions are correct.
        DatabaseManager.staticDatabaseManager = DatabaseManager.DatabaseManager(self.databaseFile)
        DatabaseManager.sessionStarted(Session.Session(User.User("000000001",10),5))
        currentTime = 7
        DatabaseManager.sessionEnded(Session.Session(User.User("000000001",10),5))
        DatabaseManager.sessionStarted(Session.Session(User.User("000000002",10),8))
        currentTime = 9
        DatabaseManager.sessionEnded(Session.Session(User.User("000000002",10),8))
        DatabaseManager.sessionStarted(Session.Session(User.User("000000001",10),15))
        sessions = DatabaseManager.staticDatabaseManager.database.execute("SELECT * FROM Sessions;").fetchall()
        self.assertEqual(sessions[0],("000000001",5,7),"Session is incorrect.")
        self.assertEqual(sessions[1],("000000002",8,9),"Session is incorrect.")
        self.assertEqual(sessions[2],("000000001",15,0),"Session is incorrect.")



"""
Runs the unit tests.
"""
def main():
    unittest.main()

# Run the tests.
if __name__ == '__main__':
    main()