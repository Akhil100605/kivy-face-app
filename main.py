import os
import cv2
import numpy as np
from android.permissions import request_permissions, Permission, check_permission
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout


class FaceApp(App):

    def build(self):
        self.image = Image()
        layout = BoxLayout()
        layout.add_widget(self.image)

        # Haar cascade
        self.face_cascade = cv2.CascadeClassifier(
            "haarcascade_frontalface_default.xml"
        )

        # Face recognizer
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.labels = {}
        self.model_trained = False  # 🔑 important flag
        self.capture = None     
       

        # Camera
       
        return layout
    def on_start(self):
        if not check_permission(Permission.CAMERA):
            request_permissions([Permission.CAMERA])
            Clock.schedule_once(self.initialize_app, 2)
    def initialize_app(self, dt):
        print("intializing model and camera")
        self.train_model()
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("⚠ Unable to access the camera")
            return
        Clock.schedule_interval(self.update, 1.0 / 30.0)


    def train_model(self):
        faces = []
        labels = []
        label_id = 0

        base_dir = "known_faces"

        if not os.path.exists(base_dir):
            print("⚠ known_faces folder not found")
            return

        for person_name in os.listdir(base_dir):
            person_path = os.path.join(base_dir, person_name)
            if not os.path.isdir(person_path):
                continue

            self.labels[label_id] = person_name

            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                if img is None:
                    print(f"⚠ Failed to read {image_path}")
                    continue

                img = cv2.resize(img, (200, 200))
                faces.append(img)
                labels.append(label_id)

            label_id += 1

        if len(faces) < 2:
            print("⚠ Not enough training data. Add more images.")
            return

        self.recognizer.train(faces, np.array(labels))
        self.model_trained = True
        print("✅ Face recognition model trained")

    def recognize(self, face):
        if not self.model_trained:
            return "Unknown"

        face = cv2.resize(face, (200, 200))
        label, confidence = self.recognizer.predict(face)

        if confidence < 70:
            return self.labels[label]

        return "Unknown"

    def update(self, dt):
        if self.capture is None:
            return
        ret, frame = self.capture.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray, 1.3, 5, minSize=(100, 100)
        )

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            name = self.recognize(face)

            if name == "Unknown":
                color = (0, 0, 255)   # 🔴 red
            else:
                color = (0, 255, 0)   # 🟢 green

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(
                frame,
                name,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2
            )

        frame = cv2.flip(frame, 0)
        buf = frame.tobytes()
        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt="bgr"
        )
        texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        self.image.texture = texture

    def on_stop(self):
        if self.capture:
            self.capture.release()


if __name__ == "__main__":
    FaceApp().run()
