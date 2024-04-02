#!/usr/bin/python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "info@strongbox.space"
__copyright__  = "Copyright 2024"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = "False"
__version__    = "0.0.1"
__doc__        = "Measure real & calculate TODO thearical electrical power usage"
"""

## Standard Library
from math import pow, sqrt, pi  # Power (2^2), Squareroot (4^0.5), and Pi (3.14159) math helper libraries
import csv                      # Import csv file to define power sources and sinks

## 3rd Party Libraries
# Sense Flex Power Measurement Sensor
# https://sense.com/buy
from sense_energy import Senseable

## Internally Developed Library
import GlobalConstants as GC


class Power:

    def __init__(self, partId: str, isPowerSource: bool, minWattage: float, maxWattage: float, currentVoltage: float, currentAmpDraw: float): #, relativeCsvFilepath: str, parts: list):
        """ Constructor to initialize a Power.py object

        Arg(s):
            self: Newly created Power object
            partId (String): Out of the Box Astronautics (OOTBA) LLC part number
            isPowerSource (Bool): Is the part a power source (like battery)?
            minWattage (Float): Theorical minimal power a part draws (while still on) in units of Watts
            minWattage (Float): Theorical max instant power a part can draw in units of Watts
            currentVoltage (Float): Exact input voltage going into a part at any instant in time in units of Volts (V)
            currentAmpDraw (Float): Exact input current going into a part at any instant in time in units of Amps (A)
            #relativeCsvFilepath (String): Relative filepath to current directory of .csv file to import
            #parts (List): A List of Power.py objects

        Instance Variable(s):
            id          (String): TODO
            isSource      (Bool): TODO
            minWatts     (Float): TODO
            maxWatts     (Float): TODO
            volts        (Float): TODO
            amps         (Float): TODO
            csvFilepath (String): TODO
            parts     (Power.py): TODO
        """
        self.id = partId
        self.isSource = isPowerSource
        self.minWatts = minWattage
        self.maxWatts = maxWattage
        self.volts = currentVoltage
        self.amps = currentAmpDraw
        #self.csvFilepath = relativeCsvFilepath
        #self.parts = []

    def __repr__(self):
        """ TODO
        """
        return f"Power('{self.id}', {self.isSource}, {self.minWatts}, {self.maxWatts}, {self.volts}, {self.amps})"


    def load_csv(filepath: str):
        """ Read a .csv file and create Power.py objects

        Arg(s):
            filepath (String): Relative filepath to current directory of .csv file to import

        Return:
            List of Power.py object defined by the select .csv file
        """
        parts = []
        with open(filepath, newline='') as csvfile:
            # Read the CSV file
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip the header row
            for row in reader:
                # Create a Power object for each row and append it to the list
                # Convert string values to appropriate types
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
            print(f"CPU Total Min Theorical Power Draw: {parts[0].minWatts + parts[1].minWatts} Watts")
            print(f"CPU Total Max Theorical Power Draw: {parts[0].maxWatts + parts[1].maxWatts} Watts")
            print("TODO")
            print("TODO")

        # TODO Get exact specs for e-con cameras
        camera1 = Power("302-00001-A:1", False, 0.01, 5.00, 4.99, 0.99)
        camera2 = Power("302-00001-A:2", False, 0.01, 5.00, 4.99, 0.99)
        camera3 = Power("302-00001-A:3", False, 0.01, 5.00, 4.99, 0.99)
        camera4 = Power("302-00001-A:4", False, 0.01, 5.00, 4.99, 0.99)
        camera5 = Power("302-00001-A:5", False, 0.01, 5.00, 4.99, 0.99)
        camera6 = Power("302-00001-A:6", False, 0.01, 5.00, 4.99, 0.99)
        camera7 = Power("302-00001-A:7", False, 0.01, 5.00, 4.99, 0.99)
        camera8 = Power("302-00001-A:8", False, 0.01, 5.00, 4.99, 0.99)
        parts.append(camera1)
        parts.append(camera2)
        parts.append(camera3)
        parts.append(camera4)
        parts.append(camera5)
        parts.append(camera6)
        parts.append(camera7)
        parts.append(camera8)
        if GC.DEBUG_STATEMENTS_ON:
            totalMinPower = 0.0
            totalMaxPower = 0.0
            for i in range(2, 7):
                totalMinPower = totalMinPower + parts[i].minWatts
                totalMaxPower = totalMaxPower + parts[i].maxWatts

            print(f"Camera Part Numbers: {parts[2].id}, {parts[3].id}, TODO")
            print(f"Camera Total Min Theorical Power Draw: {totalMinPower} Watts")
            print(f"Camera Total Max Theorical Power Draw: {totalMaxPower} Watts")
            print("TODO")
            print("TODO")


        for i in range(len(parts)):
            print(parts[i])


if __name__ == "__main__":
    print("Running Unit Test in Power.py")
    #Power.unit_test()

    importedParts = Power.load_csv(GC.CSV_POWER_PARTS)
    print(importedParts)
