# StrongBox Project Environment Setup

## 1. System Requirements
- OS: Linux (recommended)
- Python: 3.12.x (see venv_test/ for reference)

## 2. Virtual Environment Setup
```
python3.12 -m venv venv_test
source venv_test/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Running Tests
```
pip install pytest
pytest tests/
```

## 4. Optional: Code Quality Tools
```
pip install flake8 pylint coverage
flake8 .
pylint Camera.py ComputerVision.py Crater.py Database.py Debug.py GUI.py GlobalConstants.py KinematicEquations.py MainApp.py MoonAutoPilot.py Power.py strongbox.py UserInterface.py
coverage run -m pytest
coverage report -m
```

## 5. Optional: Docker Usage
See Dockerfile for containerized setup.

## 6. Notes
- Update requirements.txt as dependencies change.
- Document any environment variables or secrets needed for production.
