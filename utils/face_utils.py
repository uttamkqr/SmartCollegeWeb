import cv2
import numpy as np
from PIL import Image
import os
import qrcode
from io import BytesIO
import base64

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_faces(gray_img):
    """
    Detect faces from a grayscale image using Haar Cascade.
    Returns list of face regions (x, y, w, h).
    """
    faces = face_cascade.detectMultiScale(
        gray_img,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces


def preprocess_face(face_img):
    """
    Preprocess face image for better recognition
    """
    # Resize to standard size
    face_img = cv2.resize(face_img, (200, 200))

    # Apply histogram equalization for better contrast
    face_img = cv2.equalizeHist(face_img)

    # Apply Gaussian blur to reduce noise
    face_img = cv2.GaussianBlur(face_img, (5, 5), 0)

    return face_img


def capture_faces_from_webcam(folder_path, count=30):
    """
    Captures faces from webcam and saves them in the given folder with preprocessing.
    """
    cap = cv2.VideoCapture(0)
    os.makedirs(folder_path, exist_ok=True)
    print("📷 Look at the camera...")

    captured = 0
    frame_skip = 0

    while captured < count:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to capture frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(gray)

        # Display instructions on frame
        cv2.putText(frame, f"Captured: {captured}/{count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press ESC to cancel", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        for (x, y, w, h) in faces:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Capture face with interval to get varied expressions
            if frame_skip % 3 == 0:  # Capture every 3rd frame
                face = gray[y:y + h, x:x + w]
                face = preprocess_face(face)
                cv2.imwrite(os.path.join(folder_path, f"face_{captured}.jpg"), face)
                captured += 1
                print(f"✅ Captured {captured}/{count}")

                if captured >= count:
                    break

        frame_skip += 1
        cv2.imshow("Capturing Faces - Press ESC to cancel", frame)

        if cv2.waitKey(1) == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Face capture complete. Total images: {captured}")
    return captured

def recognize_face(image_file):
    """
    Recognizes a face from an uploaded image file.
    Returns dict with student info if recognized, otherwise None.
    """
    try:
        # Check if model exists
        model_path = "recognizer/trainer.yml"
        if not os.path.exists(model_path) or os.path.getsize(model_path) == 0:
            return {
                'success': False,
                'message': 'Model not trained. Please train the model first.',
                'student_id': None,
                'confidence': 0
            }

        # Load recognizer model
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(model_path)

        # Read uploaded image
        if isinstance(image_file, str):
            img = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
        else:
            img = Image.open(image_file).convert('L')  # Grayscale
            img = np.array(img, 'uint8')

        # Detect face
        faces = detect_faces(img)
        if len(faces) == 0:
            return {
                'success': False,
                'message': 'No face detected in the image',
                'student_id': None,
                'confidence': 0
            }

        for (x, y, w, h) in faces:
            face = img[y:y + h, x:x + w]
            face = preprocess_face(face)
            student_id, confidence = recognizer.predict(face)

            # Lower confidence value means better match
            # Threshold: confidence < 100 is acceptable (very relaxed for poor conditions)
            print(f"🔍 Face detected - Student ID: {student_id}, Confidence: {confidence:.2f}")

            if confidence < 40:
                # Excellent match
                return {
                    'success': True,
                    'message': 'Face recognized successfully with high confidence',
                    'student_id': student_id,
                    'confidence': round(100 - confidence, 2),
                    'match_quality': 'High'
                }
            elif confidence < 70:
                # Good match
                return {
                    'success': True,
                    'message': 'Face recognized successfully',
                    'student_id': student_id,
                    'confidence': round(100 - confidence, 2),
                    'match_quality': 'Medium'
                }
            elif confidence < 100:
                # Acceptable match (relaxed threshold)
                return {
                    'success': True,
                    'message': 'Face recognized with acceptable confidence',
                    'student_id': student_id,
                    'confidence': round(100 - confidence, 2),
                    'match_quality': 'Acceptable'
                }
            else:
                # Poor match
                return {
                    'success': False,
                    'message': f'Face not recognized with sufficient confidence (confidence: {confidence:.1f}). Please ensure good lighting and clear face. Try: 1) Turn on all lights 2) Face camera directly 3) Move closer 4) Or use QR method instead.',
                    'student_id': None,
                    'confidence': round(100 - confidence, 2),
                    'raw_confidence': confidence
                }

        return {
            'success': False,
            'message': 'No matching face found',
            'student_id': None,
            'confidence': 0
        }

    except Exception as e:
        print(f"❌ Error in face recognition: {e}")
        return {
            'success': False,
            'message': f'Error: {str(e)}',
            'student_id': None,
            'confidence': 0
        }


def generate_qr_code(data, filename=None):
    """
    Generate QR code for student data
    Returns base64 encoded image if no filename, otherwise saves to file
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    if filename:
        img.save(filename)
        return filename
    else:
        # Return base64 encoded image
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"


def validate_image(file):
    """
    Validate uploaded image file
    """
    try:
        img = Image.open(file)
        img.verify()

        # Check file size (max 5MB)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > 5 * 1024 * 1024:  # 5MB
            return False, "File size too large. Maximum 5MB allowed."

        # Check image dimensions
        img = Image.open(file)
        width, height = img.size
        if width < 100 or height < 100:
            return False, "Image resolution too low. Minimum 100x100 pixels required."

        return True, "Valid image"

    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def capture_and_save_image(file, folder_path, filename):
    """
    Save uploaded image file with validation
    """
    is_valid, message = validate_image(file)
    if not is_valid:
        return False, message

    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, filename)

    try:
        file.seek(0)  # Reset file pointer
        file.save(filepath)
        return True, filepath
    except Exception as e:
        return False, f"Error saving file: {str(e)}"
