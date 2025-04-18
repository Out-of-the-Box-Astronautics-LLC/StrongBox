# Problems and Issues Log for StrongBox

# Format for each entry:
# - ID: Unique identifier
# - Title: Short description
# - Severity: (Critical/Major/Minor)
# - Affected Modules: List of files
# - Steps to Reproduce: Detailed steps
# - Expected Behavior: What should happen
# - Actual Behavior: What happens now
# - Logs/Tracebacks: Relevant output
# - Status: Open/Fixed/Closed
# - Test Reference: Related test file/function

---

# Example Entry
- ID: SBX-001
- Title: Camera initialization fails on startup
- Severity: Major
- Affected Modules: Camera.py
- Steps to Reproduce:
    1. Run MainApp.py
    2. Observe error on camera initialization
- Expected Behavior: Camera initializes without error
- Actual Behavior: Exception thrown, camera not detected
- Logs/Tracebacks: [Paste relevant log from DebugLog.txt]
- Status: Open
- Test Reference: tests/test_Camera.py::test_camera_initialization

# Add new problems below using the above format.

- ID: SBX-002
- Title: Database connection fails if database file is missing
- Severity: Major
- Affected Modules: Database.py
- Steps to Reproduce:
    1. Delete or rename the database file used by Database.py
    2. Run MainApp.py
    3. Observe error on database connection
- Expected Behavior: Application should handle missing database file gracefully and provide a clear error message
- Actual Behavior: Unhandled exception is thrown
- Logs/Tracebacks: [Add traceback if available]
- Status: Open
- Test Reference: tests/test_Database.py::test_database_missing_file

- ID: SBX-003
- Title: GUI fails to launch on headless systems
- Severity: Major
- Affected Modules: GUI.py
- Steps to Reproduce:
    1. Run MainApp.py on a headless Linux server (no display)
    2. Observe error on GUI launch
- Expected Behavior: Application should detect headless environment and provide a fallback or error message
- Actual Behavior: Application crashes with display error
- Logs/Tracebacks: [Add traceback if available]
- Status: Open
- Test Reference: tests/test_GUI.py::test_gui_headless_launch

- ID: SBX-004
- Title: Camera initialization throws exception if no camera is connected
- Severity: Major
- Affected Modules: Camera.py
- Steps to Reproduce:
    1. Disconnect all cameras
    2. Run MainApp.py
    3. Observe error on camera initialization
- Expected Behavior: Application should handle missing camera gracefully
- Actual Behavior: Unhandled exception is thrown
- Logs/Tracebacks: [Add traceback if available]
- Status: Open
- Test Reference: tests/test_Camera.py::test_camera_no_device
