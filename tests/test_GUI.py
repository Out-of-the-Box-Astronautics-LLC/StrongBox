import pytest
import io
import sys
import contextlib
import importlib
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Sample test skeleton for GUI.py

def test_gui_launch():
    # TODO: Replace with actual test
    assert True

def test_gui_headless_launch(monkeypatch):
    """Test that GUI.py handles headless environment gracefully."""
    # Simulate headless environment
    monkeypatch.delenv("DISPLAY", raising=False)
    import GUI
    # Capture output
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        try:
            GUI.check_headless_environment()
        except SystemExit as e:
            assert e.code == 1, "Expected SystemExit with code 1 in headless mode."
    output = f.getvalue()
    assert "No display found" in output, "Expected error message for headless environment."
