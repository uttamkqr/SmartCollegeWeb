#!/usr/bin/env python
"""
Verification script for Smart College Dashboard
"""

print("=" * 60)
print("🔍 VERIFYING INSTALLATION")
print("=" * 60)
print()

# Test imports
packages = {
    'Flask': 'flask',
    'Werkzeug': 'werkzeug',
    'OpenCV': 'cv2',
    'NumPy': 'numpy',
    'Pillow': 'PIL',
    'MySQL Connector': 'mysql.connector',
    'QRCode': 'qrcode',
    'Python-dotenv': 'dotenv'
}

all_good = True

for name, module in packages.items():
    try:
        mod = __import__(module)
        version = getattr(mod, '__version__', 'installed')
        print(f"✅ {name:20} - {version}")
    except ImportError as e:
        print(f"❌ {name:20} - NOT INSTALLED")
        all_good = False

print()
print("=" * 60)

if all_good:
    print("✅ ALL PACKAGES INSTALLED SUCCESSFULLY!")
    print()
    print("NEXT STEPS:")
    print("1. Create MySQL database: CREATE DATABASE smart_attendance;")
    print("2. Create .env file with your database credentials")
    print("3. Run: python app.py")
    print("4. Open: http://localhost:5000")
else:
    print("⚠️  SOME PACKAGES ARE MISSING!")
    print("Please install missing packages")

print("=" * 60)
