import cv2
import numpy as np

class GazeTracker:

    def __init__(self):

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )

    def detect(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            roi_gray = gray[y:y+h, x:x+w]

            eyes = self.eye_cascade.detectMultiScale(roi_gray)

            if len(eyes) > 0:
                return "focused"

        return "not focused"
