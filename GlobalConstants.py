#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "info@strongbox.space"
__copyright__  = "Copyright 2024"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = "False"
__version__    = "0.0.1"
"""
TODO = -1
# Useful CONSTANTS for the Strong Box moon mission

DEBUG_STATEMENTS_ON = False

# Physical elements inside a Strong Box
NUMBER_OF_ROCKET_ENGINES = 1
NUMBER_OF_CAMERAS = 10
NUMBER_OF_CPUS = 2

# Mappping data CONSTANTS
NULL_LOCATION = None
MAX_X_GRID = 100_000_000
MAX_Y_GRID = 2 * MAX_X_GRID
GRID_TO_GPS_CONSTANT = 9999_999/MAX_X_GRID # GPS is 7 accurate to seven sig figs and thus seven 9's

# SQLite Database CONSTANTS
# TODO

# Location of the code base on your local development PC / Mac and flight hardware (NVIDIA AGX ORION NANO)
# The username for mission software is ootba = Out of the Box Astronautics LLC
DEV_MAC_CODE_DIRECTORY   = '/Users/pluto/GitRepos/StrongBox/'
DEV_LINUX_CODE_DIRECTORY = '/home/apollo-linux/GitRepos/StrongBox/'
DEV_WINDOWS_CODE_DIRECTORY = 'C:/Users/neptune/Desktop/GitRepos/StrongBox/'
FLIGHT_HARDWARE_CODE_DIRECTORY = '/home/ootba/StrongBox/'
TEST_IMAGE = 'static/images/TestImageApollo16_1920x1080.jpeg'
TEST_IMAGE_A = 'static/images/TestImageApollo16_GreySurface.png'
TEST_IMAGE_B = 'static/images/TestImageApollo16_BlackSky.png'
LAST_FRAMES = 'static/images/LastFrame'
CURRENT_FRAMES = 'static/images/CurrentFrame'
CSV_POWER_PARTS = 'PowerSourceSink.csv'

# GUI Display CONSTANTS
DEBUG_STATEMENTS_ON = True
STRONG_BOX_BLUE  = '#000F24'    # RGB R=0, G=15, and B=36 https://www.rgbtohex.net
STRONG_BOX_GREEN = '#126A74'    # RGB R=18, G=106, and B=116 https://www.rgbtohex.net
GUI_PAGE_REFRESH_RATE = 30      # Units are Hertz (Hz = 1 / seconds)
CLOCK_UPDATE_TIME = 60          # Units are seconds

# Kinematic Equations CONSTANTS
# See https://physicscatalyst.com/calculators/physics/kinematics-calculator.php
VF = 0
VI = 1
T  = 2
DD = 3
A  = 4
G_EARTH = 9.81
G_MOON  = 1.62
