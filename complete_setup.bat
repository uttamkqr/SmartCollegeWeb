@echo off
echo ========================================
echo Smart College Dashboard - Complete Setup
echo ========================================
echo.

:: Step 1: Verify Installation
echo [STEP 1/3] Verifying installed packages...
python verify_installation.py
if errorlevel 1 (
    echo.
    echo [ERROR] Some packages are missing!
    pause
    exit /b 1
)

echo.
echo ========================================
echo.

:: Step 2: Create .env file
echo [STEP 2/3] Creating .env file...
if exist .env (
    echo [INFO] .env file already exists
    echo [WARN] Please verify your settings
) else (
    echo [INFO] Creating .env file...
    (
        echo # Database Configuration
        echo DB_HOST=localhost
        echo DB_USER=root
        echo DB_PASSWORD=Agrawal@@3170
        echo DB_NAME=smart_attendance
        echo.
        echo # Email Configuration ^(optional^)
        echo EMAIL_USER=
        echo EMAIL_PASS=
        echo.
        echo # Flask Configuration
        echo SECRET_KEY=your-secret-key-change-me
        echo FLASK_ENV=development
        echo FLASK_DEBUG=1
    ) > .env
    echo [SUCCESS] .env file created!
)

echo.
echo ========================================
echo.

:: Step 3: MySQL Database Setup
echo [STEP 3/3] Database Setup
echo.
echo Please create MySQL database manually:
echo.
echo Commands to run in MySQL:
echo   mysql -u root -p
echo   CREATE DATABASE smart_attendance;
echo   SHOW DATABASES;
echo   EXIT;
echo.
echo Press any key after creating database...
pause > nul

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo TO START THE APPLICATION:
echo   1. Make sure MySQL is running
echo   2. Run: python app.py
echo   3. Open: http://localhost:5000
echo   4. Login: admin / admin123
echo.
echo ========================================
pause
