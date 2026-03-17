class CAAIIndex:

    def __init__(self):
        self.emotion_weight = 0.4
        self.gaze_weight = 0.3
        self.engagement_weight = 0.3

    # Emotion scoring
    def emotion_score(self, emotion):

        scores = {
            "happy": 1.0,
            "surprise": 0.9,
            "neutral": 0.7,
            "sad": 0.3,
            "angry": 0.2,
            "fear": 0.2,
            "disgust": 0.2
        }

        return scores.get(emotion.lower(), 0.5)

    # Gaze scoring
    def gaze_score(self, gaze):

        if gaze == "center":
            return 1.0
        elif gaze in ["left", "right"]:
            return 0.6
        else:
            return 0.3

    # Final CAAI computation
    def engagement_score(self, engagement):

    # Convert text → numeric
        mapping = {
            "high": 1.0,
            "medium": 0.7,
            "low": 0.3
        }

    # If already numeric
        if isinstance(engagement, (int, float)):
            return engagement if engagement <= 1 else engagement / 100

        return mapping.get(str(engagement).lower(), 0.5)


    def compute(self, emotion, gaze, engagement):

        e = self.emotion_score(emotion)
        g = self.gaze_score(gaze)
        eng = self.engagement_score(engagement)

        caai = (
            (e * self.emotion_weight) +
            (g * self.gaze_weight) +
            (eng * self.engagement_weight)
        )

        return round(caai, 2)