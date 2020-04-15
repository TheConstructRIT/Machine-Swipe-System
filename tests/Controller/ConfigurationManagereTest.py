"""
Zachary Cook

Unit tests for the configuration manager.
"""

"""
Zachary Cook

Unit tests for the SessionManager.
"""

import unittest
from Controller import ConfigurationManager



"""
Test the static methods.
"""
class TestStaticMethods(unittest.TestCase):
    """
    Sets up the unit test.
    """
    def setUp(self):
        """
        Mock file class.
        """
        class MockFile:
            """
            Reads the lines.
            """
            def read(self):
                return "{\"DisplayName\": \"Test Machine\",\"DefaultSessionTime\": 60,\"AlarmActivationTime\": 20,\"CustomSetting\":true}"
            
            """
            Closes the file.
            """
            def close(self):
                pass

        """
        Opens a file.
        """
        def open(_):
            return MockFile()

        # Set up mock opening of files.
        ConfigurationManager.open = open

    """
    Tests the readSetting method.
    """
    def test_readSetting(self):
        self.assertEqual(ConfigurationManager.readSetting("DisplayName"),"Test Machine","Setting is incorrect.")
        self.assertEqual(ConfigurationManager.readSetting("DefaultSessionTime"),60,"Setting is incorrect.")
        self.assertEqual(ConfigurationManager.readSetting("AlarmActivationTime"),20,"Setting is incorrect.")
        self.assertEqual(ConfigurationManager.readSetting("CustomSetting"),True,"Setting is incorrect.")

    """
    Tests the getMachineName method.
    """
    def test_getMachineName(self):
        self.assertEqual(ConfigurationManager.getMachineName(),"Test Machine","Setting is incorrect.")

    """
    Tests the getDefaultSessionTime method.
    """
    def test_getDefaultSessionTime(self):
        self.assertEqual(ConfigurationManager.getDefaultSessionTime(),60,"Setting is incorrect.")

    """
    Tests the getWarningAlarmActivationTime method.
    """
    def test_getWarningAlarmActivationTime(self):
        self.assertEqual(ConfigurationManager.getWarningAlarmActivationTime(),20,"Setting is incorrect.")



"""
Runs the unit tests.
"""
def main():
    unittest.main()

# Run the tests.
if __name__ == '__main__':
    main()