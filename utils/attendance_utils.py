import mysql.connector
from datetime import datetime, date, timedelta
from db_config import get_connection
import csv
import os


def mark_attendance(roll_no, method='Face', marked_by='System'):
    """
    Mark attendance for a student with enhanced tracking
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        date_today = datetime.now().date()
        time_now = datetime.now().time()

        # Get student ID first
        cursor.execute("SELECT id, name FROM students WHERE roll_no = %s", (roll_no,))
        student = cursor.fetchone()

        if not student:
            print(f"❌ Student with roll number {roll_no} not found in DB.")
            return False

        student_id, student_name = student
        print(f"📝 Found student: {student_name} (ID: {student_id}, Roll: {roll_no})")

        # Check if already marked
        cursor.execute("""
            SELECT * FROM attendance 
            WHERE student_id = %s AND date = %s
        """, (student_id, date_today))

        existing = cursor.fetchone()
        if existing:
            print(f"🟡 Attendance already marked for {roll_no} ({student_name}) on {date_today}")
            cursor.close()
            conn.close()
            return False

        # Determine status based on time (assuming class starts at 9:00 AM)
        status = 'Present'
        if time_now.hour > 9 or (time_now.hour == 9 and time_now.minute > 15):
            status = 'Late'

        print(f"⏰ Marking attendance - Status: {status}, Time: {time_now}")

        cursor.execute("""
                       INSERT INTO attendance (student_id, date, time, status, marked_by, method)
                       VALUES (%s, %s, %s, %s, %s, %s)
                       """, (student_id, date_today, time_now, status, marked_by, method))

        # Log the attendance action
        cursor.execute("""
                       INSERT INTO attendance_logs (student_id, action)
                       VALUES (%s, %s)
                       """, (student_id, f"Attendance marked: {status} via {method}"))

        conn.commit()
        print(f"✅ Attendance marked successfully for {roll_no} ({student_name}) - Status: {status}")

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as err:
        print(f"❌ Database Error in mark_attendance: {err}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"❌ Unexpected Error in mark_attendance: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            try:
                if cursor:
                    cursor.close()
                conn.close()
            except:
                pass


def get_attendance_report(start_date=None, end_date=None, export=False):
    """
    Get attendance report with date range filtering
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if not start_date:
            start_date = date.today()
        if not end_date:
            end_date = date.today()

        query = """
                SELECT s.roll_no, s.name, a.date, a.time, a.status, a.method
                FROM attendance a
                         JOIN students s ON a.student_id = s.id
                WHERE a.date BETWEEN %s AND %s
                ORDER BY a.date DESC, a.time DESC \
                """

        cursor.execute(query, (start_date, end_date))
        report = cursor.fetchall()

        if export:
            return export_to_csv(report, start_date, end_date)

        return report

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()


def export_to_csv(data, start_date, end_date):
    """
    Export attendance data to CSV file
    """
    os.makedirs('attendance_reports', exist_ok=True)
    filename = f"attendance_reports/attendance_{start_date}_to_{end_date}.csv"

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Roll No', 'Name', 'Date', 'Time', 'Status', 'Method'])
        writer.writerows(data)

    print(f"✅ Report exported to {filename}")
    return filename


def get_attendance_statistics():
    """
    Get overall attendance statistics
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Total students
        cursor.execute("SELECT COUNT(*) as total FROM students")
        total_students = cursor.fetchone()['total']

        # Today's attendance
        today = date.today()
        cursor.execute("""
                       SELECT COUNT(*) as present
                       FROM attendance
                       WHERE date = %s AND status IN ('Present', 'Late')
                       """, (today,))
        present_today = cursor.fetchone()['present']

        # Attendance rate for today
        attendance_rate = (present_today / total_students * 100) if total_students > 0 else 0

        # Weekly attendance
        week_ago = today - timedelta(days=7)
        cursor.execute("""
                       SELECT COUNT(DISTINCT student_id) as present
                       FROM attendance
                       WHERE date BETWEEN %s
                         AND %s
                       """, (week_ago, today))
        present_this_week = cursor.fetchone()['present']

        return {
            'total_students': total_students,
            'present_today': present_today,
            'absent_today': total_students - present_today,
            'attendance_rate_today': round(attendance_rate, 2),
            'present_this_week': present_this_week
        }

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return {}
    finally:
        if conn:
            cursor.close()
            conn.close()


def get_student_attendance_history(roll_no):
    """
    Get attendance history for a specific student
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                       SELECT a.date, a.time, a.status, a.method
                       FROM attendance a
                                JOIN students s ON a.student_id = s.id
                       WHERE s.roll_no = %s
                       ORDER BY a.date DESC LIMIT 30
                       """, (roll_no,))

        return cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return []
    finally:
        if conn:
            cursor.close()
            conn.close()
