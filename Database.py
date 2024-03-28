#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders", "Vladyslav Haverdovskyi"]
__contact__    = "blazes@mfc.us"
__copyright__  = "Copyright 2023"
__license__    = "MIT License"
__status__     = "Development"
__deprecated__ = "False"
__version__    = "0.1.0"
"""

# Disable PyLint linting messages
# https://pypi.org/project/pylint/
# pylint: disable=line-too-long
# pylint: disable=invalid-name

## Standard Python libraries
import sqlite3                                  # SQlite Database
from datetime import datetime, time, timedelta 	# Manipulate calendar dates & time objects https://docs.python.org/3/library/datetime.html
from time import sleep                          # Pause program execution
import os                                       # Get filename information like directoty and file path
import csv                                      # Manipulate .CSV files for data reporting
import json                                     # Use to serialize a list of list and insert into TEXT column of SQLite database
from typing import Optional                     # TODO Give function argument an optional

## 3rd party libraries
import pytz 					                # World Timezone Definitions  https://pypi.org/project/pytz/
from pytz import timezone                       # Sync data write time to database no matter where server is located https://pypi.org/project/pytz
#TODO Turo SQLite to

## Internally developed code base
import GlobalConstants as GC


class Database:

    ONE_MOON_DAY = 28.5                         # TODO Exactly 28.5? Units are days
    ONE_MOON_ORBIT_AROUND_EARTH = ONE_MOON_DAY  # TODO Are they exactly the same?

    """ Store non-Personally Identifiable Information in a SQLite database
    """

    def __init__(self, filename: str = 'test.db'):
        """ Constructor to initialize an Database object
        """
        # Connect to the database (create if it doesn't exist)
        self.conn = sqlite3.connect(filename)
        self.cursor = self.conn.cursor()

        # Create ?TODO? tables in .db file for collecting Moon data
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS CraterTable       (id INTEGER PRIMARY KEY, humanCraterName TEXT, craterDiameterMeters REAL, latitude REAL, longitude REAL, timestamp TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DayGraphTable     (id INTEGER PRIMARY KEY, o2level INTEGER, co2level INTEGER, wattHours INTEGER, hourOfDayNumber INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS WeekGraphTable    (id INTEGER PRIMARY KEY, o2level INTEGER, co2level INTEGER, wattHours INTEGER, weekNumber INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS MonthGraphTable   (id INTEGER PRIMARY KEY, o2level INTEGER, co2level INTEGER, wattHours INTEGER, monthNumber TEXT)''')

        # Create debuging logg
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS DebugLoggingTable (id INTEGER PRIMARY KEY, logMessage TEXT)''')

        # Confifure graph database at .db file creation
        self.setup_graph_tables()

        # Commit the five tables to database
        self.conn.commit()


    def setup_graph_tables(self):
        """ Prepopulate DayGraphTable, WeekGraphTable, and MonthGraphTable with 24, 52 and 12 row for quicker db update vs db insert
            TODO IS AN UPDATE FASTER THEN AN INSERT IN SQLITE????

        """
        # Each day has 24 hours with 23 different values of 0100 to 2300
        for hourNumber in range(100, 2400, 100):
            self.insert_day_graph_table(0, 0, 0, hourNumber)

        # Each year has 52 weeks
        for weekNumber in range(1, 53):
            self.insert_week_graph_table(0, 0, 0, weekNumber)

        # Each year has 12 months
        for monthNumber in range(1, 13):
            self.insert_month_graph_table(0, 0, 0, monthNumber)


    #TODO UPDATE NEXT THREE FUNCTIONS WITH MATCH DB DEFINTATIONS
    def insert_day_graph_table(self, o2: int, co2: int, wH: int, hourOfDayNum: int):
        self.cursor.execute("INSERT INTO DayGraphTable(o2level, co2level, wattHours, hourOfDayNumber) VALUES (?, ?, ?, ?)", (o2, co2, wH, hourOfDayNum))
        self.commit_changes()


    def insert_week_graph_table(self, o2: int, co2: int, wH: int, weekNum: int):
        self.cursor.execute("INSERT INTO WeekGraphTable(o2level, co2level, wattHours, weekNumber) VALUES (?, ?, ?, ?)", (o2, co2, wH, weekNum))
        self.commit_changes()


    def insert_month_graph_table(self, o2: int, co2: int, wH: int, monthNum: int):
        self.cursor.execute("INSERT INTO MonthGraphTable(o2level, co2level, wattHours, monthNumber) VALUES (?, ?, ?, ?)", (o2, co2, wH, monthNum))
        self.commit_changes()


    def commit_changes(self):
        """ Commit data inserted into a table to the *.db database file
        """
        self.conn.commit()


    def close_database(self):
        """ Close database to enable another sqlite3 instance to query a *.db database
        """
        self.conn.close()


    def get_date_time(self) -> datetime:
        """ Get date and time in San Francisco timezone, independent of location of CPU in solar system

        Returns:
            Datetime:
        """
        tz = pytz.timezone('America/SanFrancico')
        zulu = pytz.timezone('UTC')                 # Zulu time is UTC +0
        now = datetime.now(tz)
        if now.dst() == timedelta(0):
            now = datetime.now(zulu) - timedelta(hours=8)
            if GC.DEBUG_STATEMENTS_ON: print('Standard Time')

        else:
            now = datetime.now(zulu) - timedelta(hours=7)
            if GC.DEBUG_STATEMENTS_ON: print('Daylight Savings')

        return now


    def insert_crater(self, latitude: float, longitude: float):
        pass


    def insert_daily_energy_table(self, energy: int, cost: float, date: str) -> int:
        """ Insert or update the DailyEnergyTable SQLite table with data Sense energy sensor collected

        Args:
            energy (int): Amount of energy used rounded to nearest interger (e.g 2.4 kWh)
            cost (float): Cost of the energy tracked in USD per kWh (e.g. $0.11/kWh)
            date (str): Timestamp in ISO8601 format for the date energy was used (e.g 2024-01-01)

        Returns:
            int: Database index id of last row inserted OR -1 if
        """
        timeStamp = str(datetime.strptime(date, '%Y-%m-%d').isoformat(timespec="minutes")[0:10])
        results, isEmpty, isValid = self.get_daily_sensor_data(timeStamp)
        if GC.DEBUG_STATEMENTS_ON: print(f"Tuple returned was: {(results, isEmpty, isValid)}")

        try:
            if(results):
                idPrimaryKeyToUpdate = results[0][2]
                self.cursor.execute("UPDATE DailyEnergyTable SET totalDailyWattHours = ?, currentCostPerWh = ?, timestamp = ? WHERE id = ?", (energy, cost, date, idPrimaryKeyToUpdate))
            else:
                self.cursor.execute("INSERT INTO DailyEnergyTable (totalDailyWattHours, currentCostPerWh, timestamp) VALUES (?, ?, ?)", (energy, cost, date))

        except TypeError:
            # self.cursor.execute("INSERT INTO DailyEnergyTable (totalDailyWattHours, currentCostPerWh, timestamp) VALUES (?, ?, ?)", (energy, cost, date))
            print("Error occured while inserting data...")

        lastDatabaseIndexInserted = self.cursor.lastrowid

        if lastDatabaseIndexInserted is not None:
            self.commit_changes()
        else:
            lastDatabaseIndexInserted = -1

        return lastDatabaseIndexInserted


    def insert_weekly_energy_table(self, energy: int, cost: float, date: str) -> int:
        """ Insert or update the WeeklyEnergyTable SQLite table with data Sense energy sensor collected

        Args:
            energy (int): Amount of energy used rounded to nearest interger (e.g 2.4 kWh)
            cost (float): Cost of the energy tracked in USD per kWh (e.g. $0.11/kWh)
            date (str): Timestamp in ISO8601 format for the date energy was used (e.g 2024-01-01)

        Returns:
            int: Database index id of last row inserted
        """
        timeStamp = str(datetime.strptime(date, '%Y-%m-%d').isoformat(timespec="minutes")[0:10])
        current_week_number = datetime.strptime(date, '%Y-%m-%d').isocalendar()[1]

        results, isEmpty, isValid = self.get_daily_sensor_data(timeStamp)
        if GC.DEBUG_STATEMENTS_ON: print(f"Tuple returned was: {(results, isEmpty, isValid)}")
        try:
            if(results):
                weekNumberToUpdate = results[0][1]
                self.cursor.execute("UPDATE WeeklyEnergyTable SET totalWeeklyWattHours = ?, currentCostPerWh = ?, weekNumber = ? WHERE weekNumber = ?", (energy, cost, current_week_number, weekNumberToUpdate))
            else:
                self.cursor.execute("INSERT INTO WeeklyEnergyTable (totalWeeklyWattHours, currentCostPerWh, weekNumber) VALUES (?, ?, ?)", (energy, cost, current_week_number))

        except TypeError:
            # self.cursor.execute("INSERT INTO DailyEnergyTable (totalDailyWattHours, currentCostPerWh, timestamp) VALUES (?, ?, ?)", (energy, cost, date))
            self.insert_debug_logging_table("Error occured while inserting data...")

        lastDatabaseIndexInserted = self.cursor.lastrowid
        if lastDatabaseIndexInserted is not None:
            self.commit_changes()
        else:
            lastDatabaseIndexInserted = -1

        return lastDatabaseIndexInserted


    def insert_debug_logging_table(self, debugText: str):
        """ Insert debugging text in database for later review

        Args:
            debugText (str): "ERROR: " or "WARNING:" + text message to log
        """
        self.cursor.execute("INSERT INTO DebugLoggingTable (logMessage) VALUES (?)", (debugText,))
        self.commit_changes()


    def get_daily_sensor_data(self, sensorId: int, date: str) -> tuple:
        """
        """
        return GC.TODO, GC.TODO, GC.TODO



    def get_weekly_sensor_data(self, sensorId: int, date: str):
        """
        """
        return GC.TODO


    def query_table(self, tableName: str, searchTerm: Optional[str] = None, row: Optional[int]= None, column: Optional[int]= None) -> tuple:
        """ Return every row of a table from a *.db database

        Args:
            tableName (String): Name of table in database to query
            row (Interger): Optional row from tuple to return
            column (Interger): Optional column from tuple to return

        Returns:
            result: A list of tuples from a table, where each row in table is a tuple of length n
            isEmpty: Returns True if table is empty, and False otherwise
            isValid: Returns True if table name exists in EnergyReport.db, and False otherwise
        """

        if searchTerm is None:
            sqlStatement = f"SELECT * FROM {tableName}"
        else:
            sqlStatement = f"SELECT * FROM {tableName} WHERE timestamp = ?"  #f"SELECT * FROM {tableName} WHERE content LIKE ?, ('%' + {str(searchTerm)} + '%',)" #self.cursor.execute("SELECT * FROM DatasetTable WHERE content LIKE ?", ('%' + str(searchTerm) + '%',))

        self.cursor.execute(sqlStatement, (searchTerm, ))

        isEmpty = False
        isValid = True
        result = self.cursor.fetchall()[0]

        if len(result) == 0:
            isEmpty = True

        if GC.DEBUG_STATEMENTS_ON: print(f"INSIDE QUERY TRY: {result}")

        try:
            if row == None and column == None:
                return result, isEmpty, isValid
            elif column == None:
                if row is not None:
                    return result[row-1], isEmpty, isValid
            else:
                if column == GC.TODO:
                     if row is not None:
                         return json.loads(result[row-1][column]), isEmpty, isValid
                else:
                     if row is not None:
                         return result[row-1][column], isEmpty, isValid

        except IndexError:
            if GC.DEBUG_STATEMENTS_ON: self.insert_debug_logging_table("INSIDE INDEX ERROR")
            return None, None, False

        except sqlite3.OperationalError:
            if GC.DEBUG_STATEMENTS_ON: self.insert_debug_logging_table(f"INSIDE OPERATIONAL ERROR")
            return None, None, False

        # Final code path
        return None, None, False


    def export_table_to_csv(self, tableNames: list):
        """ Creates a filename assuming that the date that this code runs is a Monday

        Args:
            tableNames (list): List of string table names in the database to convert
        """
        for table in tableNames:

            # Fetch data from the table
            data = self.query_table(table, None)

            if len(data) == 0:
                self.insert_debug_logging_table(f'No table named {table} when converting table to CSV in Database.export_table_to_csv() function at {self.get_date_time()}')

            else:
                # Create a .csv filename base on (Monday - 8 days) to (Monday - 2 days) to create for example 2023-08-01_2023-08-07_LaborerTimeReport
                lastSunday = (self.get_date_time() - timedelta(days=8)).isoformat(timespec="minutes")[0:10]
                lastSaturday = (self.get_date_time() - timedelta(days=2)).isoformat(timespec="minutes")[0:10]

                currentDirectory = os.getcwd()
                nextDirectory = os.path.join(currentDirectory, 'TimeCardReports')
                if not os.path.exists(nextDirectory):
                    os.makedirs(nextDirectory)

                if table == "WeeklyReportTable":
                    columnNames = ["Full Name", "Employee ID", "Total Hours", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Check In Comments", "Check Out Comments"]
                    outputFilename = lastSunday + "_" + lastSaturday  + "_LaborerTimeReport.csv"
                    filePath = os.path.join(nextDirectory, outputFilename)

                    with open(filePath, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow(columnNames[0:12])
                        for row in data:
                            csv_writer.writerow(row[1:])

                    csvfile.close()

                elif table == "CheckInTable":
                    columnNames = ["Full Name", "Employee ID", "Clock IN Timestamp"]
                    outputFilename = lastSunday + "_" + lastSaturday  + "_ClockInTimes.csv"
                    filePath = os.path.join(nextDirectory, outputFilename)

                    with open(filePath, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow(columnNames[0:4])
                        for row in data:
                            csv_writer.writerow(row[1:])

                    csvfile.close()

                elif table == "CheckOutTable":
                    columnNames = ["Full Name", "Employee ID", "Clock OUT Timestamp"]
                    outputFilename = lastSunday + "_" + lastSaturday  + "_ClockOutTimes.csv"
                    filePath = os.path.join(nextDirectory, outputFilename)

                    with open(filePath, 'w', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow(columnNames[0:4])
                        for row in data:
                            csv_writer.writerow(row[1:])

                    csvfile.close()

                else:
                    print(f'Table Name {table} conversion not implemented')


    def is_date_between(self, startDatetimeObj, endDatetimeObj, dateToCheck) -> bool:
        return startDatetimeObj <= dateToCheck <= endDatetimeObj


if __name__ == "__main__":
    print("Testing Database.py")

    db = Database('UnitTest.db')

    date = db.get_date_time()
    isoDateDay = date.isoformat()[0:10]
    #CraterTable (id INTEGER PRIMARY KEY, humanCraterName TEXT, craterDiameterMeters REAL, latitude REAL, longitude REAL, timestamp TEXT)

    oxygenLevel = 0             # Units are milliBar Plants have not started converting CO2 to O2
    carbonMonoxideLevel = 7     # Units are milliBar (Mars atomsphereic pressure is 7 milliBar on average
    powerDraw = 0               # Units are watt-Hours
    missionStartHour = 1600     # Units of 24-hour clock, so 4 pm
    db.insert_day_graph_table(oxygenLevel, carbonMonoxideLevel, powerDraw, missionStartHour)

    results = db.query_table("CraterTable", "Shackelton Crater")
    if GC.DEBUG_STATEMENTS_ON: print(results)

    primaryKey = 69
    results = db.query_table("CraterTable", str(primaryKey))
    if GC.DEBUG_STATEMENTS_ON: print(results)

    """
    db.export_table_to_csv(["DailyEnergyTable", "WeeklyEnergyTable", "MonthlyEnergyTable", "WeekGraphTable", "MonthGraphTable", "DebugLoggingTable"])

    insertErrors = db.insert_check_in_table(1001)
    print(insertErrors)
    checkOutErrors = db.insert_check_out_table(1001)
    print(insertErrors)
    """

    db.close_database()
