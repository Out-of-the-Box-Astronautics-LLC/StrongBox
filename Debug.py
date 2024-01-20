#!/usr/bin/env python3
"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.mvp"
__company__ = "Robotic Beverage Technologies, Inc"
__status__  = "Development"
__date__    = "Late Updated: 2020-07-02"
__doc__     = "Code to make print() debuggging and data logging easier"
"""

# Allow program to create GMT and local timestamps
from time import gmtime, strftime

# Error code global CONSTANTS
OBJECT_CREATION_ERROR = 0
GLOBAL_CONSTANT_USAGE_ERROR = 1
PUMP_CONFIGURATION_ERROR = 2
LINEAR_ACTUATOR_CONFIGURATION_ERROR = 3
DISPLAY_CONFIGURATION_ERROR = 4

# TODO Create more error codes
API_ERROR = 5
USER_ERROR = 6

# Exit case CONSTANTS for debug logs
OK = 0
TORQUE_EXIT_CASE = -1
DEPTH_EXIT_CASE  = -2
TIME_EXIT_CASE   = -3


class Debug:

    def __init__(self, initState, pythonClass):
        """
        Constructor to initialize a Debug object, which determines if debug statement should print and what file the developer asked for Debug statements in

        Key arguments:
        initState -- Boolean variable, which if True causes debug statements to be printed to the terminal
        pythonClass -- String variable, of Python class or file (Driver.py) calling Debug() to create object

        Return value:
        Newly created Debug() object
        """

        self.f = open('DataLog.txt','r+')    # Open read and append at end write access to .txt file
        self.pythonClass = pythonClass

        # Toogle initial debug statements ON (true) or Off (false)
        if(initState == False):
            self.DEBUG_STATEMENTS_ON = False
        else:
            self.DEBUG_STATEMENTS_ON = True
            print("DEBUG STATEMENTS ARE ON INSIDE " + pythonClass + " CLASS")


    def GetMode(self):
	    return self.DEBUG_STATEMENTS_ON


    def TurnOnDebugMode(self):
        self.DEBUG_STATEMENTS_ON = True


    def TurnOffDebugMode(self):
        self.DEBUG_STATEMENTS_ON = False


    def CloseFile(self):
        """
        Close the text file LPrint function is writing to

        Key arguments:
        NONE

        Return value:
        NOTHING
        """

        self.f.close()


    def Dprint(self, logMessage):
        """
        Debug print to terminal only
        Calls standard Python 3 print("X") statement if "DEBUG_STATEMENTS_ON" class variable is TRUE

        Key arguments:
        logMessage -- String variable, of custom text to print to terminal

        Return value:
        NOTHING
        """

        if(self.DEBUG_STATEMENTS_ON):
            print(self.pythonClass + " MESSAGE: " + logMessage + "\n")
        else:
            print("\n") # PRINT NEW LINE / DO NOTHING

    def Lprint(self, logMessage):
       """
       Log debugging print with LOCAL TIME to both a datalog.txt file and the terminal
       Calls Dprint() and standard Python 3 write() if class variable is TRUE

       @link - https://docs.python.org/3/library/time.html#time.strftime

       Key arguments:
       logMessage --

       Return value:
       NOTHING
       """

       if(self.DEBUG_STATEMENTS_ON):
           self.Dprint(logMessage + " on " + strftime("%c") + "\n")

           self.f.write(self.pythonClass + " DAY & TIME: " + strftime("%c") + "\n")
           self.f.write(self.pythonClass + " MESSAGE: " + logMessage + "\n")
       else:
            print("\n") # PRINT NEW LINE / DO NOTHING


if __name__ == "__main__":
    print("UNIT TESTING Debug.py:")
    test = Debug(True, "Debug.py")

    print(test.GetMode())
    test.TurnOffDebugMode()

    test.Dprint("This should not print :)")
    test.TurnOnDebugMode()
    print(test.GetMode())

    test.Dprint("Hello World")
    test.Lprint("Goodbye World data logging is NOT fun")
    test.Lprint("Just kidding :)")
    test.TurnOffDebugMode()
    test.Dprint("This should not print either :)")
    test.CloseFile()
