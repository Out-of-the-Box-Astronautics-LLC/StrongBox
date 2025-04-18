#!/usr/bin/python
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "info@strongbox.space"
__copyright__  = "Copyright 2024"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = "False"
__version__    = "0.0.1"
"""
# Engineering GUI dashboard to view 8 camera image feeds and develop Computer Vision pipeline

# Disable PyLint (VSCode) linting messages that seem unuseful
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name
# pylint: disable=global-statement
#
# Disable Pyright (Zed IDE) linting messages that seem unuseful
# https://pypi.org/project/pyright/
# https://github.com/microsoft/pyright/blob/main/docs/getting-started.md
# Using Command Line Interface (CLI): pyright GUI.py
# Update using "pip install --upgrade pyright" in CLI

## Standard Python libraries
import sys          	# Used to determine which OS (MacOS, Linux, or Windows) code is running on
from time import sleep	# Used to program pause execution
import os              # Used to check environment variables

## 3rd Party Libraries
# Browser base GUI framework to build and display a user interface mobile, PC, and Mac
# https://nicegui.io/
from nicegui import app, ui
from nicegui.events import MouseEventArguments

# Load environment variables for usernames, passwords, & API keys
# https://pypi.org/project/python-dotenv/
from dotenv import dotenv_values


## Internally developed modules
import GlobalConstants as GC    # Useful global constants used across multiple files
import Crater as cr             # Crater class to define name, size, and location of craters
import Database as db           # SQLite database to store crate locations
import Camera			# Image capture code using USB attached cameras

## Global Variables
# Application boots up in light mode
isDarkModeOn = False
darkMode  = ui.dark_mode()
ui.colors(primary=GC.STRONG_BOX_BLUE)

imageWidth = 720
frameRate = 30
textFontSize = 25


def set_background(color: str) -> None:
    ui.query('body').style(f'background-color: {color}')


def page_refresh(cameras):
    set_background(GC.STRONG_BOX_GREEN)
            
    cameraA0image.source = cameras[0].take_picture()
    sleep(0.010)
    cameraA90image.source = cameras[0].take_picture()
    sleep(0.010)
    cameraA180image.source = cameras[0].take_picture()
    sleep(0.010)
    cameraA270image.source = cameras[0].take_picture()

    print(f"Total number of images taken is {cameras[0].numOfPhotos}")

    cameraA0image.update()
    cameraA90image.update()
    cameraA180image.update()
    cameraA270image.update()


def check_headless_environment():
    # SBX-003: Detect and handle headless environment for GUI
    import sys, os
    if sys.platform.startswith('linux') and not os.environ.get('DISPLAY'):
        print("No display found. GUI cannot be launched in a headless environment.")
        sys.exit(1)


if __name__ in {"__main__", "__mp_main__"}:
    check_headless_environment()  # SBX-003: Call headless check at startup

    darkMode.disable()

    db1 = db.Database("strongbox-gui-db.db")

    cameras = []
    for i in range(GC.NUMBER_OF_CAMERAS):
        newCamera = Camera.Camera()
        cameras.append(newCamera)

    #ui.timer(GC.GUI_PAGE_REFRESH_RATE, lambda: set_background(GC.STRONG_BOX_GREEN))
    with ui.row().classes("self-center"):
        ui.button("PAGE REFRESH", on_click=lambda e: page_refresh(cameras))


    if __name__ == "__main__":
        # Outgoing API connection should only run once, on single port, in a single threaded main function
        # apiBackgroundProcessCode = start_api()
        pass

    # Incoming APIs URL's and keys
    try:
        config = dotenv_values()
        url = config['STRONG_BOX_GUI_DB_URL']
        key = config['STRONG_BOX_GUI_DB_TOKEN']

    except KeyError:
        db1.insert_debug_logging_table("ERROR: Could not find .ENV file when calling dotenv_values()")


    finally:
        pass


    if GC.DEBUG_STATEMENTS_ON: print(f"Font size was set to: {textFontSize}")

    with ui.footer(value=True) as footer:
        ui.label('Strong Box: Air Plant One Mission').style(f"font-size: 25px;")

    # Eight HD 720p (1280 × 720) or 4K UHD (3840 × 2160) cameras on the corners of the A & B sides of a Strong Box cube in two 3 x 3 grids (for MVP. Mission code with stitch into two circles)
    # A0 is the image on the A side of Strong Box hardware, displayed at 0 degrees (on compass which is North) on GUI
    # B270 os the image on the B side of Strong Box hardware, displayed at 270 degrees (on compass which is West) on GUI
    with ui.grid(columns=3).classes("self-center"):
        ui.label("").style(f"width: {imageWidth}px;")
        ui.label("").style(f"width: {imageWidth}px;")
        ui.label("").style(f"width: {imageWidth}px;")

        blankImageCellInGrid = ui.image('')
        cameraA0image = ui.image(GC.TEST_IMAGE_A)
        blankImageCellInGrid = ui.image('')

        cameraA270image = ui.image(GC.TEST_IMAGE_A)
        ui.label(f"SIDE A CAMERA'S: {frameRate} Hz").style(f"width: {imageWidth}px; font-size: {textFontSize}px; display: flex; justify-content: center; align-items: center;")
        cameraA90image = ui.image(GC.TEST_IMAGE_A)

        blankImageCellInGrid = ui.image('')
        cameraA180image = ui.image(GC.TEST_IMAGE_A)
        blankImageCellInGrid = ui.image('')

    with ui.grid(columns=3).classes("self-center"):
        ui.label("").style(f"width: {imageWidth}px;")
        ui.label("").style(f"width: {imageWidth}px;")
        ui.label("").style(f"width: {imageWidth}px;")

        blankImageCellInGrid = ui.image('')
        cameraB0image = ui.image(GC.TEST_IMAGE_B)
        blankImageCellInGrid = ui.image('')

        cameraB270image = ui.image(GC.TEST_IMAGE_B)
        ui.label(f"SIDE B CAMERA'S: {frameRate} Hz").style(f"width: {imageWidth}px; font-size: {textFontSize}px; display: flex; justify-content: center; align-items: center;")
        cameraB90image = ui.image(GC.TEST_IMAGE_B)

        blankImageCellInGrid = ui.image('')
        cameraB180image = ui.image(GC.TEST_IMAGE_B)
        blankImageCellInGrid = ui.image('')

    ui.run()
