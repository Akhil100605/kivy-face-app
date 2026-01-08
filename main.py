import os
import cv2
import numpy as np

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture

FACE_DIR = "faces"


class FaceApp(App):

    def build(self):
        os.makedirs(FACE_DIR, exist_ok=True)

        self.cam_index = 0  # 0 = back, 1 = front

        self.layout = BoxLayout(orientation="vertical")

        self.img = Image()
        self.layout.add_widget(self.img)

        btn_layout = BoxLayout(size_hint_y=0.2)

        self.enroll_btn = Button(text="Enroll")
        self.enroll_btn.bind(on_press=self.enroll_face)

        self.rec_btn = Button(text="Recognize")
        self.rec_btn.bind(on_press=self.recognize_face)

        self.switch_btn = Button(text="Switch Cam")
        self.switch_btn.bind(on_press=self.switch_camera)

        btn_layout.add_widget(self.enroll_btn)
        btn_layout.add_widget(self.rec_btn)
        btn_layout.add_widget(self.switch_btn)

        self.layout.add_widget(btn_layout)

        # Open camera
        self.cap = cv2.VideoCapture(self.cam_index)

        # Face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        Clock.schedule_interval(self.update, 1.0 / 30)

        return self.layout

    # ---------------- CAMERA PREVIEW ----------------
    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            return

        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        self.img.texture = texture

    # ---------------- SWITCH CAMERA ----------------
    def switch_camera(self, *args):
        self.cam_index = 1 if self.cam_index == 0 else 0
        self.cap.release()
        self.cap = cv2.VideoCapture(self.cam_index)

    # ---------------- ENROLL FACE ----------------
    def enroll_face(self, *args):
        ret, frame = self.cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            print("No face found")
            return

        x, y, w, h = faces[0]
        face = gray[y:y + h, x:x + w]

        count = len(os.listdir(FACE_DIR))
        path = os.path.join(FACE_DIR, f"face_{count}.png")
        cv2.imwrite(path, face)
        print("Saved:", path)

    # ---------------- RECOGNIZE FACE ----------------
    def recognize_face(self, *args):
        files = os.listdir(FACE_DIR)
        if len(files) == 0:
            print("No enrolled faces")
            return

        images = []
        labels = []

        for i, f in enumerate(files):
            img = cv2.imread(os.path.join(FACE_DIR, f), cv2.IMREAD_GRAYSCALE)
            images.append(img)
            labels.append(i)

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(images, np.array(labels))

        ret, frame = self.cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            label, confidence = recognizer.predict(face)

            if confidence < 80:
                color = (0, 255, 0)
                text = "Known"
            else:
                color = (0, 0, 255)
                text = "Unknown"

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
        texture.blit_buffer(buf, colorfmt="bgr", bufferfmt="ubyte")
        self.img.texture = texture

    def on_stop(self):
        self.cap.release()


if __name__ == "__main__":
    FaceApp().run()
