#!/usr/bin/python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "info@strongbox.space"
__copyright__  = "Copyright 2023"
__license__    = "MIT License"
__status__     = "Production"
__deprecated__ = "False"
__version__    = "1.0.1"
"""
# Make print() debuggging and data logging easier"

## Standard Library
# Allow program to create GMT and local timestamps
from time import gmtime, strftime


# Error code global CONSTANTS (TODO Create more error codes)
OBJECT_CREATION_ERROR = 0
GLOBAL_CONSTANT_USAGE_ERROR = 1
PUMP_CONFIGURATION_ERROR = 2
LINEAR_ACTUATOR_CONFIGURATION_ERROR = 3
DISPLAY_CONFIGURATION_ERROR = 4
API_ERROR = 5
USER_ERROR = 6

# Exit case CONSTANTS for debug logs
OK = 0
TORQUE_EXIT_CASE = -1
DEPTH_EXIT_CASE  = -2
TIME_EXIT_CASE   = -3


class Debug:

    def __init__(self, initState, pythonClass):
        """ Constructor to initialize a Debug.py object

        Arg(s):
            initState (Boolean): If  set to True, debug statements will be printed to the terminal
            pythonClass (String): Python class or file (Driver.py) calling / creating the Debug() to object

        Returns:
            Newly created Debug() object
        """
        self.f = open('DebugLog.txt','r+')    # Open read and append at end write access to .txt file
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
        """ Close the text file LPrint functions is writing to

        Arg(s):
            NONE

        Returns:
            NOTHING
        """
        self.f.close()


    def Dprint(self, logMessage):
        """ Debug print to terminal only

        Calls standard Python 3 print("X") statement if "DEBUG_STATEMENTS_ON" class variable is TRUE

        Arg(s):
            logMessage (String variable: Custom text to print to terminal

        Returns:
            NOTHING
        """
        if(self.DEBUG_STATEMENTS_ON):
            print(self.pythonClass + " MESSAGE: " + logMessage + "\n")
        else:
            print("\n") # PRINT NEW LINE / DO NOTHING


    def Lprint(self, logMessage):
       """ Log debugging print with LOCAL TIME to both a datalog.txt file and the terminal

       Calls both Dprint() function and standard Python 3 write() if class variable is TRUE

       See https://docs.python.org/3/library/time.html#time.strftime

       Arg(s):
           logMessage (String variable: Custom text to print to terminal

       Returns:
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
