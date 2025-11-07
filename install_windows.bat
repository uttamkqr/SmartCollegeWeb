@echo off
echo ========================================
echo Smart College Dashboard - Installation
echo ========================================
echo.

:: Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo [INFO] Virtual environment not detected.
    echo [INFO] Activating .venv...
    if exist .venv\Scripts\activate.bat (
        call .venv\Scripts\activate.bat
    ) else (
        echo [ERROR] Virtual environment not found!
        echo [INFO] Creating virtual environment...
        python -m venv .venv
        call .venv\Scripts\activate.bat
    )
)

echo.
echo [STEP 1/4] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [STEP 2/4] Installing dependencies (this may take a few minutes)...
echo [INFO] Installing packages with pre-built wheels for Windows...

:: Install packages one by one to better handle errors
python -m pip install Flask==3.0.0
python -m pip install Werkzeug==3.0.1
python -m pip install numpy==1.24.3
python -m pip install opencv-contrib-python==4.8.1.78
python -m pip install mysql-connector-python==8.2.0
python -m pip install Pillow==10.2.0
python -m pip install qrcode[pil]==7.4.2
python -m pip install python-dotenv==1.0.0

echo.
echo [STEP 3/4] Creating project directories...
if not exist student_images mkdir student_images
if not exist recognizer mkdir recognizer
if not exist attendance_reports mkdir attendance_reports
if not exist static\css mkdir static\css
if not exist static\js mkdir static\js
if not exist static\images mkdir static\images

echo.
echo [STEP 4/4] Setting up environment file...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo [INFO] .env file created from template
        echo [WARN] Please edit .env file with your database credentials!
    ) else (
        echo [WARN] .env.example not found. Creating basic .env...
        (
            echo # Database Configuration
            echo DB_HOST=localhost
            echo DB_USER=root
            echo DB_PASSWORD=your_password_here
            echo DB_NAME=smart_attendance
            echo.
            echo # Email Configuration (optional)
            echo EMAIL_USER=your_email@gmail.com
            echo EMAIL_PASS=your_app_password
            echo.
            echo # Flask Configuration
            echo SECRET_KEY=your-secret-key-change-me
            echo FLASK_ENV=development
            echo FLASK_DEBUG=1
        ) > .env
        echo [INFO] Basic .env file created
    )
) else (
    echo [INFO] .env file already exists
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Edit .env file with your database credentials
echo 2. Create MySQL database: CREATE DATABASE smart_attendance;
echo 3. Run: python app.py
echo 4. Open browser: http://localhost:5000
echo 5. Login: admin / admin123
echo.
echo For troubleshooting, see README.md
echo ========================================
echo.
pause
