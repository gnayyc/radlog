@echo off
REM RadLog Windows Build Script

echo Installing dependencies...
pip install -r requirements.txt

echo Building executable...
pyinstaller --onefile --windowed --name RadLog --icon=icon.ico radlog.py

echo Done! Executable at: dist\RadLog.exe
pause
