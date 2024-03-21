#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "info@strongbox.space"
__copyright__  = "Copyright 2024"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = "False"
__version__    = "0.0.1"
__doc__        = "Calculate one of the unknown values of motion using 1 of 4 equations"
"""

## Standard Library
import math

## Internal Library
import GlobalConstants as GC


class KinematicEquations:

    def __init__(self, velocityFinal, velocityInitial, time, deltaDistance, acceleration):
        """

        """
        unknowns = KinematicEquations.determineUnkwown(velocityFinal, velocityInitial, time, deltaDistance, acceleration)
        print(f"Unknown arguments OUTSIDE function are ", unknowns)

        self.isValid = False

        if sum(unknowns) > 2:
            if GC.DEBUG_STATEMENTS_ON: print("ERROR: Too many unknowns to calculate the answer")

        else:
            self.isValid = True
            self.vf = velocityFinal
            self.vi = velocityInitial
            self.t  = time
            self.dd = deltaDistance
            self.a  = acceleration

            # TODO: What are the 5 combinations of arguments?
            if unknowns[GC.VF] and not (unknowns[GC.VI] or unknowns[GC.T] or unknowns[GC.DD] or unknowns[GC.A]):
                vf_2 = math.pow(velocityInitial, 2) + (2 * acceleration * deltaDistance)
                self.vf = math.pow(vf_2, 0.5)

            elif unknowns[GC.VI]:
                vi_2 = math.pow(velocityFinal, 2) - (2 * acceleration * deltaDistance)
                self.vi = math.pow(vi_2, 0.5)

            elif unknowns[GC.T]:
                t = GC.TODO

            elif unknowns[GC.DD]:
                dd = GC.TODO

            elif unknowns[GC.A] and unknowns[GC.DD]:
                self.a = (velocityFinal - velocityIntial) / time
                self.dd = (velocityInitial * time) + (0.5 * acceleration * math.pow(time, 2))

            else:
                if GC.DEBUG_STATEMENTS_ON: print("WARNING: All arguments have valid known float values, nothing to calculate")


    def determineUnkwown(vf, vi, t, d, a):
        """

        """
        unknownArguments = [False, False, False, False, False]

        try:
            velocityFinal = float(vf)
        except ValueError:
            unknownArguments[GC.VF] = True

        try:
            velocityIntial = float(vi)
        except ValueError:
            unknownArguments[GC.VI] = True

        try:
            time = float(t)
        except ValueError:
            unknownArguments[GC.T] = True

        try:
            deltaDistance = float(d)
        except ValueError:
            unknownArguments[GC.DD] = True

        try:
            acceleration = float(a)
        except ValueError:
            unknownArguments[GC.A] = True

        return unknownArguments


    def unit_test():
        """ Checked using the following online calculators

            https://physicscatalyst.com/calculators/physics/kinematics-calculator.php
        """
        deltaDistance = 122 - 11
        (vf, vi, t, dd, a) = KinematicEquations("?", 0, 2.9, deltaDistance, 9.81)

if __name__ == "__main__":
     test = KinematicEquations("?", "?", "?", 111, 9.81)
     test = KinematicEquations(44.69, 571.0, "?", "?", 1.62)
#    test = KinematicEquations(44.69, 0, 2.9, 11, 9.81)
