from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.camera import Camera
import cv2
import numpy as np
import os
import pickle
import threading
from kivy.metrics import dp
import time

class FaceRecognitionApp(App):
    def build(self):
        self.known_faces = []
        self.known_names = []
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.is_recognizing = False
        self.camera_thread = None
        
        # Load known faces
        self.load_known_faces()
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Camera texture widget
        self.texture = Texture.create(size=(640, 480), colorfmt='rgb')
        self.camera_label = Label(text='Initializing camera...', size_hint=(1, 0.8))
        layout.add_widget(self.camera_label)
        
        # Buttons
        btn_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=dp(5))
        self.start_btn = Button(text='Start Recognition')
        self.start_btn.bind(on_press=self.toggle_recognition)
        btn_layout.add_widget(self.start_btn)
        
        self.enroll_btn = Button(text='Enroll Face')
        self.enroll_btn.bind(on_press=self.enroll_face)
        btn_layout.add_widget(self.enroll_btn)
        
        layout.add_widget(btn_layout)
        
        # Status label
        self.status_label = Label(text='Ready', size_hint=(1, 0.1))
        layout.add_widget(self.status_label)
        
        Clock.schedule_interval(self.update_display, 1.0 / 30.0)
        return layout
    
    def toggle_recognition(self, instance):
        if not self.is_recognizing:
            self.start_recognition()
        else:
            self.stop_recognition()
    
    def start_recognition(self):
        self.is_recognizing = True
        self.start_btn.text = 'Stop Recognition'
        self.status_label.text = 'Recognizing...'
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()
    
    def stop_recognition(self):
        self.is_recognizing = False
        self.start_btn.text = 'Start Recognition'
        self.status_label.text = 'Stopped'
    
    def camera_loop(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Portrait orientation fix for Android
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YV12'))
        
        while self.is_recognizing:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            
            # Fix orientation and mirroring for portrait
            frame = cv2.flip(frame, 1)  # Mirror horizontally
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)  # Portrait rotation
            
            self.process_frame(frame)
            time.sleep(0.03)
        
        cap.release()
    
    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (100, 100))
            
            # Recognize face
            label, confidence = self.recognizer.predict(face_roi)
            
            if confidence < 80:  # Known face threshold
                name = self.known_names[label]
                color = (0, 255, 0)  # Green
                self.status_label.text = f'Recognized: {name}'
            else:
                name = "Unknown"
                color = (0, 0, 255)  # Red
                self.status_label.text = 'Unknown face detected'
            
            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # Convert to RGB and update texture
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame_data = frame_rgb.tobytes()
        self.texture_size = frame_rgb.shape[1], frame_rgb.shape[0]
    
    def update_display(self, dt):
        if hasattr(self, 'frame_data') and self.texture:
            self.texture.blit_buffer(self.frame_data, colorfmt='rgb', bufferfmt='ubyte')
            self.texture.flip_vertical()
            self.camera_label.texture = self.texture
        return True
    
    def enroll_face(self, instance):
        self.status_label.text = 'Enrollment mode - look at camera'
        # Simplified enrollment - in production, add name input dialog
        threading.Thread(target=self.enroll_thread, daemon=True).start()
    
    def enroll_thread(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        name = "User_" + str(len(self.known_names) + 1)  # Auto name
        faces = []
        
        for i in range(30):  # Capture 30 samples
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                for (x, y, w, h) in face:
                    faces.append(cv2.resize(gray[y:y+h, x:x+w], (100, 100)))
            time.sleep(0.1)
        
        cap.release()
        
        if len(faces) > 10:
            self.known_faces.extend(faces[-20:])  # Use last 20 samples
            self.known_names.append(name)
            self.train_recognizer()
            self.status_label.text = f'Enrolled: {name}'
        else:
            self.status_label.text = 'Enrollment failed - not enough samples'
    
    def train_recognizer(self):
        if len(self.known_faces) > 0:
            self.recognizer.train(self.known_faces, np.arange(len(self.known_names)))
        self.save_known_faces()
    
    def save_known_faces(self):
        data = {'faces': self.known_faces, 'names': self.known_names}
        try:
            with open('known_faces.pkl', 'wb') as f:
                pickle.dump(data, f)
        except:
            pass  # Ignore save errors on Android
    
    def load_known_faces(self):
        try:
            if os.path.exists('known_faces.pkl'):
                with open('known_faces.pkl', 'rb') as f:
                    data = pickle.load(f)
                    self.known_faces = data['faces']
                    self.known_names = data['names']
                if len(self.known_faces) > 0:
                    self.train_recognizer()
        except:
            pass

if __name__ == '__main__':
    FaceRecognitionApp().run()


