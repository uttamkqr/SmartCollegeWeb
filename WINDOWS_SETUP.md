# 🪟 Windows Setup Guide

Complete guide for setting up Smart College Dashboard on Windows.

## 🚀 Quick Installation

### Method 1: Automated Installation (Recommended)

1. **Double-click** `install_windows.bat`
2. Wait for installation to complete
3. Edit `.env` file with your database credentials
4. Double-click `start.bat` to run the application

### Method 2: Manual Installation

```powershell
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
copy .env.example .env

# 6. Edit .env with notepad
notepad .env

# 7. Run application
python app.py
```

## 📋 Prerequisites

### 1. Python Installation

- **Version Required:** Python 3.8 or higher
- **Download:** https://www.python.org/downloads/
- **During installation:** ✅ Check "Add Python to PATH"

**Verify installation:**

```powershell
python --version
```

### 2. MySQL Installation

- **Download:** https://dev.mysql.com/downloads/installer/
- **Choose:** MySQL Installer for Windows
- **During installation:**
    - Install MySQL Server
    - Remember your root password!
    - Start MySQL service

**Verify installation:**

```powershell
mysql --version
```

### 3. Microsoft Visual C++ (for OpenCV)

- **Download:** https://aka.ms/vs/17/release/vc_redist.x64.exe
- **Install** Visual C++ Redistributable
- **Required for:** OpenCV to work properly

### 4. Webcam

- Built-in laptop camera OR USB webcam
- Make sure it's not being used by other applications

## 🔧 Installation Steps

### Step 1: Download Project

```powershell
# Clone or download the project
cd D:\SmartCollegeWeb
```

### Step 2: Install Dependencies

**Option A: Use automated script**

```powershell
.\install_windows.bat
```

**Option B: Manual installation**

```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Setup Database

**Open MySQL Command Line:**

```sql
-- Login with your password
mysql -u root -p

-- Create database
CREATE DATABASE smart_attendance;

-- Verify
SHOW DATABASES;

-- Exit
EXIT;
```

### Step 4: Configure Environment

**Edit `.env` file:**

```powershell
notepad .env
```

**Minimum configuration:**

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=smart_attendance
```

### Step 5: Run Application

**Option A: Use start script**

```powershell
.\start.bat
```

**Option B: Manual start**

```powershell
# Activate virtual environment
.venv\Scripts\activate

# Run app
python app.py
```

**Access at:** http://localhost:5000

## 🐛 Troubleshooting

### Problem 1: NumPy Installation Fails

**Error:** `NumPy requires GCC >= 8.4`

**Solution:**

```powershell
# Install pre-built wheel instead
pip install numpy==1.24.3
```

### Problem 2: OpenCV Import Error

**Error:** `ImportError: DLL load failed`

**Solutions:**

1. **Install Visual C++ Redistributable:**
    - Download: https://aka.ms/vs/17/release/vc_redist.x64.exe
    - Install and restart computer

2. **Use different OpenCV version:**
   ```powershell
   pip uninstall opencv-contrib-python
   pip install opencv-contrib-python==4.8.1.78
   ```

### Problem 3: MySQL Connection Failed

**Error:** `Can't connect to MySQL server`

**Solutions:**

1. **Check MySQL is running:**
   ```powershell
   # Start MySQL service
   net start MySQL80
   ```

2. **Verify credentials in .env:**
   ```powershell
   notepad .env
   ```

3. **Test connection:**
   ```powershell
   mysql -u root -p
   ```

### Problem 4: Port 5000 Already in Use

**Error:** `Address already in use`

**Solutions:**

1. **Find process using port:**
   ```powershell
   netstat -ano | findstr :5000
   ```

2. **Kill the process:**
   ```powershell
   taskkill /PID <process_id> /F
   ```

3. **Or change port in app.py:**
   ```python
   # Last line in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Problem 5: Virtual Environment Activation Failed

**Error:** `cannot be loaded because running scripts is disabled`

**Solution:**

```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
.venv\Scripts\activate
```

### Problem 6: Webcam Not Working

**Solutions:**

1. **Check camera permissions:**
    - Settings → Privacy → Camera
    - Allow desktop apps to access camera

2. **Close other apps using camera:**
    - Skype, Teams, Discord, etc.

3. **Test webcam:**
   ```powershell
   python -c "import cv2; print('Webcam:', cv2.VideoCapture(0).isOpened())"
   ```

### Problem 7: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**

```powershell
# Make sure virtual environment is activated
.venv\Scripts\activate

# Reinstall packages
pip install -r requirements.txt
```

### Problem 8: Permission Denied Errors

**Solution:**

```powershell
# Run command prompt as Administrator
# Right-click → Run as administrator
```

## 📦 Package Installation Issues

If installation fails, try installing packages one by one:

```powershell
# Activate virtual environment
.venv\Scripts\activate

# Install core packages first
pip install Flask==3.0.0
pip install Werkzeug==3.0.1
pip install python-dotenv==1.0.0

# Install numpy (may take time)
pip install numpy==1.24.3

# Install OpenCV
pip install opencv-contrib-python==4.8.1.78

# Install remaining packages
pip install mysql-connector-python==8.2.0
pip install Pillow==10.2.0
pip install qrcode[pil]==7.4.2
```

## 🔍 Verification Commands

**Check Python:**

```powershell
python --version
# Should show 3.8 or higher
```

**Check pip:**

```powershell
pip --version
```

**Check MySQL:**

```powershell
mysql --version
```

**Check installed packages:**

```powershell
pip list
```

**Test imports:**

```powershell
python -c "import flask; print('Flask:', flask.__version__)"
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import numpy; print('NumPy:', numpy.__version__)"
```

## 📁 Directory Structure Check

Make sure these directories exist:

```
D:\SmartCollegeWeb\
├── .venv\              (virtual environment)
├── student_images\     (student photos)
├── recognizer\         (trained models)
├── attendance_reports\ (CSV exports)
├── templates\          (HTML files)
├── static\             (CSS, JS, images)
└── utils\              (utility modules)
```

## 🔐 Database Setup Script

Save as `setup_database.sql`:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS smart_attendance;
USE smart_attendance;

-- Show created database
SHOW DATABASES;

-- Show tables (after running app first time)
SHOW TABLES;
```

**Run it:**

```powershell
mysql -u root -p < setup_database.sql
```

## 🚀 Starting the Application

### Using Batch Scripts (Easy)

**Install:**

```powershell
.\install_windows.bat
```

**Start:**

```powershell
.\start.bat
```

### Manual Method

```powershell
# 1. Activate virtual environment
.venv\Scripts\activate

# 2. Check .env file exists
if not exist .env copy .env.example .env

# 3. Run application
python app.py
```

### Verify It's Running

1. Open browser
2. Go to: http://localhost:5000
3. You should see login page
4. Login with:
    - Username: `admin`
    - Password: `admin123`

## 📧 Email Configuration (Optional)

For Gmail:

1. **Enable 2-Factor Authentication**
    - https://myaccount.google.com/security

2. **Generate App Password**
    - https://myaccount.google.com/apppasswords
    - Select "Mail" and "Windows Computer"
    - Copy generated password

3. **Update .env:**
   ```env
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=generated_16_char_password
   ```

## 🎯 Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL installed and running
- [ ] Visual C++ Redistributable installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database created
- [ ] .env file configured
- [ ] Application starts without errors
- [ ] Can access http://localhost:5000
- [ ] Can login with admin/admin123

## 💡 Tips

1. **Always activate virtual environment** before running commands
2. **Keep MySQL running** when using the app
3. **Use recommended package versions** for compatibility
4. **Check firewall** if can't access localhost:5000
5. **Update pip** regularly: `python -m pip install --upgrade pip`

## 🆘 Still Having Issues?

1. **Check the logs:**
   ```powershell
   type app.log
   ```

2. **Run setup verification:**
   ```powershell
   python setup.py
   ```

3. **Check Python path:**
   ```powershell
   where python
   ```

4. **Reinstall everything:**
   ```powershell
   # Remove virtual environment
   rmdir /s .venv
   
   # Start fresh
   .\install_windows.bat
   ```

## 📞 Support

- **Documentation:** See README.md
- **Quick Start:** See QUICKSTART.md
- **Changelog:** See CHANGELOG.md

---

**Good luck! 🎉**
