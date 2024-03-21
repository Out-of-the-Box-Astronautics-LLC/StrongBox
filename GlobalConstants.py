#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = "False"
__version__    = "0.0.1"
"""
TODO = -1
# Useful CONSTANTS for the Strong Box moon mission

DEBUG_STATEMENTS_ON = True

# Physical elements inside a Strong Box
NUMBER_OF_ROCKET_ENGINES = 1
NUMBER_OF_CAMERAS = 9

# Mappping data CONSTANTS
NULL_LOCATION = None
MAX_X_GRID = 100_000_000
MAX_Y_GRID = 2 * MAX_X_GRID
GRID_TO_GPS_CONSTANT = 9999_999/MAX_X_GRID # GPS is 7 accurate to seven sig figs and thus seven 9's

# SQLite Database CONSTANTS
# TODO

# Default file location for code
MAC_CODE_DIRECTORY   = '/Users/venus/GitRepos/StrongBox'
LINUX_CODE_DIRECTORY = '/home/mercury/MoeBuild/StrongBox'
WINDOWS_CODE_DIRECTORY = 'D:/StrongBox'
TEST_IMAGE = 'static/images/TestImageApollo16_1920x1080.jpeg'
LAST_FRAMES = 'static/images/LastFrame'
CURRENT_FRAMES = 'static/images/CurrentFrame'

# GUI Display CONSTANTS
DEBUG_STATEMENTS_ON = True
STRONG_BOX_BLUE  = '#000F24'    # RGB R=0, G=15, and B=36 https://www.rgbtohex.net
STRONG_BOX_GREEN = '#126A74'    # RGB R=18, G=106, and B=116 https://www.rgbtohex.net
GUI_PAGE_REFRESH_RATE = 30      # Units are Hertz (Hz = 1 / seconds)
CLOCK_UPDATE_TIME = 60          # Units are seconds

# Kinematics Equation CONSTANTS
# See https://physicscatalyst.com/calculators/physics/kinematics-calculator.php
VF = 1
VI = 2
T  = 3
DD = 4
A  = 5
