from deepface import DeepFace

class EmotionDetector:

    def detect(self, frame):

        try:

            result = DeepFace.analyze(
                frame,
                actions=["emotion"],
                enforce_detection=False
            )

            return result[0]["dominant_emotion"]

        except:

            return "neutral"