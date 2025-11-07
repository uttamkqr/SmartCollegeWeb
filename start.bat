@echo off
echo ========================================
echo Smart College Dashboard
echo ========================================
echo.

:: Check if virtual environment exists
if not exist .venv\Scripts\activate.bat (
    echo [ERROR] Virtual environment not found!
    echo [INFO] Please run install_windows.bat first
    pause
    exit /b 1
)

:: Activate virtual environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat

:: Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [ERROR] Flask not installed!
    echo [INFO] Please run install_windows.bat first
    pause
    exit /b 1
)

:: Check if .env exists
if not exist .env (
    echo [WARN] .env file not found!
    echo [INFO] Creating from template...
    if exist .env.example (
        copy .env.example .env
        echo [INFO] Please edit .env with your database credentials
        notepad .env
    )
)

echo.
echo [INFO] Starting Smart College Dashboard...
echo [INFO] Press Ctrl+C to stop the server
echo.
echo Application will be available at:
echo http://localhost:5000
echo.
echo Default Login:
echo Username: admin
echo Password: admin123
echo.
echo ========================================
echo.

:: Start the application
python app.py
