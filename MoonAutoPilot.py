#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = False
_version__    = "0.0.1"
"""
# Analyze the size and location of Moon craters to navigate down to the surface


# Useful standard Python system jazz
import sys, time, traceback, argparse, string

# Allow program to extract filename of the current file
import os

# 
# https://pypi.org/project/opencv-python/ 
import cv2
import numpy as np

class MoonAutoPilot:

    def __init__(self):
        pass


    def load_image(self, filename: str, mode: int):
        """ Load a PNG image on the local harddrive into RAM

        Arg(s):
            filename (string): .PNG filename to load into memory
            mode (interger): 0 to read image in grayscale mode or 1 to read image in rgb mode.

        Returns:
            img (cv2) : -- Image header object
        """
        # TODO: CHECK FOR .PNG FILE EXTENSION
        path = "images/" + filename
        print(" path " + path)

        img = cv2.imread(path, mode)

        return img
    
    
if __name__ == "__main__":
    strongBox = MoonAutoPilot()
    strongBox.load_image("NearSurveyor6_HeightUnknown.png", 0)
