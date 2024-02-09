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


# Global Variables
isDarkModeOn = False            # Application boots up in light mode
darkMode = ui.dark_mode()


if __name__ in {"__main__", "__mp_main__"}:
    darkMode.disable()

    db1 = db.Database("GUI.db")

    if __name__ == "__main__":
        # Outgoing API connection should only run once, on single port, in a single threaded main function
        # apiBackgroundProcessCode = start_api()
        pass

    # Incoming APIs
    try:
        config = dotenv_values()

    except KeyError:
        db.insert_error_logging_table(GC.TODO, "ERROR: Could not find .ENV file")

    finally:
        url = config['TURSO_URL']
        key = config['TURSO_KEY']
