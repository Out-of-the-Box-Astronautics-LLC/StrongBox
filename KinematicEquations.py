import math

Class KinematicEquations:

    def __init__(self, velocityFinal, velocityInitial, time, deltaDistance, acceleration):
        (velocityFinal, velocityInitial, time, deltaDistance, acceleration) = determineUnkwown()
        
        if velocityFinal == "?":
            velocityFinal = velocityInitial + acceleration * time