import librosa
import numpy as np

class VoiceAnalyzer:

    def analyze(self, audio):

        y, sr = librosa.load(audio)

        energy = np.mean(librosa.feature.rms(y=y))

        if energy > 0.1:
            return "energetic"

        return "calm"
