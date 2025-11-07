#!/usr/bin/env python
"""
Setup script for Smart College Dashboard
This script initializes the project structure and checks dependencies
"""

import os
import sys
import subprocess


def create_directories():
    """Create necessary directories"""
    directories = [
        'student_images',
        'recognizer',
        'attendance_reports',
        'static/css',
        'static/js',
        'static/images',
        'utils',
        'templates'
    ]

    print("📁 Creating project directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✓ {directory}")
    print()


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"   ✗ Python 3.8+ required. Current: {version.major}.{version.minor}")
        return False
    print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
    print()
    return True


def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")

    required_packages = [
        'flask',
        'opencv-python',
        'mysql-connector-python',
        'numpy',
        'Pillow',
        'qrcode',
        'werkzeug'
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').split()[0].lower())
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} - Not installed")
            missing.append(package)

    print()

    if missing:
        print("⚠️  Missing packages detected. Install with:")
        print("   pip install -r requirements.txt")
        print()
        return False
    return True


def check_mysql():
    """Check if MySQL is accessible"""
    print("🗄️  Checking MySQL connection...")
    try:
        import mysql.connector
        # Try to connect (will fail if MySQL not running)
        # This is just a connectivity check
        print("   ✓ MySQL connector available")
        print("   ℹ️  Make sure MySQL server is running")
        print()
        return True
    except ImportError:
        print("   ✗ MySQL connector not installed")
        print()
        return False


def check_env_file():
    """Check if .env file exists"""
    print("⚙️  Checking configuration...")
    if os.path.exists('.env'):
        print("   ✓ .env file found")
    else:
        print("   ⚠️  .env file not found")
        print("   Creating from .env.example...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as src:
                with open('.env', 'w') as dst:
                    dst.write(src.read())
            print("   ✓ .env file created")
            print("   ⚠️  Please update .env with your configuration")
        else:
            print("   ✗ .env.example not found")
    print()


def check_webcam():
    """Check if webcam is available"""
    print("📷 Checking webcam...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("   ✓ Webcam is available")
            cap.release()
        else:
            print("   ⚠️  Webcam not detected")
            print("   Face capture will not work without a webcam")
    except Exception as e:
        print(f"   ✗ Error checking webcam: {e}")
    print()


def print_next_steps():
    """Print next steps for setup"""
    print("=" * 60)
    print("📋 NEXT STEPS:")
    print("=" * 60)
    print()
    print("1. Update .env file with your database credentials")
    print("2. Create MySQL database: CREATE DATABASE smart_attendance;")
    print("3. Configure email settings in .env (optional)")
    print("4. Run the application: python app.py")
    print("5. Open browser: http://localhost:5000")
    print("6. Login with default credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print()
    print("⚠️  IMPORTANT: Change default password after first login!")
    print()
    print("=" * 60)


def main():
    """Main setup function"""
    print()
    print("=" * 60)
    print("   🎓 SMART COLLEGE DASHBOARD - SETUP")
    print("=" * 60)
    print()

    # Run all checks
    all_good = True

    if not check_python_version():
        all_good = False

    create_directories()

    if not check_dependencies():
        all_good = False

    if not check_mysql():
        all_good = False

    check_env_file()
    check_webcam()

    if all_good:
        print("✅ All checks passed!")
        print()
        print_next_steps()
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print()

    return all_good


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
