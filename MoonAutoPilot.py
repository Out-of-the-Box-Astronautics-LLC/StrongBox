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
# Analyze the size and location of Moon craters to navigate down to the surface https://wms.lroc.asu.edu/lroc

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
import Crater as cr             # Crater class to define name, size, and location of craters
import Database as db           # SQLite database to store crate locations


class MoonAutoPilot:

    # Class global constants
    GRAY_SCALE_MODE = 0
    RGB_MODE = 1
    MIN_CRATER_PIXEL_DIAMETER = 10

    def __init__(self, name: str):
        self.spacecraftName = name
        self.altitude = 384_400_000     # Average distance between the Earth and Moon
        self.attitude = [0, 0, 0, 0]    # Quaternion-Based Kalman Filter https://github.com/liviobisogni/quaternion-kalman-filter
        self.referenceMoonImages = []
        self.referenceSpaceImages = []
        self.flameyEndDown = False      # https://xkcd.com/1133/ & https://imgs.xkcd.com/comics/up_goer_five.png and https://twitter.com/erdayastronaut/status/1433640020288618497?s=61&t=eS1giEUgStrI7lLV1Klx5Q
        self.craterDB = db.Database("MoonCraterPositions.db")


    def load_image(self, filename: str, mode: int):
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

    def find_crater_centers(self, image) -> bool:
        """

        Return False if crater center couldn't be determine, True otherwise

        https://zed.dev/docs/collaboration
        https://zed.dev/docs/assistant-panel
        Remember that detecting ovals can be affected by many factors like perspective distortions, occlusions, and noise in the image, so you might need to adjust the `aspect_ratio_thresh` and other preprocessing steps depending on your actual images and requirements.
        For ovals detection, you would need to analyze the contours and the aspect ratio of their bounding rectangles, as well as their degree of elongation:
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply threshold or Canny edge detection
        ret, thresh = cv2.threshold(gray, 127, 255, 0)

        # Find contours in the thresholded image
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Fit an ellipse to the contour
            if len(contour) >= 5:  # Requires at least 5 points to fit an ellipse
                ellipse = cv2.fitEllipse(contour)

                # Extract the axes lengths of the ellipse
                (major_axis, minor_axis) = ellipse[1]

                # Calculate the aspect ratio of the ellipse
                aspect_ratio = max(major_axis, minor_axis) / min(major_axis, minor_axis)

                # Define a threshold for the aspect ratio to distinguish between circles and ovals
                aspect_ratio_thresh = 1.2  # Adjust this value based on your specific requirements

                # If aspect ratio is greater than the threshold, it's an oval (not a perfect circle)
                if aspect_ratio > aspect_ratio_thresh:
                    # Draw the fitted ellipse on the original image
                    cv2.ellipse(image, ellipse, (255, 0, 0), 2)

        # Show the output image with the detected ovals
        cv2.imshow('Detected Ovals', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        """
        circleFound = False
        centerDetermined = False

        # Starte image manipulatiom: Convert to grey scale image & apply GaussianBlur to reduce noise and improve detection
        grayScaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        grayScaleImageBlurred = cv2.GaussianBlur(grayScaleImage, (9, 9), 0)

        # Start looking for craters by location all ovals and circles in the image larger then 10 pixels () in diameter
        circles = cv2.HoughCircles(grayScaleImageBlurred, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=0, maxRadius=0)

        if circles is not None:
            # Convert the circle parameters to integers
            circles = np.round(circles[0, :]).astype("int")

            # Loop over the circles and draw them on the original image
            for (x, y, r) in circles:
                cv2.circle(image, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(image, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            # Show the output image with the detected circles
            if GC.DEBUG_STATEMENTS_ON:
                cv2.imshow('Detected Circles', image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                print(f"Closing debugging window: 'Detected Circles'")
        else:
            self.craterDB.insert_debug_logging_table("No circles dectected")


        circleDiameter = GC.TODO
        if circleDiameter > MoonAutoPilot.MIN_CRATER_PIXEL_DIAMETER:
            circleFound = True

        if circleFound:
            # TODO
            centerDetermined = True

        if (circleFound and centerDetermined):
            return False

        return True


    def store_crater_grid_pattern(self, x: int, y: int):
        pass


    def store_crater_coordinates(self, c: cr.Crater):
        latitude = GC.GRID_CONSTANT * c.xCoordinate
        longitude = GC.GRID_CONSTANT * c.yCoordinate
        self.craterDB.insert_crater(latitude, longitude)


    def show_image_for_debugging(self, name, img) -> None:
        """
        Prams:Img to be printed
        :return: NA
        PRESS KEY TO PROCEED.
        """
        # Get image dimensions
        height, width, channels = img.shape
        for y_pixel in range(height):
            for x_pixel in range(width):
                pixel_value = img[y_pixel, x_pixel]

        cv2.imshow(name, img)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            if GC.DEBUG_STATEMENTS_ON: print(f"Closing debugging window: '{name}'")


if __name__ == "__main__":
    strongBox = MoonAutoPilot("AirPlant-1")
    images = ['NearSurveyor6_HeightUnknown.png']
    img = strongBox.load_image(images[0], MoonAutoPilot.RGB_MODE)
    strongBox.show_image_for_debugging("Moon AutoPilot v0.1" , img)
