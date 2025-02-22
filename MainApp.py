#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders", "Vladyslav Haverdovskyi"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = False
__version__    = "0.0.1"
__doc__        = "Simple PWA to display the cost of the electrical power measured by the Sense Flex product"
"""
# https://caffeinedev.medium.com/building-and-installing-opencv-on-m1-macbook-c4654b10c188

# Disable PyLint linting messages that seem unuseful
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name
# pylint: disable=global-statement

## Standard Python libraries
import sys                                              # Determine which OS this code is running on https://docs.python.org/3/library/sys.html
from datetime import datetime, time, timedelta      	# Manipulate calendar dates & time objects https://docs.python.org/3/library/datetime.html
import pytz                                             # Sync data write time to database no matter where server is located https://pypi.org/project/pytz/
from pytz import timezone

## 3rd party libraries
# Browser based GUI framework to build and display a user interface on mobile, PC, and Mac
# https://nicegui.io/
from nicegui import app, ui                             # Define highest level app and UI elements
from nicegui.events import ValueChangeEventArguments    # Catch button, radio button, and other user actions

# Unofficial API for the Sense Energy Monitor
# https://github.com/scottbonline/sense
# TODO from sense_energy import Senseable                      # Used to connect to the Sense hardware in factory https://sense.com/sense-home-energy-monitor

# Load environment variables for usernames, passwords, & API keys
# https://pypi.org/project/python-dotenv/
from dotenv import dotenv_values                        # Used to login into Sense API

## Internally developed modules
import GlobalConstants as GC                            # Useful global constants used across multiple files
from Database import Database                           # Store non-Personally Identifiable Information in local (to server) SQlite database
import UserInterface                                    # Update the bar graph UI

## Global Variables
#TODO sense = Senseable()                         # Object to authenticate and collect realtime trends
instantPower = 0                            # Instant power (in Watts) being measured by the Sense device
dailyEnergyUsage = 0                        # Total energy (in kWh) measured by the Sense device so far (12:01 am to function call time)
currentGuiState = 0                         # State Machine number for the current GUI layout
dateSelected = None                         # Date selcted with left mouse click from the ui.date() calendar element
totalEnergy = 0                             # Units are kWh
selectedView = GC.RADIO_BUTTON_VALUES[0]    # State of radio buttons which defines how energy graph is displayed
#canUpdateweeklyReportTable = True          # TODO IF Dollar General needs .csv output


"""TODO If Dollar General needs .csv output instead of just website GUI they could screenshot for their bosses (replace ''' if uncommented)
def generate_report(db: Database):
    ''' Generate EXCEL document every monday at 3 am
        Work week starts Sunday at 12:01 am and repeats every 7 days
        Work week ends Saturday at 11:59 pm and repeats every 7 days
        Assumes 12 hour work day at 11 pm if an employee only clocks IN but forgets to clock out
        Back calculates 12 hour work day using the time an employee clocks OUT if no clocking IN exists

    Arg(s):
        db (sqlite): *.db database file
    '''

    currentDateObj = db.get_date_time()
    dayOfWeek = currentDateObj.weekday()
    currentTime = currentDateObj.time()

    if dayOfWeek == GC.MONDAY and (ELEVEN_PM < currentTime and currentTime < THREE_AM):
        canUpdateweeklyReportTable = True
        db.export_table_to_csv(["WeeklyReportTable", "CheckInTable", "CheckOutTable"])
"""

def search_button_click(db: Database, selectedView: GC):
    """ Toogle the visibility of GUI elements and draw a SVG bar grpah to create the graph page

    Arg(s):
        db (Database): SQlite database file containing all the logged (every GC.SENSE_UPDATE_TIME mintues) energy consumption datapoints
        selectedView (GlobalConstants): A value in the GC.RADIO_BUTTON_VALUES list used to determine which graph view to display
    """
    logo.visible = False
    calendarElement.visible = False
    graph.visible = True
    radioButtons.visible = True
    searchButton.visible = False
    closeGraphButton.visible = True
    totalCostLabel.visible = True
    graph.set_content(UserInterface.build_svg_graph(db, dateSelected, selectedView))
    totalCostLabel.set_text(f"The total cost for this {selectedView} is {round(GC.FACTORY_ENERGY_COST * UserInterface.total_kilowatthours_in_weekly_mode * GC.WORKING_LED_LIGHTS,2)} USD")


def close_graph_button_click():
    """ Toogle the visibility of GUI elements to create the home page
    """
    calendarElement.visible = True
    logo.visible = True
    graph.visible = False
    radioButtons.visible = False
    closeGraphButton.visible = False
    totalCostLabel.visible = False
    searchButton.visible = True


def get_radio_button_state(e: str):
    """ Determine which of the two radio buttons where selected and redraw the bar graph in a WEEKLY or MONTHLY view

    Arg(s):
        e (String): e.value variable created via the ValueChangeEventArguments Class
    """
    global selectedView, totalEnergy
    selectedView = e

    if selectedView == 'WEEK VIEW':
        totalEnergy = UserInterface.total_kilowatthours_in_weekly_mode
        totalCostLabel.set_text(f"The total cost for this {selectedView} is {round(GC.FACTORY_ENERGY_COST * totalEnergy * GC.WORKING_LED_LIGHTS, 2)} USD")
    else:
        totalEnergy = UserInterface.total_kilowatthours_in_monthly_mode
        totalCostLabel.set_text(f"The total cost for this {selectedView} is {round(GC.FACTORY_ENERGY_COST * totalEnergy * GC.WORKING_LED_LIGHTS, 2)} USD")

    graph.set_content(UserInterface.build_svg_graph(db, dateSelected, selectedView))


def get_date_selected(e: str):
    """ Store date clicked on the calendar element by the user into a global variable

    Arg(s):
        e (String): e.value variable created via the ValueChangeEventArguments Class
    """
    global dateSelected
    dateSelected = e
    if (GC.DEBUG_STATEMENTS_ON): print(f"DateSelected variable was updated: {dateSelected}")


def sense_updating(db: Database, mode: str):
    global instantPower
    global dailyEnergyUsage

    sense.update_realtime()
    sense.update_trend_data()
    instantPower = sense.active_power
    dailyEnergyUsage = sense.daily_usage
    weeklyEnergyUsage = sense.weekly_usage
    monthlyEnergyUsage = sense.monthly_usage
    yearlyEnergyUsage = sense.yearly_usage
    timeZone = sense.time_zone

    current_date = datetime.now(timezone('CST6CDT'))
    currentDate0 = current_date.strftime("%Y-%m-%d")
    year, month, day = current_date.year, current_date.month, current_date.day
    currentDate = str(year) + '-' + str(month) + '-' + str(day)

    if GC.DEBUG_STATEMENTS_ON:
        print (f"{mode} Active: {instantPower} W")
        print (f"{mode} Daily:  {dailyEnergyUsage} kWh")
        print (f"{mode} Weekly:  {weeklyEnergyUsage} kWh")
        print (f"{mode} Monthly:  {monthlyEnergyUsage} kWh")
        print (f"{mode} Yearly:  {yearlyEnergyUsage} kWh")
        print ("Active Devices:",", ".join(sense.active_devices))

    db.insert_daily_energy_table(dailyEnergyUsage*1000, GC.FACTORY_ENERGY_COST, currentDate) 
    db.insert_weekly_energy_table(weeklyEnergyUsage*1000, GC.FACTORY_ENERGY_COST, currentDate0)

# TODO Switch to using routers for real Single Page App instead of visibility changes in UI elements https://github.com/zauberzeug/nicegui/blob/main/examples/single_page_app/main.py
if __name__ in {"__main__", "__mp_main__"}:
    # Force application to run in light mode since calendar color is bad in dark mode
    darkMode = ui.dark_mode()
    darkMode.disable()

    ui.colors(primary=GC.DOLLAR_STORE_LOGO_BLUE)

    # Create directory and URI for local storage of images
    if sys.platform.startswith('darwin'):
        app.add_static_files('/static/images', GC.MAC_CODE_DIRECTORY +'/static/images')
        app.add_static_files('/static/videos', GC.MAC_CODE_DIRECTORY + '/static/videos')
    elif sys.platform.startswith('linux'):
        try: #PRIMARY DEBIAN LINODE SERVER
            print("Trying to deploy code to the 'Sense-Energy-Gauge-Optimizer-Track Debian based Linode server")
            app.add_static_files('/static/images', '/root' + GC.LINUX_CODE_DIRECTORY + '/static/images')
            app.add_static_files('/static/videos', '/root' + GC.LINUX_CODE_DIRECTORY + '/static/videos')
        except RuntimeError: # BACKUP MFC JUPITER SERVER RUNNING UBUNTU
            print("Linode Debian server failed deploying to MFC Jupiter server as hot backup")

            app.add_static_files('/static/images', '/home/jupiter/Apps' + GC.LINUX_CODE_DIRECTORY + '/static/images')
            app.add_static_files('/static/videos', '/home/jupiter/Apps' + GC.LINUX_CODE_DIRECTORY + '/static/videos')

    elif sys.platform.startswith('win'):
        print("WARNING: Running Main.py server code on Windows OS is NOT fully supported")
        app.add_static_files('/static/images', GC.WINDOWS_CODE_DIRECTORY + '/static/images')
        app.add_static_files('/static/videos', GC.WINDOWS_CODE_DIRECTORY + '/static/videos')
    else:
        print("ERROR: Running on an unknown operating system")
        quit()

    db = Database()

    config = dotenv_values()
    username = config['SENSE_USERNAME']
    password = config['SENSE_PASSWORD']
    sense.authenticate(username, password)

    if GC.DEBUG_STATEMENTS_ON: ui.timer(60, lambda: sense_updating(db, 'DEV'))           # Call every 60 seconds to speed up testing
    ui.timer(GC.SENSE_UPDATE_TIME, lambda: sense_updating(db, 'PROD'))                   # Limit to once every 20 mins to not hit API limits

    logo = ui.image('static/images/DollarGeneralEnergyLogo.png').classes('w-96 m-auto')

    graph = ui.html().classes("self-center")
    graph.visible = False

    calendarElement = ui.date(value=Database.get_date_time(db), on_change=lambda e: get_date_selected(e.value)).classes('m-auto').style("color: #001b36")
    calendarElement.visible = True

    # Invisible character https://invisibletext.com/#google_vignette
    with ui.row().classes("self-center"):
        searchButton = ui.button(on_click=lambda e: search_button_click(db, selectedView), \
                                 color=GC.DOLLAR_STORE_LOGO_GREEN).classes("relative  h-24 w-64")
        with searchButton:
            searchButton.visible = True
            ui.label('SEARCH ㅤ').style('font-size: 100%; font-weight: 300')
            ui.icon('search')

    with ui.row().classes("self-center"):
        radioButtons = ui.radio(GC.RADIO_BUTTON_VALUES, value=GC.RADIO_BUTTON_VALUES[0], \
                                on_change=lambda e: get_radio_button_state(e.value)).props('inline')
        with radioButtons:
            radioButtons.visible = False

    # Invisible character https://invisibletext.com/#google_vignette
    with ui.row().classes("self-center"):
        closeGraphButton = ui.button(on_click=lambda e: close_graph_button_click(), color="red").classes("relative  h-24 w-32")
        with closeGraphButton:
            closeGraphButton.visible = False
            ui.label('CLOSE ㅤ').style('font-size: 100%; font-weight: 300')
            ui.icon('close')


    totalCostLabel = ui.label(f"The total cost for this {selectedView} is {GC.FACTORY_ENERGY_COST * totalEnergy * GC.WORKING_LED_LIGHTS} USD").style("color: #001b36; font-size: 300%; font-weight: 300").classes("self-center")
    totalCostLabel.visible = False

    ui.run(native=GC.RUN_ON_NATIVE_OS, port=GC.LOCAL_HOST_PORT_FOR_GUI)
