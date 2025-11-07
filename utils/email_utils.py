import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db_config import get_connection
from datetime import date
import os


def send_email(to_email, subject, html_body, plain_body=None):
    """
    Generic email sending function with HTML support
    """
    EMAIL_USER = os.environ.get('EMAIL_USER')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    if not EMAIL_USER or not EMAIL_PASS:
        print("⚠️ Email credentials not set. Please set EMAIL_USER and EMAIL_PASS environment variables.")
        return False

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = to_email

        # Add plain text and HTML parts
        if plain_body:
            part1 = MIMEText(plain_body, 'plain')
            msg.attach(part1)

        part2 = MIMEText(html_body, 'html')
        msg.attach(part2)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
            print(f"✅ Email sent to: {to_email}")
            return True

    except smtplib.SMTPException as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        return False


def send_registration_email(email, name, roll_no=None):
    """
    Send registration confirmation email with enhanced HTML template
    """
    subject = '🎉 Welcome to Smart College Dashboard'

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background-color: white;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background-color: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Smart College!</h1>
            </div>
            <div class="content">
                <h2>Hello {name}! 👋</h2>
                <p>Your registration has been successfully completed.</p>
                {f'<p><strong>Your Roll Number:</strong> {roll_no}</p>' if roll_no else ''}
                <p>You can now:</p>
                <ul>
                    <li>✅ Mark attendance using face recognition</li>
                    <li>📊 View your attendance history</li>
                    <li>📧 Receive attendance notifications</li>
                    <li>📲 Use QR code for quick attendance</li>
                </ul>
                <p>Thank you for joining us!</p>
            </div>
            <div class="footer">
                <p>© 2025 Smart College Dashboard. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    plain_body = f"""
    Hello {name}!
    
    Your registration has been successfully completed.
    {f'Your Roll Number: {roll_no}' if roll_no else ''}
    
    You can now use all features of Smart College Dashboard.
    
    Thank you for joining us!
    
    © 2025 Smart College Dashboard
    """

    return send_email(email, subject, html_body, plain_body)


def send_absent_emails():
    """
    Sends attendance alert emails to students who were absent today.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        today = date.today()

        # Get absent students (not in attendance table)
        cursor.execute("""
                       SELECT s.name, s.email, s.roll_no, s.department
                       FROM students s
                       WHERE s.id NOT IN (SELECT student_id FROM attendance WHERE date =%s)
        """, (today,))
        absent_students = cursor.fetchall()

        if not absent_students:
            print("✅ All students are present. No emails sent.")
            return

        sent_count = 0
        for name, email, roll_no, department in absent_students:
            subject = '🚨 Attendance Alert - You Were Marked Absent'

            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #f9f9f9;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                        color: white;
                        padding: 30px;
                        text-align: center;
                        border-radius: 10px 10px 0 0;
                    }}
                    .content {{
                        background-color: white;
                        padding: 30px;
                        border-radius: 0 0 10px 10px;
                    }}
                    .alert {{
                        background-color: #fff3cd;
                        border-left: 4px solid #ffc107;
                        padding: 15px;
                        margin: 20px 0;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 20px;
                        color: #666;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>⚠️ Attendance Alert</h1>
                    </div>
                    <div class="content">
                        <h2>Dear {name},</h2>
                        <div class="alert">
                            <strong>You were marked absent on {today.strftime('%d %B %Y')}</strong>
                        </div>
                        <p><strong>Roll Number:</strong> {roll_no}</p>
                        {f'<p><strong>Department:</strong> {department}</p>' if department else ''}
                        <p>If this is a mistake or you have a valid reason for your absence, 
                        please contact the administration as soon as possible.</p>
                        <p><strong>Important:</strong> Regular attendance is crucial for your academic progress.</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 Smart College Dashboard. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """

            plain_body = f"""
            Dear {name},
            
            You were marked absent on {today.strftime('%d-%m-%Y')}.
            
            Roll Number: {roll_no}
            {f'Department: {department}' if department else ''}
            
            If this is a mistake, please contact the administration.
            
            Regards,
            Smart College Dashboard
            """

            if send_email(email, subject, html_body, plain_body):
                sent_count += 1

        print(f"✅ Sent {sent_count} absence alert emails")

    except Exception as e:
        print(f"❌ Error while sending emails: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


def send_weekly_report_email(email, name, attendance_data):
    """
    Send weekly attendance summary report to student
    """
    subject = '📊 Weekly Attendance Report'

    present_days = sum(1 for day in attendance_data if day['status'] in ['Present', 'Late'])
    total_days = len(attendance_data)
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .content {{
                background-color: white;
                padding: 30px;
                border-radius: 0 0 10px 10px;
            }}
            .stats {{
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
            }}
            .stat-box {{
                text-align: center;
                padding: 15px;
                background-color: #f0f0f0;
                border-radius: 8px;
                flex: 1;
                margin: 0 10px;
            }}
            .stat-number {{
                font-size: 32px;
                font-weight: bold;
                color: #667eea;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Weekly Attendance Report</h1>
            </div>
            <div class="content">
                <h2>Hello {name}!</h2>
                <p>Here's your attendance summary for this week:</p>
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-number">{present_days}</div>
                        <div>Days Present</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{total_days - present_days}</div>
                        <div>Days Absent</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{attendance_percentage:.1f}%</div>
                        <div>Attendance Rate</div>
                    </div>
                </div>
                <p>Keep up the good work! 🎉</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(email, subject, html_body)
