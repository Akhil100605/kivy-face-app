import os
import cv2
import numpy as np
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Line
from kivy.core.window import Window

Window.rotation = 0
from android.permissions import request_permissions, Permission

request_permissions([
    Permission.CAMERA,
    Permission.READ_EXTERNAL_STORAGE,
    Permission.WRITE_EXTERNAL_STORAGE
])


class FaceApp(App):

    def build(self):
        self.cam_index = 0

        self.base_dir = os.getcwd()
        self.face_dir = os.path.join(self.base_dir, "faces")
        os.makedirs(self.face_dir, exist_ok=True)

        self.cascade = cv2.CascadeClassifier(
            os.path.join(self.base_dir, "haarcascade_frontalface_default.xml")
        )

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.labels = {}
        self.train_model()

        root = BoxLayout(orientation="vertical")

        self.camera = Camera(index=self.cam_index, play=True, resolution=(640, 480))
        root.add_widget(self.camera)

        btns = BoxLayout(size_hint_y=None, height=60)

        self.enroll_btn = Button(text="Enroll")
        self.switch_btn = Button(text="Switch")

        self.enroll_btn.bind(on_press=self.enroll_face)
        self.switch_btn.bind(on_press=self.switch_camera)

        btns.add_widget(self.enroll_btn)
        btns.add_widget(self.switch_btn)
        root.add_widget(btns)

        Clock.schedule_interval(self.detect_faces, 1 / 10)

        return root

    def switch_camera(self, *args):
        self.cam_index = 1 if self.cam_index == 0 else 0
        self.camera.index = self.cam_index

    def texture_to_cv2(self, texture):
        size = texture.size
        buf = np.frombuffer(texture.pixels, np.uint8)
        frame = buf.reshape(size[1], size[0], 4)
        frame = frame[:, :, :3]
        return frame

    def enroll_face(self, *args):
        tex = self.camera.texture
        if not tex:
            return

        frame = self.texture_to_cv2(tex)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            print("No face found")
            return

        x, y, w, h = faces[0]
        face_img = gray[y:y+h, x:x+w]

        name = f"user_{int(time.time())}.jpg"
        path = os.path.join(self.face_dir, name)
        cv2.imwrite(path, face_img)

        print("Saved:", path)
        self.train_model()

    def train_model(self):
        faces = []
        labels = []
        self.labels = {}

        label_id = 0

        for file in os.listdir(self.face_dir):
            if not file.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            path = os.path.join(self.face_dir, file)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue

            faces.append(img)
            labels.append(label_id)
            self.labels[label_id] = file
            label_id += 1

        if len(faces) > 0:
            self.recognizer.train(faces, np.array(labels))
            print("Model trained")

    def detect_faces(self, dt):
        tex = self.camera.texture
        if not tex:
            return

        frame = self.texture_to_cv2(tex)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.cascade.detectMultiScale(gray, 1.3, 5)

        self.camera.canvas.after.clear()
        with self.camera.canvas.after:
            for (x, y, w, h) in faces:
                label = "Unknown"
                color = (1, 0, 0)

                if len(self.labels) > 0:
                    roi = gray[y:y+h, x:x+w]
                    id_, conf = self.recognizer.predict(roi)
                    if conf < 80:
                        label = self.labels.get(id_, "Known")
                        color = (0, 1, 0)

                Color(*color)
                Line(rectangle=(x, y, w, h), width=2)


if __name__ == "__main__":
    FaceApp().run()
