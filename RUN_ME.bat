@echo off
title Smart College Dashboard
color 0A

echo.
echo ================================================
echo     SMART COLLEGE DASHBOARD - COMPLETE SETUP
echo ================================================
echo.

:: Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo [1/5] Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo [1/5] Virtual environment already active
)

echo.
echo [2/5] Verifying packages...
python verify_installation.py

echo.
echo [3/5] Checking .env file...
if exist .env (
    echo ✅ .env file exists
) else (
    echo ❌ .env file missing!
    exit /b 1
)

echo.
echo [4/5] Creating MySQL database...
echo.
echo Running SQL script...
mysql -u root -pAgrawal@@3170 < create_database.sql
if errorlevel 1 (
    echo.
    echo ⚠️  Database creation failed!
    echo Please make sure MySQL is running: net start MySQL80
    echo.
    pause
    exit /b 1
)
echo ✅ Database created successfully!

echo.
echo [5/5] Starting application...
echo.
echo ================================================
echo     APPLICATION STARTING...
echo ================================================
echo.
echo 🌐 Open your browser: http://localhost:5000
echo.
echo 🔐 Login Credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo ⚠️  Press Ctrl+C to stop the server
echo.
echo ================================================
echo.

python app.py
