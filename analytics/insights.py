def generate_insight(emotion, engagement):

    if engagement == "High":
        return "Participant highly aligned cognitively."

    if emotion == "sad":
        return "Possible disengagement detected."

    if emotion == "neutral":
        return "Low emotional response."

    return "Moderate engagement."