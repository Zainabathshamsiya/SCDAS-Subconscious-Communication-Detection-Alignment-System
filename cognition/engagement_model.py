class EngagementModel:

    def predict(self, score):

        if score > 70:
            return "High"

        if score > 40:
            return "Medium"

        return "Low"