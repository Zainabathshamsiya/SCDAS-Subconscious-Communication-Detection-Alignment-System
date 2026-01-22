import cv2
import numpy as np


class MicroExpressionDetector:
    def __init__(self):
        pass

    def extract_action_units(self, face_region):
        """
        Simulated Action Unit extraction
        """
        gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
        h = gray.shape[0]

        action_units = {
            "AU1": float(np.mean(gray[:h // 3]) / 255.0),
            "AU4": float(np.std(gray[:h // 3]) / 255.0),
            "AU12": float(np.mean(gray[2 * h // 3:]) / 255.0),
            "AU15": float(np.std(gray[2 * h // 3:]) / 255.0),
        }

        return action_units

    def classify_expression(self, action_units):
        """
        Returns:
        - expression (str)
        - confidence (float 0–1)
        """
        au12 = action_units["AU12"]
        au4 = action_units["AU4"]
        au15 = action_units["AU15"]

        if au12 > 0.6:
            return "agreement", au12
        elif au4 > 0.6:
            return "tension", au4
        elif au15 > 0.6:
            return "doubt", au15
        else:
            return "neutral", 0.5
