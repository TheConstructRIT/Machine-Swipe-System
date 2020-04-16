"""
Zachary Cook

Deploys the code to a SD card with Raspbian.
Note: This only works on Windows.

Requires:
pip3 install pywin32
"""

# The files and directories to copy.
FILES_TO_COPY = [
    "Controller",
    "Hardware",
    "Model",
    "__init__.py",
    "Initializer.py",
]

# Configurable values in configuration.json.
CONFIGURABLE_ITEMS = [
    ["DisplayName","The name displayed ot a user.",str],
    ["DefaultSessionTime","The default session time in seconds.",int],
    ["AlarmActivationTime","The time to run an alarm for a session close to running out.",int],
]



import json
import os
import shutil
import win32api
from Controller import DatabaseManager



"""
Returns the drive letter with Raspbian.
"""
def getRaspbianRootDrive():
    # Iterate through the drives and find a removable drive with /home/pi.
    raspbianDrive = None
    for driveLetter in win32api.GetLogicalDriveStrings().split("\x00"):
        if os.path.exists(os.path.join(driveLetter,"home","pi")):
            raspbianDrive = driveLetter

    # Return the drives.
    return raspbianDrive

"""
Reads the source of a file and returns it.
If it doesn't exist, an empty string is returned.
"""
def readFile(location):
    # Return an empty string if the location doesn't exist.
    if not os.path.exists(location):
        return ""

    # Open the file and return the contents.
    with open(location) as file:
        return file.read()



if __name__ == '__main__':
    # Get the root file system of Raspbian.
    raspbianDrive = getRaspbianRootDrive()
    if raspbianDrive is None:
        print("Raspbian SD card not detected. Make sure:")
        print("\tThe SD card is connected and connected.")
        print("\tThe SD card contains an install of Raspbian with the default pi account.")
        print("\tAn Ext2 driver (like Paragon LFS or Ext2Fsd) is installed and running.")
        exit(1)

    # Set up auto-login.
    autoLoginConfigurationFile = os.path.join(raspbianDrive,"etc","systemd","system","getty@tty1.service.d","autologin.conf")
    autoLoginSource = readFile(autoLoginConfigurationFile)
    if "--autologin pi" not in autoLoginSource:
        print("Setting Raspbian to boot auto login.")
        with open(autoLoginConfigurationFile,"w",newline="\n") as file:
            file.write(autoLoginSource + "[Service]\nExecStart=\nExecStart=-/sbin/agetty --autologin pi --noclear %I $TERM")

    # Patch the raspi-config to replace RET=$1 with RET=1.
    raspiConfigFile = os.path.join(raspbianDrive,"usr","bin","raspi-config")
    raspiConfigSource = readFile(raspiConfigFile)
    if "RET=$1" in raspiConfigSource:
        print("Patching raspi-config for non-interactive mode.")
        with open(raspiConfigFile,"w",newline="\n") as file:
            raspiConfigSource = raspiConfigSource.replace("RET=$1","RET=0")
            file.write(raspiConfigSource)

    # Set up the .bashrc to run the code.
    bashrcFile = os.path.join(raspbianDrive,"home","pi",".bash_aliases")
    bashrcSource = readFile(bashrcFile)
    if "python3 Initializer.py" not in bashrcSource:
        print("Adding code starting on login.")
        with open(bashrcFile,"w",newline="\n") as file:
            bashrcSource += "\n# Enable i2c if it isn't enabled (reboot required)."
            bashrcSource += "\nif [ $(/usr/bin/raspi-config nonint get_i2c) -eq 1 ]; then"
            bashrcSource += "\n    sudo /usr/bin/raspi-config nonint do_i2c"
            bashrcSource += "\n    sudo reboot"
            bashrcSource += "\nfi"
            bashrcSource += "\n"
            bashrcSource += "\n# Start the machine swipe system."
            bashrcSource += "\ncd /home/pi/MachineSwipeSystem"
            bashrcSource += "\npython3 Initializer.py"
            file.write(bashrcSource)

    # Copy the libraries.
    smbusFileLocation = os.path.join(raspbianDrive,"usr","lib","python3","dist-packages","smbus.py")
    rPiFileLocation = os.path.join(raspbianDrive,"usr","lib","python3","dist-packages","RPi")
    if not os.path.exists(smbusFileLocation):
        print("Adding smbus Python library.")
        shutil.copy("deploy/smbus.py",smbusFileLocation)
    if not os.path.exists(rPiFileLocation):
        print("Adding RPi Python library.")
        shutil.copytree("deploy/RPi",rPiFileLocation)

    # Copy the code.
    print("Replacing Machine Swipe System code.")
    machineSwipeSystemDirectory = os.path.join(raspbianDrive,"home","pi","MachineSwipeSystem")
    for fileToReplace in FILES_TO_COPY:
        print("\tReplacing " + fileToReplace)
        targetLocation = os.path.join(machineSwipeSystemDirectory,fileToReplace)
        if os.path.isdir(fileToReplace):
            if os.path.exists(targetLocation):
                shutil.rmtree(targetLocation)
            shutil.copytree(fileToReplace,targetLocation)
        else:
            if os.path.exists(targetLocation):
                os.remove(targetLocation)
            shutil.copy(fileToReplace,targetLocation)

    # Prompt to set up the configuration.json.
    configurationLocation = os.path.join(raspbianDrive,"home","pi","MachineSwipeSystem","configuration.json")
    setupConfiguration = True
    if os.path.exists(configurationLocation):
        updateConfigurationResult = input("Update the configuration?\n").lower().strip()
        setupConfiguration = (updateConfigurationResult == "y" or updateConfigurationResult == "yes" or updateConfigurationResult == "t" or updateConfigurationResult == "true")

    if setupConfiguration:
        # Parse the existing configuration.
        existingConfiguration = {}
        configurationExists = False
        changesMade = False
        if os.path.exists(configurationLocation):
            with open(configurationLocation) as file:
                existingConfiguration = json.loads(file.read())
                configurationExists = True

        # Prompt for new fields in the configuration.
        for configurationInformation in CONFIGURABLE_ITEMS:
            displayName,description,configurationType = configurationInformation[0],configurationInformation[1],configurationInformation[2]
            print("Enter the desired \"" + displayName + "\" (" + description + ")")
            if displayName in existingConfiguration.keys():
                print("\tExisting value: " + str(existingConfiguration[displayName]))

            # Get and set the value.
            while True:
                newValue = input()
                if configurationType == int:
                    try:
                        newValue = int(newValue)
                        if newValue not in existingConfiguration.keys() or newValue != existingConfiguration[displayName]:
                            changesMade = True
                        existingConfiguration[displayName] = newValue
                        break
                    except ValueError:
                        print("Value must be a number.")
                else:
                    if newValue not in existingConfiguration.keys() or newValue != existingConfiguration[displayName]:
                        changesMade = True
                    existingConfiguration[displayName] = newValue
                    break

        # Save the configuration.
        if changesMade:
            with open(configurationLocation,"w",newline="\n") as file:
                file.write(json.dumps(existingConfiguration,indent=4))

    # Prompt to set up the admin ids.
    database = DatabaseManager.DatabaseManager(os.path.join(raspbianDrive,"home","pi","MachineSwipeSystem","database.sqlite"))
    changeAdminIds = True
    if len(database.database.execute("SELECT * FROM Users WHERE AccessType = \"ADMIN\";").fetchall()) > 0:
        changeAdminIdsResult = input("Update the admin ids?\n").lower().strip()
        changeAdminIds = (changeAdminIdsResult == "y" or changeAdminIdsResult == "yes" or changeAdminIdsResult == "t" or changeAdminIdsResult == "true")

    # Change the admin ids.
    if changeAdminIds:
        # Change the existing ids.
        for user in database.database.execute("SELECT Id FROM Users WHERE AccessType = \"ADMIN\";").fetchall():
            changeAccess = input("Set admin id " + user[0] + " to authorized from admin?\n").lower().strip()
            if changeAccess == "y" or changeAccess == "yes" or changeAccess == "t" or changeAccess == "true":
                database.setUserAccessType(user[0],"AUTHORIZED")
            changeAccess = input("Set admin id " + user[0] + " to unauthorized from admin?\n").lower().strip()
            if changeAccess == "y" or changeAccess == "yes" or changeAccess == "t" or changeAccess == "true":
                database.setUserAccessType(user[0],"UNAUTHORIZED")

        # Prompt for new ids.
        newIds = input("Enter the new admin ids separated by commas?\n").lower().strip()
        for id in newIds.split(","):
            if id != 0 and len(id) == 9:
                database.setUserAccessType(id,"ADMIN")
                print("Set " + id + " as an admin.")