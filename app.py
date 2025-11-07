import os
from flask import Flask, render_template, request, redirect, session, url_for, send_file, jsonify, flash
from utils.face_utils import recognize_face, generate_qr_code, validate_image
from utils.attendance_utils import mark_attendance, get_attendance_report, get_attendance_statistics, \
    get_student_attendance_history
from utils.email_utils import send_absent_emails, send_registration_email
from db_config import get_connection, init_database
from train_model import train_face_model
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'student_images'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# Initialize database on startup
try:
    init_database()
    print("✅ Database initialized successfully")
except Exception as e:
    print(f"⚠️ Database initialization warning: {e}")


# Admin users management
def get_admin_user(username):
    """Get admin user from database"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin_users WHERE username = %s", (username,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error getting admin user: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()


def create_default_admin():
    """Create default admin user if not exists"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                           INSERT INTO admin_users (username, password_hash, email, full_name)
                           VALUES (%s, %s, %s, %s)
                           """, ('admin', generate_password_hash('admin123'), 'admin@college.edu', 'Administrator'))
            conn.commit()
            print("✅ Default admin user created (username: admin, password: admin123)")
    except Exception as e:
        print(f"Error creating default admin: {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()


create_default_admin()


# Authentication decorator
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = get_admin_user(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user'] = username
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid username or password', 'error')
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    stats = get_attendance_statistics()
    return render_template('dashboard.html', stats=stats, user=session.get('full_name', 'Admin'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    conn = None  # Initialize conn at the start
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            roll = request.form.get('roll', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            department = request.form.get('department', '').strip()

            # Validation
            if not all([name, roll, email]):
                return jsonify({'success': False, 'message': 'Name, Roll Number, and Email are required'}), 400

            # Check if roll number already exists
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM students WHERE roll_no = %s", (roll,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return jsonify({'success': False, 'message': f'Student with roll number {roll} already exists'}), 400

            # Create folder for student images
            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{name}_{roll}")
            os.makedirs(folder_path, exist_ok=True)

            # Save captured images (handle both base64 and file uploads)
            image_count = 0

            # Check for base64 images from JavaScript
            for key in request.form:
                if key.startswith('image_'):
                    img_data = request.form.get(key)
                    if img_data and img_data.startswith('data:image'):
                        # It's a base64 image
                        import base64
                        import io
                        from PIL import Image as PILImage

                        # Extract base64 data
                        header, encoded = img_data.split(',', 1)
                        img_bytes = base64.b64decode(encoded)
                        img = PILImage.open(io.BytesIO(img_bytes))

                        # Convert to grayscale and save
                        img = img.convert('L')
                        img.save(os.path.join(folder_path, f"face_{image_count}.jpg"))
                        image_count += 1

            # If no base64 images, check for file uploads
            if image_count == 0:
                for key in request.files:
                    if key.startswith('image_'):
                        img = request.files[key]
                        if img and img.filename:
                            # Validate image
                            is_valid, message = validate_image(img)
                            if is_valid:
                                img.save(os.path.join(folder_path, f"face_{image_count}.jpg"))
                                image_count += 1
                            img.seek(0)  # Reset file pointer

            if image_count == 0:
                cursor.close()
                conn.close()
                return jsonify({'success': False, 'message': 'No valid images captured. Please try again.'}), 400

            # Generate QR code for student
            qr_data = json.dumps({'roll_no': roll, 'name': name})
            qr_path = os.path.join(folder_path, 'qr_code.png')
            generate_qr_code(qr_data, qr_path)

            # Save to database
            cursor.execute("""
                           INSERT INTO students (name, roll_no, email, phone, department, image_path, qr_code)
                           VALUES (%s, %s, %s, %s, %s, %s, %s)
                           """, (name, roll, email, phone, department, folder_path, qr_path))
            conn.commit()

            print(f"✅ Student registered: {name} ({roll}) - {image_count} images captured")

            cursor.close()
            conn.close()

            # Train model with new data
            training_success = True
            training_message = "Model trained successfully"
            try:
                train_face_model()
            except Exception as train_error:
                print(f"⚠️ Model training warning: {train_error}")
                training_success = False
                training_message = f"Warning: Model training had issues - {str(train_error)}"

            # Send registration email
            try:
                send_registration_email(email, name, roll)
            except Exception as email_error:
                print(f"⚠️ Email sending warning: {email_error}")

            flash(f'Student {name} registered successfully!', 'success')
            return jsonify({
                'success': True,
                'message': f'Student {name} registered successfully! {image_count} images captured.',
                'training_status': training_success,
                'training_message': training_message
            }), 200

        except Exception as e:
            print(f"Error in registration: {e}")
            import traceback
            traceback.print_exc()
            if conn:
                try:
                    cursor.close()
                    conn.close()
                except:
                    pass
            return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'}), 500

    return render_template('register.html')

@app.route('/recognize', methods=['GET', 'POST'])
@login_required
def recognize():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image uploaded', 'error')
            return render_template('recognize.html', error='No image uploaded')

        image = request.files['image']
        if image.filename == '':
            flash('No image selected', 'error')
            return render_template('recognize.html', error='No image selected')

        try:
            # Recognize face
            result = recognize_face(image)

            if result['success']:
                # Get student info
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                               SELECT id, name, roll_no, email, department
                               FROM students
                               WHERE id = %s
                               """, (result['student_id'],))
                student = cursor.fetchone()

                if student:
                    # Mark attendance
                    attendance_marked = mark_attendance(student['roll_no'], method='Face',
                                                        marked_by=session.get('user', 'System'))

                    if attendance_marked:
                        result.update(student)
                        result['attendance_marked'] = True
                        flash(f'✅ Attendance marked for {student["name"]} ({student["roll_no"]})', 'success')
                    else:
                        result.update(student)
                        result['attendance_marked'] = False
                        result['already_marked'] = True
                        flash(f'⚠️ Attendance already marked for {student["name"]} ({student["roll_no"]}) today',
                              'warning')
                else:
                    flash('Student not found in database', 'error')
                    result['success'] = False

                cursor.close()
                conn.close()
            else:
                flash(result.get('message', 'Face not recognized'), 'warning')

            return render_template('recognize.html', result=result)

        except Exception as e:
            print(f"Error in recognition: {e}")
            import traceback
            traceback.print_exc()
            flash(f'Recognition failed: {str(e)}', 'error')
            return render_template('recognize.html', error=str(e))

    return render_template('recognize.html')

@app.route('/analytics')
@login_required
def analytics():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        report = get_attendance_report(start_date, end_date)
        stats = get_attendance_statistics()

        return render_template('analytics.html', report=report, stats=stats)
    except Exception as e:
        print(f"Error in analytics: {e}")
        flash(f'Error loading analytics: {str(e)}', 'error')
        return render_template('analytics.html', report=[], stats={})

@app.route('/export')
@login_required
def export():
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        report = get_attendance_report(start_date, end_date)
        path = get_attendance_report(start_date, end_date, export=True)

        flash('Attendance report exported successfully', 'success')
        return send_file(path, as_attachment=True)
    except Exception as e:
        print(f"Error exporting: {e}")
        flash(f'Export failed: {str(e)}', 'error')
        return redirect(url_for('analytics'))

@app.route('/email_absentees')
@login_required
def email_absentees():
    try:
        send_absent_emails()
        flash('Absence notification emails sent successfully', 'success')
    except Exception as e:
        flash(f'Failed to send emails: {str(e)}', 'error')
    return redirect(url_for('dashboard'))

@app.route('/student_panel')
def student_panel():
    return render_template('student_panel.html')


@app.route('/api/student/<roll_no>')
def get_student_info(roll_no):
    """API endpoint to get student information"""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
                       SELECT id, name, roll_no, email, phone, department, created_at
                       FROM students
                       WHERE roll_no = %s
                       """, (roll_no,))
        student = cursor.fetchone()

        if student:
            # Convert datetime to string for JSON serialization
            if 'created_at' in student and student['created_at']:
                student['created_at'] = student['created_at'].strftime('%Y-%m-%d %H:%M:%S')

            # Get attendance history
            history = get_student_attendance_history(roll_no)

            # Convert history tuples to serializable format
            serialized_history = []
            for record in history:
                # record format: (date, time, status, method)
                date_str = record[0].strftime('%Y-%m-%d') if record[0] else ''
                time_str = str(record[1]) if record[1] else ''
                status = record[2] if len(record) > 2 else ''
                method = record[3] if len(record) > 3 else ''
                serialized_history.append([date_str, time_str, status, method])

            student['attendance_history'] = serialized_history

            cursor.close()
            conn.close()

            return jsonify({'success': True, 'data': student})
        else:
            cursor.close()
            conn.close()
            return jsonify({'success': False, 'message': 'Student not found'}), 404
    except Exception as e:
        print(f"❌ Error in get_student_info for roll_no {roll_no}: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if conn:
            try:
                conn.close()
            except:
                pass


@app.route('/api/stats')
@login_required
def get_stats():
    """API endpoint for dashboard statistics"""
    try:
        stats = get_attendance_statistics()
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/mark_attendance_qr', methods=['POST'])
def mark_attendance_qr():
    """API endpoint for QR code attendance marking"""
    try:
        data = request.get_json()
        qr_data = json.loads(data.get('qr_data', '{}'))
        roll_no = qr_data.get('roll_no')

        if not roll_no:
            return jsonify({'success': False, 'message': 'Invalid QR code'}), 400

        success = mark_attendance(roll_no, method='QR', marked_by='Self')

        if success:
            return jsonify({'success': True, 'message': 'Attendance marked successfully'})
        else:
            return jsonify({'success': False, 'message': 'Attendance already marked or student not found'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/train_model')
@login_required
def train_model_route():
    """Endpoint to manually trigger model training"""
    try:
        train_face_model()
        flash('Face recognition model trained successfully', 'success')
    except Exception as e:
        flash(f'Model training failed: {str(e)}', 'error')
    return redirect(url_for('dashboard'))


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# Utility context processor
@app.context_processor
def utility_processor():
    return {
        'now': datetime.now(),
        'today': datetime.now().date()
    }


if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('recognizer', exist_ok=True)
    os.makedirs('attendance_reports', exist_ok=True)

    app.run(debug=True, host='0.0.0.0', port=5000)
