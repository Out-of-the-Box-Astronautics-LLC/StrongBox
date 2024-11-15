#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2024"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = "False"
__version__    = "0.0.1"
"""
#  Data structure to define the name, size, and location of Moon craters

# Disable PyLint (VSCode) linting messages that seem unuseful
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name
# pylint: disable=global-statement
#
# Disable Pyright (Zed IDE) linting messages that seem unuseful
# https://pypi.org/project/pyright/
# TODO https://github.com/microsoft/pyright/blob/main/docs/getting-started.md
# PYRIGHT_PYTHON_IGNORE_WARNINGS = True
# Using Command Line Interface (CLI): pyright --verifytypes TODO --ignoreexternal MainApp.py

## Internally developed modules
import GlobalConstants as GC                            # Useful global constants used across multiple files

class Crater:

    def __init__(self, name: str, diameter: float, location: tuple):
        """ Constructor for Crater objects that define phyically traits about a large (great than 100 meters) Moon crate

        Arg(s):
            name (String): NASA offical name for a crater if it exists; otherwise, None
            diameter (Float): Diameter of a crater in meters
            location (Tuple): Interger custom grid position and Float 'GPS' position of a craters center (for circular craters) or semi and minor axis crossing point (for elliptical craters with eccentricity greater than 0.200) e.g. (0000420, 0006969, 02.67890, 89.12345)

        """
        self.name = str(name)

        # Check that crater sizes are above a reasonable lower bound based on camera resolution to see small crater and a reasonable upper bound based on the Moon full equatorial distance
        if GC.MIN_CAMERA_DEFINED_CRATER_DIAMETER <= diameter and diameter <= GC.MAX_PHYSICAL_CRATER_DIAMETER:
            self.diameter = diameter
        else:
            if GC.DEBUG_STATEMENTS_ON: print("TODO")
            return

        # Check that interger grid input parameters are valid
        if location[0] <= GC.MAX_X_GRID and location[1] <= GC.MAX_Y_GRID:
            self.xCoordinate = location[0]
            self.yCoordinate = location[1]
        else:
            if GC.DEBUG_STATEMENTS_ON: print("TODO")
            return

        # Check that latitude & longitude input parameters are valid East/West and North/South values
        if 180 >= location[2] and locatiom[2] >= -180:
            self.longitude = location[2]                 # Units are decimal arc degrees
        else:
            if GC.DEBUG_STATEMENTS_ON: print("TODO")
            return

        if 90 >= location[3] and locatiom[3] >= -90:
            self.latitude = location[3]                 # Units are decimal arc degrees
        else:
            if GC.DEBUG_STATEMENTS_ON: print("TODO")
            return


    def get_offical_name(self) -> str:
        if self.name == "":
            if GC.DEBUG_STATEMENTS_ON: print(f"Crater at ({self.latitude}, {self.longitude}) doesn't have an offical name.")
            return None
        else:
            return self.name


    def get_diameter(self) -> float:
        return self.diameter        # Units are meters



    def get_lat_long_position(self) -> tuple:
        """ Get Moon 'GPS' coordinate of crater 'center'

        Arg(s):
            NONE

        Returns:
            Float tuples with (+North/-South, -East/+West) values

        """
        lat = self.latitude
        long = self.longitude

        return (lat, long)


    def get_x_y_position(self) -> tuple:
        """ Get Moon 'GPS' coordinate of crater 'center'

        Arg(s):
            NONE

        Returns:
            Interger tuples with (+North/-South, -East/+West) values

        """
        x = self.xCoordinate
        y = self.xyCoordinate

        return (x, y)
