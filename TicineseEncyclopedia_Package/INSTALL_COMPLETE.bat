@echo off
setlocal enabledelayedexpansion
color 0A

:: Run as administrator check
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ===============================================
    echo   This installer needs administrator rights
    echo ===============================================
    echo.
    echo Please right-click this file and choose
    echo "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo ===============================================
echo   Ticinese Language Encyclopedia
echo   COMPLETE One-Click Installer
echo ===============================================
echo.
echo This will automatically:
echo  1. Check if Python is installed
echo  2. Install Python if needed (automatic)
echo  3. Create desktop shortcut
echo  4. Set everything up for you
echo.
echo Just sit back and relax!
echo.
pause

:: Get the current directory
set "INSTALL_DIR=%~dp0"
set "DESKTOP=%USERPROFILE%\Desktop"

echo.
echo [1/4] Checking for Python...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed! Great!
    goto :create_shortcut
)

echo Python is not installed. Installing now...
echo.

:: Download Python installer
echo [2/4] Downloading Python installer...
echo.

set "PYTHON_INSTALLER=%TEMP%\python-installer.exe"
set "PYTHON_URL=https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe"

:: Use PowerShell to download Python
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'}" 2>nul

if not exist "%PYTHON_INSTALLER%" (
    echo.
    echo ERROR: Could not download Python installer.
    echo.
    echo Please install Python manually from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Download complete!
echo.

:: Install Python silently
echo [3/4] Installing Python (this may take a few minutes)...
echo Please wait...
echo.

"%PYTHON_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

:: Wait for installation to complete
timeout /t 5 /nobreak >nul

:: Refresh PATH
call :RefreshPath

:: Verify Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Python installation may need a computer restart.
    echo Please restart your computer and run this installer again.
    echo.
    pause
    exit /b 1
)

echo Python installed successfully!
echo.

:: Clean up installer
del "%PYTHON_INSTALLER%" 2>nul

:create_shortcut
echo [4/4] Creating desktop shortcut...
echo.

:: Create the VBS script for shortcut
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
echo SUCCESS! Everything is ready!
echo.
echo A shortcut "Ticinese Encyclopedia" has been
echo created on your desktop.
echo.
echo TO USE:
echo   1. Double-click the desktop icon
echo   2. Your browser will open automatically
echo   3. Start exploring!
echo.
echo When finished, just close the browser window.
echo.
echo ===============================================
echo.
pause
exit /b 0

:RefreshPath
:: Refresh environment variables
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "UserPath=%%b"
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "SystemPath=%%b"
set "PATH=%UserPath%;%SystemPath%"
exit /b 0
