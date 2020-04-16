# Machine Swipe System Setup

## Hardware
(This will be typed in the future when a wiring diagram is done)

## Software
The software implementation is specific to the to the 
Raspberry Pi. The system has been validated on the 2B+,
but should work on any version that has the GPIO pins.

### Deploy Script
To speed up deployment, a `Deploy.py` script has been created
to automate most of the deployment process for Windows. The
pre-requisites for this include:
- [Python 3](https://www.python.org/downloads/)
- An EXT file system driver, like [Ext2Fsd](https://sourceforge.net/projects/ext2fsd/files/) or [extFS by Paragon](https://www.paragon-software.com/business/extfs-for-windows/)
- [Raspbian Buster Lite](https://www.raspberrypi.org/downloads/raspbian/)
  - The desktop versions don't work with the deployment script since the
    process for setting the desktop to CLI wasn't easy to automate.

Start by flashing Raspbian Buster Lite onto the SD card for
the Raspberry Pi. Check for a guide online on how to do this.
Before running the deploy script, the pywin32 library is required. It can be 
installed by running the following in the command line:
```bash
pip3 install pywin32
```

After the SD card is plugged in an recognized, run the Deploy script
by running it in the command line.
```bash
python3 Deploy.py
```

The deploy script asks for configuration values and the initial
admin ids as 9-digit university ids. If the system was already
deployed, the script can update the code, configuration, and admin ids.
After the script is done, it can be put into the Raspberry Pi. The
first run can take up over 2 minutes to complete, but should be less
to start up for future runs. This depends on the speed of the SD card
and the model of Raspberry Pi.


### Operating System
The intended operating system for the system is any
distribution of [Rasbian](https://www.raspberrypi.org/downloads/raspbian/).
A version with the desktop user interface is recommended
for setup, although the command line is all that is required
for operation. Python 3 is also required using the existing
code. Both Python 2.7 and 3.5 are typically included. If 
this is the case, the required command is `python3`.

### Files
With the default setup, the only files that need to
be downloaded is the repository excluding the following:
- `tests`
- `docs`
- `README.md`
- `.gitignore`

To setup the system for a specific machine, `configuraiton.json`
needs to be modified. The configuration includes the
following options:
- DisplayName - the name displayed to the end user.
- DefaultSessionTime - the default session time for an
authorized user.
- AlarmActivationTime - the time (in seconds) that the alarm will
beep for 5 times if the session goes below it. To disable it, this
number should be set greater than the session time, or set to 0.

The location of the directory doesn't matter, but must be known for
the command. It is recommended to be in the `pi`'s home directory
to make navigation easier.

### Initialization
Since the system uses `stdin` (standard input), the
system needs to boot to a command line interface. This is
set by:
- Desktop:
    - On the top bar, click the Raspberry Pi logo
    - In the menu, go to `Preferences`, then to Raspberry `Pi Configuration`
    - Under Boot, select `To CLI` and make sure `Login as user 'pi'` is selected
    - Press `Ok` and reboot the system
- Command line:
    - Open the configuration using `sudo raspi-config`
    - Navigate to `3 Boot Options`
    - Navigate to `B1 Desktop / CLI`
    - Select `B4 Console Autologin`
    - Press `Esc` to exit the tool
    - Type `reboot` and press enter to reboot the system
    
When booted to CLI mode, you will need to use the text editor `nano` to
modify the `.bashrc` file to auto-start the system. `.bashrc` is used
since it will run at boot and allow using `stdin`. When using `nano`, you
may get an error saying `Error opening terminal: unknown.`. This means
the terminal variable is not set. A temporary fix for this is executing
`export TERM=xterm-256color`.

When editing `.bashrc`, you will need to add the command for starting the
system, and potentially patching the terminal (see above). If the system
in in the pi's Desktop directory, the following should be added to `.bashrc`
using `nano .bashrc`:
```
# Set the terminal.
export TERM=xterm-256color

# Start the python system.
python3 ~/Desktop/Machine-Swipe-System/Initializer.py
```

When the system is started, commands will not be able to be run since the
system is treated as an active command. To stop the system, `Ctrl + C` can
be used to interrupt the command and stop it from executing. This will also
be need in the desktop environment since `.bashrc` will run the commands
when opening a terminal window.