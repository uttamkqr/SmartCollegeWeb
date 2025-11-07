# 🚀 Quick Start Guide

Get Smart College Dashboard up and running in 5 minutes!

## Prerequisites Check

- ✅ Python 3.8+
- ✅ MySQL Server running
- ✅ Webcam connected
- ✅ Internet connection (for dependencies)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Database

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE smart_attendance;
exit;
```

### 3. Configure Environment

```bash
# Copy example config
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit .env with your settings
notepad .env  # Windows
nano .env     # Linux/Mac
```

**Minimum required settings:**

```env
DB_PASSWORD=your_mysql_password
DB_NAME=smart_attendance
```

### 4. Run Setup Check

```bash
python setup.py
```

This will verify all requirements and create necessary directories.

### 5. Start Application

```bash
python app.py
```

### 6. Access Dashboard

Open browser: **http://localhost:5000**

**Login credentials:**

- Username: `admin`
- Password: `admin123`

## First Steps

### 1. Register a Student

1. Click **"Register Student"**
2. Fill in student details
3. Allow webcam access
4. Click **"Capture & Register"**
5. Wait for face capture (30 images)
6. Model trains automatically

### 2. Mark Attendance

1. Click **"Mark Attendance"**
2. Upload student photo OR use webcam
3. Click **"Identify Faces"**
4. System marks attendance automatically

### 3. View Reports

1. Click **"Analytics"**
2. View attendance statistics
3. Export to CSV if needed

## Common Issues

### Database Connection Failed

```bash
# Check if MySQL is running
net start MySQL80  # Windows
sudo systemctl start mysql  # Linux

# Verify credentials in .env
```

### Webcam Not Working

```bash
# Test webcam
python -c "import cv2; print('Webcam:', cv2.VideoCapture(0).isOpened())"

# Should print: Webcam: True
```

### Module Not Found

```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Port Already in Use

```bash
# Change port in app.py (last line)
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Email Configuration (Optional)

For email notifications:

1. Get Gmail App Password:
    - Go to: https://myaccount.google.com/apppasswords
    - Generate password

2. Update .env:

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=generated_app_password
```

## Testing the System

### Test Face Recognition

```bash
# Train model with test data
python train_model.py

# Test recognition
python recognize_and_mark.py
```

### Test Email Sending

1. Register student with valid email
2. Click **"Email Absentees"**
3. Check email inbox

## Development Tips

### Enable Debug Mode

```env
FLASK_DEBUG=1
```

### View Logs

```bash
# Check application logs
tail -f app.log  # Linux/Mac
type app.log     # Windows
```

### Database Reset

```sql
-- WARNING: This deletes all data!
DROP DATABASE smart_attendance;
CREATE DATABASE smart_attendance;
```

## Project Structure

```
SmartCollegeWeb/
├── app.py              # Main application
├── config.py           # Configuration
├── setup.py            # Setup script
├── requirements.txt    # Dependencies
├── .env               # Your settings
├── utils/             # Utility modules
├── templates/         # HTML templates
└── student_images/    # Student photos
```

## Next Steps

1. ✅ Change default admin password
2. ✅ Register multiple students
3. ✅ Test face recognition
4. ✅ Configure email settings
5. ✅ Explore analytics dashboard

## Need Help?

- 📖 Read full README.md
- 🐛 Check troubleshooting section
- 💬 Create GitHub issue
- 📧 Contact: admin@college.edu

---

**Happy coding! 🎉**
