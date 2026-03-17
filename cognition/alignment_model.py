class CognitiveAlignment:

    def compute(self, emotion, gaze):

        score = 0

        if gaze == "focused":
            score += 50

        if emotion in ["happy","surprise"]:
            score += 30

        if emotion == "neutral":
            score += 20

        return score