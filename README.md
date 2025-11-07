# 📘 Smart College Dashboard (Enhanced Web-Based System)

A comprehensive facial recognition-based web application for automating student attendance with real-time tracking, QR
code support, analytics, and email notifications.

## 🚀 Features

### Core Features

- 🎭 **Advanced Face Recognition** with OpenCV (LBPH Algorithm)
- 👨‍🎓 **Student Registration** with webcam capture and validation
- 📅 **Real-time Attendance Marking** with multiple methods
- 🧠 **Auto-Training Face Model** after each registration
- 📬 **Email Notifications** with beautiful HTML templates
- 📊 **Attendance Analytics Dashboard** with statistics
- 📷 **Webcam Support** for image capture
- 🔐 **Secure Admin Login System** with session management
- 📲 **QR Code Generation** for each student
- ✅ **QR Code Attendance Marking** (contactless)

### New Enhanced Features

- 🔒 **Database Connection Pooling** for better performance
- 📈 **Attendance Statistics** (daily, weekly, monthly)
- 📉 **Attendance Reports** with date range filtering
- 💾 **CSV Export** functionality for reports
- 🎨 **Modern UI/UX** with responsive design
- 🔔 **Flash Messages** for user feedback
- 🛡️ **Image Validation** (size, format, dimensions)
- 📝 **Attendance Logs** for detailed tracking
- 🌐 **RESTful API Endpoints** for integration
- 🔄 **Status Tracking** (Present, Late, Absent)
- 👤 **Student Profile Management** with history
- 📧 **Enhanced Email Templates** with HTML styling

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- Webcam (for face capture)
- Gmail account (for email notifications)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SmartCollegeWeb
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database

Create a MySQL database:

```sql
CREATE
DATABASE smart_attendance;
```

The application will automatically create all necessary tables on first run:

- `students` - Student information
- `attendance` - Attendance records
- `admin_users` - Admin accounts
- `attendance_logs` - Detailed activity logs

**⚠️ For Existing Installations:**

If you're upgrading from an older version, run the migration script to update the database schema:

```bash
python migrate_database.py
```

This will add the missing `marked_by` and `method` columns to the attendance table.

### 5. Configure Environment Variables

Copy `.env.example` to `.env` and update with your settings:

```bash
cp .env.example .env
```

Edit `.env`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=smart_attendance

EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

SECRET_KEY=your-secret-key
```

**For Gmail:**

1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the generated password in `EMAIL_PASS`

### 6. Run the Application

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## 🔑 Default Credentials

- **Username:** admin
- **Password:** admin123

⚠️ **Important:** Change default credentials after first login!

## 📖 Usage Guide

### Admin Dashboard

1. **Login** - Access the admin panel
2. **Dashboard** - View statistics and recent activity
3. **Register Student**
    - Enter student details
    - Capture face images via webcam (30 images)
    - System auto-generates QR code
    - Model trains automatically
    - Registration email sent
4. **Mark Attendance**
    - Upload student photo or use webcam
    - System recognizes face and marks attendance
    - Shows confidence score and student details
5. **Analytics**
    - View attendance reports
    - Filter by date range
    - Export to CSV
6. **Email Absentees**
    - Send notification emails to absent students
    - Beautiful HTML email templates

### Student Panel

- View personal attendance history
- Check QR code
- Self-service attendance marking

## 🔌 API Endpoints

### Student Information

```http
GET /api/student/<roll_no>
Authorization: Required (Session)

Response:
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "roll_no": "2024001",
    "email": "john@example.com",
    "attendance_history": [...]
  }
}
```

### Statistics

```http
GET /api/stats
Authorization: Required (Session)

Response:
{
  "success": true,
  "data": {
    "total_students": 50,
    "present_today": 45,
    "absent_today": 5,
    "attendance_rate_today": 90.0
  }
}
```

### QR Code Attendance

```http
POST /api/mark_attendance_qr
Content-Type: application/json

Body:
{
  "qr_data": "{\"roll_no\": \"2024001\", \"name\": \"John Doe\"}"
}

Response:
{
  "success": true,
  "message": "Attendance marked successfully"
}
```

## 📁 Project Structure

```
SmartCollegeWeb/
├── app.py                  # Main Flask application
├── db_config.py            # Database configuration & initialization
├── train_model.py          # Face recognition model training
├── recognize_and_mark.py   # Real-time recognition script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── utils/
│   ├── face_utils.py       # Face detection & recognition utilities
│   ├── attendance_utils.py # Attendance management functions
│   └── email_utils.py      # Email sending utilities
├── templates/
│   ├── login.html          # Login page
│   ├── dashboard.html      # Admin dashboard
│   ├── register.html       # Student registration
│   ├── recognize.html      # Face recognition page
│   ├── analytics.html      # Attendance reports
│   ├── student_panel.html  # Student dashboard
│   ├── 404.html            # Error page
│   └── 500.html            # Error page
├── static/
│   └── css/                # Stylesheets
├── student_images/         # Student face images
├── recognizer/
│   └── trainer.yml         # Trained model file
└── attendance_reports/     # Exported CSV files
```

## 🔧 Advanced Configuration

### Face Recognition Parameters

Edit `utils/face_utils.py`:

```python
# Detection sensitivity
scaleFactor = 1.1  # Lower = more sensitive (1.1 - 1.3)
minNeighbors = 5  # Higher = fewer false positives (3 - 6)

# Recognition threshold
confidence < 70  # Lower = stricter matching (50 - 80)
```

### Attendance Time Rules

Edit `utils/attendance_utils.py`:

```python
# Late arrival time (default: 9:15 AM)
if time_now.hour > 9 or (time_now.hour == 9 and time_now.minute > 15):
    status = 'Late'
```

## 🐛 Troubleshooting

### Common Issues

**1. Webcam Not Working**

- Check camera permissions
- Ensure no other app is using the camera
- Try different USB port

**2. Face Not Recognized**

- Ensure good lighting
- Capture images from multiple angles
- Retrain the model

**3. Database Connection Error**

- Verify MySQL is running
- Check credentials in `.env`
- Ensure database exists

**4. Email Not Sending**

- Use Gmail App Password (not regular password)
- Enable "Less secure app access" if needed
- Check SMTP settings

**5. Model Training Failed**

- Ensure at least one student is registered
- Check image folder permissions
- Verify images are valid

## 🔐 Security Recommendations

1. **Change default admin password immediately**
2. **Use strong SECRET_KEY in production**
3. **Never commit `.env` file to version control**
4. **Use HTTPS in production**
5. **Implement rate limiting for API endpoints**
6. **Regular database backups**
7. **Keep dependencies updated**

## 📊 Performance Tips

- Use connection pooling (already implemented)
- Optimize image sizes before storing
- Regular database maintenance
- Cache frequently accessed data
- Use CDN for static assets in production

## 🚀 Deployment

### Production Setup

1. Set environment to production:

```env
FLASK_ENV=production
FLASK_DEBUG=0
```

2. Use production WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. Setup reverse proxy (Nginx):

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Developer

Developed with ❤️ by Uttam Agrawal

## 📞 Support

For issues and questions:

- Create an issue on GitHub
- Email: admin@college.edu

## 🎯 Future Enhancements

- [ ] Mobile app integration
- [ ] Fingerprint authentication
- [ ] SMS notifications
- [ ] Multi-class support
- [ ] Attendance prediction AI
- [ ] Geolocation tracking
- [ ] Blockchain verification
- [ ] Integration with LMS platforms
- [ ] Advanced analytics with charts
- [ ] Parent portal access

---

**Version:** 2.0.0  
**Last Updated:** January 2025