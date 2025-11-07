import cv2
import numpy as np
from PIL import Image
import os

def train_face_model():
    print("🧠 Starting training...")
    data_dir = 'student_images'
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces = []
    labels = []

    for folder_name in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder_name)

        if not os.path.isdir(folder_path):
            continue

        # Skip folder if no digits (label will fail)
        if not any(char.isdigit() for char in folder_name):
            print(f"⚠️ Skipping folder with no digits in name: {folder_name}")
            continue

        label = int(''.join(filter(str.isdigit, folder_name)))

        for image_name in os.listdir(folder_path):
            img_path = os.path.join(folder_path, image_name)
            img = Image.open(img_path).convert('L')
            img_np = np.array(img, 'uint8')

            faces.append(img_np)
            labels.append(label)

    if len(faces) == 0:
        print("❌ No images found to train.")
        return

    recognizer.train(faces, np.array(labels))
    os.makedirs('recognizer', exist_ok=True)
    recognizer.save('recognizer/trainer.yml')
    print("✅ Training complete. Model saved to recognizer/trainer.yml")

if __name__ == "__main__":
    train_face_model()
