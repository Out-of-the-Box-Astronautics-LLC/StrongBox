#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "info@strongbox.space"
__copyright__  = "Copyright 2024"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = "False"
__version__    = "0.0.1"
__doc__        = "Calculate unknown value(s) of motion using 5 kinematic equations"
"""

## Standard Library
from math import pow, sqrt, pi

## 3rd Party Libraries
# TODO Robot arm inverse & forward kinematics
# https://pypi.org/project/visual-kinematics/
# from visual_kinematics.RobotTrajectory import *

# PhysiPy is a powerful and versatile Python library designed to streamline physics calculations
# https://github.com/rohankishore/PhysiPy
import PhysiPy


## Internally Developed Library
import GlobalConstants as GC


class KinematicEquations:

    def __init__(self, velocityFinal: float, velocityInitial: float, time: float, deltaDistance: float, acceleration: float):
        """ Constructor to initialize a KinematicEquations.py object

        Arg(s):
            self: Newly created KinematicEquations object
            velocityFinal   (Float): A +/- scalar velocity of an item slower then 100 km/s
            velocityInitial (Float): A +/- scalar velocity of an item slower than 100 km/s
            time (Float): Positive time value less than 100,000,000 seconds
            deltaDistance (Float): A +/- scalar displacement of an item less than 200,000,00 km
            acceleration (Float): A +/- scalar change in velocity in units of meters per second per secnds, decceleration against gravity is negative

        Instance Variable(s):
           isValid (Boolean): Is the input list of arguments enough to solve the 5 equations?
           eq1 (String): The 1st kinematic equation of motion solving for delta distance
           eq2 (String): The 2nd kinematic equation of motion solving for final velocity
           eq3 (String): The 3rd kinematic equation of motion solving for final velocity
           eq4 (String): The 4th kinematic equation of motion solving for delta distance
           eq5 (String): The 5th kinematic equation of motion solving for delta distance

           vf (Float): Long term storage of the calculated value for final velocity
           vi (Float): Long term storage of the calculated value for initial velocity
           t  (Float): Long term storage of the calculated value for time
           dd (Float): Long term storage of the calculated value for delta distance
           a  (Float): Long term storage of the calculated value for acceleration
        """
        unknowns = KinematicEquations.determine_unkwown(velocityFinal, velocityInitial, time, deltaDistance, acceleration)

        self.isValid = False
        self.eq1 = "dd = vi * t + (0.5 * a * t^2)"
        self.eq2 = "vf^2 = vi^2 + (2.0 * a * dd)"
        self.eq3 = "vf = vi + a *t"
        self.eq4 = "dd = vf * t - (0.5 * a * t^2)"
        self.eq5 = "dd = 0.5 * (vf + vi) * t"

        if sum(unknowns) > 2:
            if GC.DEBUG_STATEMENTS_ON: print("ERROR: Too many unknowns to calculate the answer")

        else:
            self.isValid = True
            self.vf = velocityFinal
            self.vi = velocityInitial
            self.t = time
            self.dd = deltaDistance
            self.a = acceleration

            # TODO: What are the 5 combinations of arguments?
            # Calculate Final Velocity in FOUR different ways
            if (unknowns[GC.VF]) and not (unknowns[GC.VI] or unknowns[GC.T] or unknowns[GC.DD] or unknowns[GC.A]):
                print(f"Using {self.eq4} equation since ONLY final velocity = {velocityFinal} is unknown")
                self.vf = (deltaDistance + (0.5 * acceleration * pow(time, 2))) / time

            elif (unknowns[GC.VF] and unknowns[GC.T]) and not (unknowns[GC.VI] or unknowns[GC.DD] or unknowns[GC.A]):
                print(f"Using {self.eq2} equation since final velocity = {velocityFinal} & time = {time} are unknown")
                vf_2 = pow(velocityInitial, 2) + (2 * acceleration * deltaDistance)
                self.vf = sqrt(vf_2)

            elif (unknowns[GC.VF] and unknowns[GC.DD]) and not (unknowns[GC.VI] or unknowns[GC.T] or unknowns[GC.A]):
                print(f"Using {self.eq3} equation since final velocity = {velocityFinal} & delta distance = {deltaDistance} are unknown")
                self.vf = velocityInitial + acceleration * time

            elif (unknowns[GC.VF] and unknowns[GC.A]) and not (unknowns[GC.VI] or unknowns[GC.DD] or unknowns[GC.T]):
                print(f"Using {self.eq5} equation since final velocity = {self.vf} & acceleration = {a} are unknown")
                self.vf = ((2 * deltaDistance) / time) - velocityInitial

            elif (unknowns[GC.VI] and unknowns[GC.DD]) and not (unknowns[GC.VF] or unknowns[GC.T] or unknowns[GC.A]):
                pass  #TODO


            # Calculate Time
            elif unknowns[GC.T]:
                t = GC.TODO


            # Calculate Delta Distance
            elif (unknowns[GC.DD]) and not (TODO):
                dd = GC.TODO

            elif (unknowns[GC.DD] and unknowns[GC.VF]) and not (TODO):
                dd = GC.TODO


            # Calculate Time
            elif (unknowns[GC.T] and unknowns[GC.VF]) and not (unknowns[GC.VI] or unknowns[GC.DD] or unknowns[GC.A] or self.acceleration == 0):
                print(f"Using {self.eq1} equation since ONLY time = {t} is unknown and acceleration does NOT equal 0")
                t = (sqrt(2 * acceleration * deltaDistance + pow(velocityInitial, 2)) - velocityInitial) / acceleration


            # Calculate Acceleration
            elif unknowns[GC.A] and unknowns[GC.DD]:
                self.a = (velocityFinal - velocityInitial) / time
                self.dd = (velocityInitial * time) + (0.5 * acceleration * pow(time, 2))

            else:
                if GC.DEBUG_STATEMENTS_ON: print("WARNING: All arguments have valid known float values, nothing to calculate")


    def determine_unkwown(vf, vi, t, d, a):
        """ Determine if input arguments are valid float or interger numbers or a "?" string to be calculated

        Arg(s):
            vf (Float or String):
            vi (Float or String):
            t  (Float or String):
            d  (Float or String):
            a  (Float or String):

        Returns:
            List of Booleans values, based on if an argument is a float (False) or a string (True)
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


    def scalarize_vector(x: float, y: float, z: float):
        """ Convert 3 dimension vector inside a magnitude without direction

        """
        scalarVelocity = sqrt(pow(x, 2) + pow(y, 2) + pow(z, 2))

        return scalarVelocity


    def calculate_potential_energy(mass: float, gravity: float, height: float):
        """ Calculate the potential energy (PE) an item has
        
        Arg(s):
            mass (Float): Mass in kilograms
            gravity (Float): Acceleration dur to gravity in meters per seconds per second
            height (Float): Scalar distance in meters above a reference point
        """
        return (mass * gravity * height) 


    def calculate_kinetic_energy(mass: float, velocity: float):
        """ Calculate the kinetic energy (KE) an item has
        
        Arg(s):
            mass (Float): Mass in kilograms
            velocity (Float): Scalar velocity in meters per second
        """
        return (0.5 * mass * velocity * velocity) 

    
    def unit_test():
        """ Checked using the following online calculators

            https://physicscatalyst.com/calculators/physics/kinematics-calculator.php
            https://study.com/academy/lesson/kinematic-equations-list-calculating-motion.html
        """
        deltaDistance = 111.0 - 0.0
        answer1 = KinematicEquations("?", 0.0, "?", 111.0, GC.G_EARTH)
        print(f"Vf = {answer1.vf} | Vi = {answer1.vi} | Time = {answer1.t} | Displacement = {answer1.dd} | Accel = {answer1.a}")

        answer2 = KinematicEquations(44.69, 571.0, "?", 319_000.0, GC.G_MOON)
        print(f"Vf = {answer2.vf} | Vi = {answer2.vi} | Time = {answer2.t} | Displacement = {answer2.dd} | Accel = {answer2.a}")

        xVelocity = 5.03
        yVelocity = 20.10
        zVelocity = 22.56
        scalarInput = KinematicEquations.scalarize_vector(xVelocity, yVelocity, zVelocity)
        print(f"Initial Velocity: {scalarInput} m/s = [{xVelocity}, {yVelocity}, {zVelocity}]")
        xAxis = KinematicEquations(xVelocity, 50.8, "?", 100, 0)
        yAxis = KinematicEquations(yVelocity, 571.0, "?", -100_000, 0)
        zAxis = KinematicEquations(zVelocity, 10.2, "?", 319_000.0, GC.G_MOON)
        print(f"Vfx = {xAxis.vf} | Vix = {xAxis.vi} | Time = {xAxis.t} | X-Axis Displacement = {xAxis.dd} | X-Axis Accel = {xAxis.a}")
        print(f"Vfy = {yAxis.vf} | Viy = {yAxis.vi} | Time = {yAxis.t} | Y-Axis Displacement = {yAxis.dd} | Y-Axis Accel = {yAxis.a}")
        print(f"Vfz = {zAxis.vf} | Viz = {zAxis.vi} | Time = {zAxis.t} | Z-Axis Displacement = {zAxis.dd} | Z-Axis Accel = {zAxis.a}")
        scalarOutput = KinematicEquations.scalarize_vector(xAxis.vf, yAxis.vf, zAxis.vf)
        print(f"Final Velocity: {scalarOutput} m/s = [{xAxis.vf}, {yAxis.vf}, {zAxis.vf}]")


if __name__ == "__main__":
    print("Running Unit Test in KinematicEquations.py")
    KinematicEquations.unit_test()
