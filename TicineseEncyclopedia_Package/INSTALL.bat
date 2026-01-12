@echo off
setlocal enabledelayedexpansion
color 0A

echo ===============================================
echo   Ticinese Language Encyclopedia
echo   Installer for Grandma
echo ===============================================
echo.
echo This will install the Ticinese Encyclopedia
echo and create a desktop shortcut.
echo.
pause

:: Get the current directory where this batch file is located
set "INSTALL_DIR=%~dp0"
set "DESKTOP=%USERPROFILE%\Desktop"

echo.
echo Installing to: %INSTALL_DIR%
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Python is not installed on this computer.
    echo.
    echo The encyclopedia needs Python to run.
    echo Please download Python from: https://www.python.org/downloads/
    echo.
    echo During installation, make sure to check:
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo Python is installed! Good.
echo.

:: Create the desktop shortcut
echo Creating desktop shortcut...

:: Create a VBS script to create the shortcut
set "VBS_FILE=%TEMP%\CreateShortcut.vbs"
(
echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
echo sLinkFile = "%DESKTOP%\Ticinese Encyclopedia.lnk"
echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
echo oLink.TargetPath = "pythonw.exe"
echo oLink.Arguments = """%INSTALL_DIR%launch_encyclopedia.py"""
echo oLink.WorkingDirectory = "%INSTALL_DIR%"
echo oLink.Description = "Ticinese Language Encyclopedia - Swiss-Italian Heritage"
echo oLink.IconLocation = "C:\Windows\System32\shell32.dll,13"
echo oLink.Save
) > "%VBS_FILE%"

:: Run the VBS script
cscript //nologo "%VBS_FILE%"
del "%VBS_FILE%"

echo.
echo ===============================================
echo   Installation Complete!
echo ===============================================
echo.
echo A shortcut has been created on your desktop.
echo.
echo To use the encyclopedia:
echo   1. Double-click "Ticinese Encyclopedia" on your desktop
echo   2. Your web browser will open automatically
echo   3. Enjoy exploring the Ticinese language!
echo.
echo When you're done, simply close the browser window.
echo.
pause
