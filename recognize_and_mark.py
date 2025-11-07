import cv2
import numpy as np
import os
from utils.face_utils import detect_face
from utils.attendance_utils import mark_attendance
from db_config import get_connection

def recognize_and_mark():
    print("📷 Starting real-time recognition...")

    trainer_path = 'recognizer/trainer.yml'
    if not os.path.exists(trainer_path) or os.stat(trainer_path).st_size == 0:
        print("❌ Error: trainer.yml not found or empty. Please train the model first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(trainer_path)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to capture frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            id_, confidence = recognizer.predict(face)

            if confidence < 70:
                cursor.execute("SELECT name, roll_no FROM students WHERE id = %s", (id_,))
                result = cursor.fetchone()
                if result:
                    name, roll = result
                    mark_attendance(roll)
                    label = f"{name} ({roll})"
                    print(f"✅ Recognized: {label} | Confidence: {confidence:.2f}")
                else:
                    label = "Unknown"
                    print(f"⚠️ ID {id_} not found in database.")
            else:
                label = "Unknown"
                print("🟡 Unknown face detected.")

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Recognition", frame)
        if cv2.waitKey(1) == 13:  # Enter key
            break

    cap.release()
    cv2.destroyAllWindows()
    conn.close()

if __name__ == "__main__":
    recognize_and_mark()
