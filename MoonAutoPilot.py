#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = False
__version__    = "0.0.1"
"""
# Analyze the size and location of Moon craters to navigate down to the surface https://wms.lroc.asu.edu/lroc

# Disable PyLint linting messages that seem unuseful
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name
# pylint: disable=global-statement

## Standard Python libraries
import sys                                      # Determine which OS this code is running on https://docs.python.org/3/library/sys.html
from datetime import datetime, time, timedelta  # Manipulate calendar dates & time objects https://docs.python.org/3/library/datetime.html
import traceback
import argparse
import os                                       # Allow program to extract filename of the current file
#TODO REMOVE? import string 


## 3rd party libraries
# OpenCV (Open Source Computer Vision Library) for computer vision and machine learning https://opencv.org
# https://pypi.org/project/opencv-python/ 
import cv2

# NumPy (Numerical Python)is an universal standard for working with numerical data
# https://numpy.org/install/
import numpy as np


## Internally developed modules
import GlobalConstants as GC    # Useful global constants used across multiple files

class MoonAutoPilot:

    GRAY_SCALE_MODE = 0
    RGB_MODE = 1

    def __init__(self, name: str):
        self.spacecraftName = name
        self.altitude = 384_400_000     # Average distance between the Earth and Moon
        self.attitude = [0, 0, 0, 0]    # Quaternion-Based Kalman Filter https://github.com/liviobisogni/quaternion-kalman-filter
        self.referenceMoonImages = []
        self.referenceSpaceImages = []
        self.flameyEndDown = False      # https://xkcd.com/1133/ & https://imgs.xkcd.com/comics/up_goer_five.png and https://twitter.com/erdayastronaut/status/1433640020288618497?s=61&t=eS1giEUgStrI7lLV1Klx5Q


    def load_image(self, filename: str, mode: int) -> cv2:
        """ Load a PNG image on the local harddrive into RAM for processing

        Arg(s):
            filename (string): .PNG filename to load into memory
            mode (interger): 0 to read image in grayscale mode or 1 to read image in rgb mode.

        Returns:
            img (cv2): Image header object
        """
        filenameParts = filename.split('.')
        if filenameParts[1].upper() != "PNG" and filenameParts[1].upper() != "JPEG":
          return None  
    
        filepath = "images/" + filename
        if GC.DEBUG_STATEMENTS_ON: print(f"Using image at filepath '{filepath}'")

        img = cv2.imread(filepath, mode)

        return img
    
    
    def show_image_for_debugging(self, name, img) -> None:
        """
        Prams:Img to be printed
        :return: NA
        PRESS KEY TO PROCEED.
        """
        cv2.imshow(name, img)
        cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
        if cv2.waitKey(0) == ord('q'):
            if GC.DEBUG_STATEMENTS_ON: print(f"Closing debugging window '{name}'")
    
    
if __name__ == "__main__":
    strongBox = MoonAutoPilot("AirPlant-1")
    images = ['NearSurveyor6_HeightUnknown.png']
    img = strongBox.load_image(images[0], MoonAutoPilot.RGB_MODE)
    strongBox.show_image_for_debugging("Moon AutoPilot" , img)
