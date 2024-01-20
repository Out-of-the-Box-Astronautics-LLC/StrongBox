# !/usr/bin/env python3
"""
__author__  = "Blaze Sanders"
__email__   = "blaze.d.a.sanders@gmail.com"
__company__ = "CocoTaps"
__status__  = "Development"
__date__    = "Late Updated: 2020-07-15"
__doc__     = "Script to analyze the size of coconuts & scan QR codes, so that we make 99% reliable Tapomatic"
"""

# Useful standard Python system jazz
import sys, time, traceback, argparse, string

# Allow program to extract filename of the current file
import os

# Robotic Beverage Technologies code for custom data logging and terminal debugging output
from Debug import *

try:
    # OpenCV magic
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_table_of_contents_imgproc/py_table_of_contents_imgproc.html
    import cv2
    import numpy as np

except ImportError:
    currentProgramFilename = os.path.basename(__file__)
	ImportDebugObject = Debug(True, currentProgramFilename)
    ImportDebugObject.Dprint("Run ComputerVision.py with python not PYTHON3")


# Create a command line parser
# parser = argparse.ArgumentParser(prog = "Tapomatic Computer Vision", description = __doc__, add_help=True)
# parser.add_argument("-f", "--filename", type=str, default="Update.py", help="Local or cloud software to be loaded on ki$
# parser.add_argument("-l", "--loop", type=int, default=0, help="Set to 1 to loop this driver program.")
# args = parser.parse_args()

##GUIDE TO BEGINNERS
##Treat the Image as a matrix and that is how computers see and store the images.
## [x,y]

class ComputerVision():
    def printImageForTestingPurpose(self, name, img):
        """
        Prams:Img to be printed
        :return: NA
        PRESS KEY TO PROCEED.
        """
        cv2.imshow(name, img)
        cv2.waitKey(0) & 0xFF
        cv2.destroyAllWindows()
        if cv2.waitKey(0) == ord('q'):
            print('Done')

    def auto_canny(self, image, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(image)
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
        # return the edged image
        return edged

    def LoadImage(self, filename, mode):
        """
        Load a PNG image on the local harddrive into RAM

        Key arguments:
        filename -- PNG file to load into memory
        mode - 0 to read image in grayscale mode.
               1 to read image in rgb mode.

        Return value:
        img -- Image header object
        """
        print("TODO: CHECK FOR >PNG?")
        path = "static/CVImages/" + filename
        print(" path " + path)
        img = cv2.imread(path, mode)  # 0 for black, 1 for rgb
        return img

    def FindScale(self):
        """
        Find the ruler or object in background that define scale between pixel and real life size

        """

        ## 6 and from the cv code the distance is 6 then we are good
        print("TODO: Very hard")

    def IncreaseContrast(self, image, percentage):
        """
        Create new image object with increased contrast to make edge dection easier

        Key arguments:
        image --
        percentage -- ??? TODO Blaze please read the following explanation and let me know new arguments suitable for this function.
        Image Contrast and Brightness can be formulated like the following.
        g(x) = af(x)+b  where f(x) is the old image and g(x) is the new image.
        To increase the contrast, multiply each pixel by constant a (GAIN) and add a
        constant b (BIAS). To increase the contrast choose a > 1 and to decrease choose a < 1

        """
        # copyImage  = [ [0...0][0...0][0...0][0...0]]
        # copyImage = np.zeros(image.shape, image.dtype) # dtype is the data type ex:int
        # newImg = loop x,y,c (old_image) * a + b

        a = 1.5  # [1.0..3.0] Responsible for Contrast #TODO GET PARAMS
        b = 35  # [0.. 100]  Responsible for Brightness #TODO GET PARAMS
        newImg = cv2.convertScaleAbs(image, alpha=a, beta=b)
        return newImg

    def ConvertToBW(self, colorImage):
        """
        Convert image to Black & White to make processing faster and more discrete

        Key arguments:
        image --

        Return value:
        bwImg -- Black & White image header object

        """

        grayImg = cv2.cvtColor(colorImage, cv2.COLOR_BGR2GRAY)
        ## Input 1st Param Image
        # 2nd Param : Threshold, if the pixel is less than this, value will be 0 (black) or set to 3rd param (white)
        # Usually coconuts are close to white, set this to > 200. so that they convert to black
        ##TODO NEED TO REVISIT, may need to have iterations and as well
        (threshold, bwImg) = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY)
        self.printImageForTestingPurpose('GREY IMAGE', bwImg)
        return bwImg

    def ConvertToGray(self, colorImage):
        """
        Convert image to Black & White to make processing faster and more discrete

        Key arguments:
        image --

        Return value:
        bwImg -- Black & White image header object

        """

        grayImg = cv2.cvtColor(colorImage, cv2.COLOR_BGR2GRAY)
        self.printImageForTestingPurpose('GREY IMAGE', grayImg)

        return grayImg

    def FindSideToSideEdges(self, grey_image):
        """
        Scan image left to right and find two mostly vertical lines

        Key arguments:
        bwImage -- Black & White image to analyze

        Return value:
        columnList -- Two item list holding equation for a line
        """
        kernel_size = 5
        blur_gray = cv2.GaussianBlur(grey_image, (kernel_size, kernel_size), 0)
        self.printImageForTestingPurpose('BLURRED', blur_gray)
        low_threshold = 25
        high_threshold = 75
        edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
        self.printImageForTestingPurpose('EDGES USING CANNY', edges)

        vertical = np.copy(blur_gray)
        # [vert]
        # Specify size on vertical axis
        rows = vertical.shape[0]
        verticalsize = rows // 30
        # Create structure element for extracting vertical lines through morphology operations
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
        # Apply morphology operations
        vertical = cv2.erode(vertical, verticalStructure)
        vertical = cv2.dilate(vertical, verticalStructure)
        # Show extracted vertical lines
        self.printImageForTestingPurpose("vertical", vertical)
        # [vert]
        # [smooth]
        # Inverse vertical image
        vertical = cv2.bitwise_not(vertical)
        self.printImageForTestingPurpose("vertical bit", vertical)

        imshape = grey_image.shape
        print(imshape)
        vertices = np.array([[(0, imshape[0]), (150, imshape[1]), (500, imshape[1]), (imshape[1], imshape[0])]],
                            dtype=np.int32)
        cv2.fillPoly(grey_image, vertices, None)
        masked_edges = cv2.bitwise_and(edges, grey_image)
        self.printImageForTestingPurpose('Masked Edges', masked_edges)
        ##TODO Copied code from the medium blog.... have to see the test results.???
        rho = 0.75  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 20  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 20  # minimum number of pixels making up a line
        max_line_gap = 20  # maximum gap in pixels between connectable line segments
        line_image = np.copy(grey_image) * 0  # creating a blank to draw lines on
        lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 25, 255), 5)

        lines_edges = cv2.addWeighted(grey_image, 0.8, line_image, 1, 0)
        self.printImageForTestingPurpose('Lines Edges New', lines_edges)

        columnList = ["y=100/98x-420", "y=-100/97+690"]  # Temp List
        return columnList

    def FindTopToBottomEdges(self, bwImage):
        """
        Scan image top to bottom and find two mostly horizontal lines

        Key arguments:
        bwImage -- Black & White image to analyze

        Return value:
        rowList -- Two item list holding equation for a line
        """

        rowList = ["y=1/98x-69", "y=-1/97+70"]  # Temp List
        return rowList

    def MeasurePixels(self, edge1, edge2):
        """

        Return values:
        numOfPixels -- Number of pixels between two nearly perpendicular lines
        """

        return numOfPixels

    def CreateQRcode():
        """
        Used MyQR https://github.com/sylnsfar/qrcode and/or https://www.qrcode-monkey.com/#text to made Image QR codes with return intergers 

        Key arguments:
        NONE

        Return value:
        qrCodeInt -- Interger, corresponding to the CocoDrink.py CONSTANT for each bottle flavor and/or health additiive
        """

        return qrCodeInt

	def ScanQRcode():
		"""
		Use https://manpages.debian.org/jessie/fswebcam/fswebcam.1.en.html
		https://www.raspberrypi.org/documentation/usage/webcams/
		https://www.raspberrypi.org/forums/viewtopic.php?t=142489
		https://elinux.org/RPi_USB_Webcams
		https://www.raspberrypi.org/forums/viewtopic.php?t=23800
		
		"""
		img = cv2.imread(path, mode)  # 0 for black, 1 for rgb
		check_call("fwswebcam -d /dev/video0 - r 960x720 pic.jpg" , shell=True)

		img = /pic.jpg

		return img

if __name__ == "__main__":
    object = ComputerVision()
    # The CV flow should probably be done in the following order
    ##TODO Remove this later, only testing purposes loading images statically here.
    filename = "coco_1.jpg"
    img = object.LoadImage(filename, 1)
    ##TODO REMOVE LATER, Will open loaded images in a seperate window.
    object.printImageForTestingPurpose('COCO IMAGE ORIGINAL', img)

    ##TODO COMMENT UNTIL MURALI GET SOME CLARITY FROM BLAZE ON WHAT TO DO.
    # scale = FindScale(filename)  #TODO HARD

    contrastColorImg = object.IncreaseContrast(img, 100)  ##TODO BLAZE, SEE MY EXPLANATION
    ##TODO Remove later Testing Purpose Only.
    object.printImageForTestingPurpose('CONTRASTED IMAGE', contrastColorImg)

    ##Convert TO Black and White.
    bwImg = object.ConvertToBW(img)
    ##Convert TO Gray.
    grayImg = object.ConvertToGray(img)
    ##TODO Remove later Testing Purpose Only.
    object.printImageForTestingPurpose('GREY IMAGE', grayImg)

    columnList = object.FindSideToSideEdges(grayImg)
    # columnList[1] = edge1
    #  columnList[2] = edge2
    # sideToSidePixels = object.MeasurePixels(edge1, edge2)
    # coconutWidth = object.ConvertToLength(scale, sideToSidePixels)

    # rowList = FindTopToBottomEdges(bwImage)
    # rowList[1] = edge1
    # rowList[2] = edge2
    # topToBottomPixels = MeasurePixels(edge1, edge2)
    # coconutHeight = ConvertToLength(scale, topToBottomPixels)
