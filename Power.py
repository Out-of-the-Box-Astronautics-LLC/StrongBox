#!/usr/bin/python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "info@strongbox.space"
__copyright__  = "Copyright 2024"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = "False"
__version__    = "0.0.1"
__doc__        = "Measure real and calculate theoretical electrical power usage"
"""

## Standard Library
from math import pow, sqrt, pi  # Power (2^2), Squareroot (4^0.5), and Pi (3.14159) math helper libraries
import csv                      # Import csv file to define power sources and sinks

## 3rd Party Libraries
# Sense Flex Power Measurement Sensor from https://sense.com/buy
# Unofficial API for the Sense Energy Monitor
# https://github.com/scottbonline/sense
from sense_energy import Senseable

# Load environment variables for usernames, passwords, & API keys
# Used to login into Sense API
# https://pypi.org/project/python-dotenv/
from dotenv import dotenv_values

## Internally Developed Library
import GlobalConstants as GC                # Useful global constants used across multiple files
from Database import Database               # Store non-Personally Identifiable Information in local (TODO Turso server) SQlite database


class Power:

    def __init__(self, partId: str, isPowerSource: bool, minWattage: float, maxWattage: float, currentVoltage: float, currentAmpDraw: float):
        """ Constructor to initialize a Power.py object

        Arg(s):
            self: Newly created Power object
            partId (String): Out of the Box Astronautics (OOTBA) LLC part number
            isPowerSource (Bool): Is the part a power source (like battery)?
            minWattage (Float): Theoretical minimal power a part draws (while still on) in units of Watts
            minWattage (Float): Theoretical max instant power a part can draw in units of Watts
            currentVoltage (Float): Exact input voltage going into a part at any instant in time in units of Volts (V)
            currentAmpDraw (Float): Exact input current going into a part at any instant in time in units of Amps (A)

        Instance Variable(s):
            senseAPI (Senseable Object): Authenticate and collect realtime data from unoffical sene_energy API

        """
        self.id = partId
        self.isSource = isPowerSource
        self.minWatts = minWattage
        self.maxWatts = maxWattage
        self.volts = currentVoltage
        self.amps = currentAmpDraw

        self.senseAPI = Senseable()

        self.db = Database('Power.db')

    def __repr__(self):
        """ Object "Representation" of Power.py Class (https://www.geeksforgeeks.org/python-__repr__-magic-method)
        """
        return f"Current class variable are: Power(Part ID = '{self.id}', Is part a power source? = {self.isSource}, " \
	       f"Min Power Draw = {self.minWatts}, Max Power Draw = {self.maxWatts}, Current Volts = {self.volts}, Current Amp Draw = {self.amps})"


    def store_data(self, minWattage: float, measuredPowerDraw: float, maxWattage: float, dateAndTimeStamp: str):
        """ Store the key sensor readings and date / time into a SQlite database file

        Arg(s):
            minWattage (Float): Theoretical min power usage, nominally this should be close to 0 Watts
            measuredPowerDraw (Float): Sensor measured power usage (Power = Volts * Amps) in units of Watts
            maxWattage (Float): Theoretical max power usage, nominally this should be greater then measuredPowerDraw
            dateAndTimeStamp (String): The date and time in ISO-8601 format (e.g. 2024-04-07T06:49:22+0000)

        Returns:
            Integer: -1 if database insert failed; otherwise, a value of 1 or greater is expected (1-based indicies)

        """
        isInsertSuccessful = self.db.insert_day_graph_table(oxygenLevel, carbonDioxideLevel, currentPowerDraw, dateAndTimeStamp)

        return isInsertSuccessful


    def load_csv(filepath: str) -> list:
        """ Read a .csv file to create multiple Power.py objects and return as List

        Arg(s):
            filepath (String): Relative filepath to current directory of the .csv file to import

        Return:
            List of Power.py objects defined by the selected .csv file
        """
        parts = []
        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  			# Skip the header row with column descriptions
            for row in reader:
                # Create a Power object for each row and append it to the list, convert string values to appropriate types
                partId = row[0]
                isPowerSource = True if row[1].lower() == 'true' else False
                minWattage = float(row[2])
                maxWattage = float(row[3])
                currentVoltage = float(row[4])
                currentAmpDraw = float(row[5])

                newPowerObject = Power(partId, isPowerSource, minWattage, maxWattage, currentVoltage, currentAmpDraw)

                parts.append(newPowerObject)

        return parts


    def unit_test():
        """ Test power measurement and calculation s with float values accurate to 3 sig figs

        """
        parts = []
        # TODO Get exact specs for AGX Orin
        cpu1 = Power("301-00001-A:1", False, 0.10, 60.0, 11.9, 4.51)
        cpu2 = Power("301-00001-A:2", False, 0.10, 60.0, 11.8, 4.53)
        parts.append(cpu1)
        parts.append(cpu2)
        if GC.DEBUG_STATEMENTS_ON:
            print(f"CPU Part Numbers: {parts[0].id}, {parts[1].id}")
            print(f"CPU Total Min Theoretical Power Draw: {parts[0].minWatts + parts[1].minWatts} Watts")
            print(f"CPU Total Max Theoretical Power Draw: {parts[0].maxWatts + parts[1].maxWatts} Watts")
            print(f"{GC.NUMBER_OF_CPUS} CPU Average Instantaneous Voltage: {(parts[0].volts + parts[1].volts)/GC.NUMBER_OF_CPUS} Volts")
            print(f"{GC.NUMBER_OF_CPUS} CPU Average Instantaneous Current Draw: {(parts[0].amps + parts[1].amps)/GC.NUMBER_OF_CPUS} Amps")


        # TODO Get exact specs for e-con cameras
        camera1 = Power("302-00001-A:1",  False, 0.01, 5.00, 4.99, 0.99)
        camera2 = Power("302-00001-A:2",  False, 0.01, 5.00, 4.99, 0.99)
        camera3 = Power("302-00001-A:3",  False, 0.01, 5.00, 4.99, 0.99)
        camera4 = Power("302-00001-A:4",  False, 0.01, 5.00, 4.99, 0.99)
        camera5 = Power("302-00001-A:5",  False, 0.01, 5.00, 4.99, 0.99)
        camera6 = Power("302-00001-A:6",  False, 0.01, 5.00, 4.99, 0.99)
        camera7 = Power("302-00001-A:7",  False, 0.01, 5.00, 4.99, 0.99)
        camera8 = Power("302-00001-A:8",  False, 0.01, 5.00, 4.99, 0.99)
        camera9 = Power("302-00001-A:9",  False, 0.01, 5.00, 4.99, 0.99)
        cameraA = Power("302-00001-A:10", False, 0.01, 5.00, 4.99, 0.99)
        parts.append(camera1)
        parts.append(camera2)
        parts.append(camera3)
        parts.append(camera4)
        parts.append(camera5)
        parts.append(camera6)
        parts.append(camera7)
        parts.append(camera8)
        parts.append(camera9)
        parts.append(cameraA)

        if GC.DEBUG_STATEMENTS_ON:
            totalMinPower = 0.0
            totalMaxPower = 0.0
            totalInstantaneousVolts = 0.0
            totalInstantaneousAmps = 0.0
            for i in range(GC.NUMBER_OF_CPUS, (GC.NUMBER_OF_CAMERAS + GC.NUMBER_OF_CPUS -1)):
                totalMinPower = totalMinPower + parts[i].minWatts
                totalMaxPower = totalMaxPower + parts[i].maxWatts
                totalInstantaneousVolts = totalInstantaneousVolts + parts[i].volts
                totalInstantaneousAmps = totalInstantaneousAmps + parts[i].amps


            print(f"Camera Part Numbers: {parts[2].id}, {parts[3].id}, {parts[4].id}, {parts[5].id}, {parts[6].id}, " \
                                       f"{parts[7].id}, {parts[8].id}, {parts[9].id}, {parts[10].id}, {parts[11].id}")
            print(f"{GC.NUMBER_OF_CAMERAS} Camera Total Min Theoretical Power Draw: {totalMinPower} Watts")
            print(f"{GC.NUMBER_OF_CAMERAS} Camera Average Instantaneous Voltage: {totalInstantaneousVolts/GC.NUMBER_OF_CAMERAS} Volts")
            print(f"{GC.NUMBER_OF_CAMERAS} Camera Average Instantaneous Current Draw: {totalInstantaneousAmps/GC.NUMBER_OF_CAMERAS} Amps")


        for i in range(len(parts)):
            print(parts[i])


if __name__ == "__main__":
    print("Running Unit Test in Power.py")
    Power.unit_test()

    importedParts = Power.load_csv(GC.CSV_POWER_PARTS)
    print(importedParts)
