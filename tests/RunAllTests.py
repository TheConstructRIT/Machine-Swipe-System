"""
Zachary Cook

Runs all the unit tests.
"""

import os
import importlib.machinery
import unittest



testCaseLoader = unittest.TestLoader()
testCases = []

"""
Adds test cases from the specified directory.
"""
def addTestCases(location):
    if os.path.isdir(location):
        # Add the directories.
        for file in os.listdir(location):
            addTestCases(os.path.realpath(os.path.join(location,file)))
    elif os.path.isfile(location) and location.endswith(".py") and location != os.path.realpath(__file__):
        # Load the module.
        moduleName, fileExtension = os.path.splitext(os.path.split(location)[-1])
        loader = importlib.machinery.SourceFileLoader(moduleName, location)
        module = loader.load_module()

        # Add the test cases.
        for testClassName in dict([(name, cls) for name,cls in module.__dict__.items() if isinstance(cls,type)]):
            testClass = getattr(module,testClassName)
            if issubclass(testClass,unittest.TestCase):
                testCases.append(testCaseLoader.loadTestsFromTestCase(testClass))



if __name__ == '__main__':
    # Add the test cases.
    addTestCases(os.path.realpath(__file__ + "/../"))

    # Run the test cases.
    suite = unittest.TestSuite(testCases)
    runner = unittest.TextTestRunner()
    results = runner.run(suite)