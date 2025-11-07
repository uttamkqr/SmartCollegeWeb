# 🚀 Smart College Web - Setup Instructions

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- MySQL Server
- Git

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/uttamkqr/SmartCollegeWeb.git
cd SmartCollegeWeb
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file and update with your credentials:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_mysql_password
   DB_NAME=smart_attendance
   
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_specific_password
   
   SECRET_KEY=generate-a-strong-random-key
   ```

### 5. Setup MySQL Database

1. Login to MySQL:
   ```bash
   mysql -u root -p
   ```

2. Create database:
   ```sql
   CREATE DATABASE smart_attendance;
   exit;
   ```

3. Initialize tables:
   ```bash
   python fix_database.py
   ```

### 6. Run the Application

```bash
# Windows
start.bat

# Or manually:
python app.py
```

The application will be available at: http://localhost:5000

## Default Admin Login

- **Username:** admin
- **Password:** admin123

⚠️ **Important:** Change the default password after first login!

## Directory Structure

```
SmartCollegeWeb/
├── student_images/     # Student photos (auto-created)
├── attendance_reports/ # Generated reports (auto-created)
├── recognizer/        # Face recognition models (auto-created)
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── utils/            # Helper functions
└── .env              # Your configuration (DO NOT COMMIT)
```

## Troubleshooting

### Database Connection Error

- Verify MySQL is running
- Check credentials in `.env` file
- Ensure database exists

### Face Recognition Not Working

- Ensure OpenCV is properly installed
- Check if webcam permissions are granted
- Train the model with at least 30 images per student

### Module Import Errors

```bash
pip install --upgrade -r requirements.txt
```

## Features

✅ Student Registration with Face Recognition  
✅ Automated Attendance Marking  
✅ QR Code Based Attendance  
✅ Real-time Dashboard  
✅ Attendance Reports & Analytics  
✅ Email Notifications  
✅ Student Portal

## Support

For issues and questions:

- GitHub Issues: https://github.com/uttamkqr/SmartCollegeWeb/issues
- Documentation: Check the various MD files in the repository

## Security Notes

⚠️ **Never commit:**

- `.env` file
- Student images
- Database backups
- Trained models
- Personal data

These are automatically excluded via `.gitignore`

## License

This project is for educational purposes.
