import numpy as np
import sounddevice as sd

class VocalAnalyzer:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def record_audio(self, duration=0.5):
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
        return audio.flatten()

    def extract_features(self, audio_chunk):
        # Energy (RMS)
        energy = float(np.sqrt(np.mean(audio_chunk ** 2)))

        # Pitch (Autocorrelation)
        pitch = self._estimate_pitch(audio_chunk)

        return {
            "energy": energy,
            "pitch": pitch,
        }

    def _estimate_pitch(self, audio):
        audio = audio - np.mean(audio)
        corr = np.correlate(audio, audio, mode="full")
        corr = corr[len(corr)//2:]

        # Find first peak
        d = np.diff(corr)
        start = np.where(d > 0)[0]
        if len(start) == 0:
            return 0.0

        peak = start[0] + np.argmax(corr[start[0]:])
        if peak == 0:
            return 0.0

        pitch = self.sample_rate / peak
        return float(pitch)
