import time
from vision.face_detector import FaceDetector
from vision.micro_expression import MicroExpressionDetector
from vision.gaze_tracker import GazeTracker
from audio.vocal_analyzer import VocalAnalyzer
from core.caai_calculator import CAAICalculator


# =========================
# DATA CLASSES
# =========================

class Participant:
    def __init__(
        self,
        participant_id,
        bbox,
        micro_expression,
        emotion_confidence,
        energy,
        pitch,
        stress_level,
        engagement_score,
        alignment_score,
    ):
        self.participant_id = participant_id
        self.bbox = bbox                  # (x, y, w, h)
        self.micro_expression = micro_expression
        self.emotion_confidence = emotion_confidence  # %
        self.energy = energy
        self.pitch = pitch                # Hz
        self.stress_level = stress_level  # HIGH / NORMAL
        self.engagement_score = engagement_score
        self.alignment_score = alignment_score


class GroupState:
    def __init__(self, caai, participants, alert_level):
        self.caai = caai
        self.participants = participants
        self.alert_level = alert_level


# =========================
# MAIN SYSTEM
# =========================

class SCDASSystem:
    def __init__(self):
        self.face_detector = FaceDetector()
        self.micro_exp_detector = MicroExpressionDetector()
        self.gaze_tracker = GazeTracker()
        self.vocal_analyzer = VocalAnalyzer()
        self.caai_calculator = CAAICalculator()

    def process_frame(self, frame, timestamp):
        """
        Processes:
        - Live webcam frame
        - Live microphone audio
        Returns:
        - GroupState
        """

        # =========================
        # 🎤 LIVE AUDIO ANALYSIS
        # =========================
        audio_chunk = self.vocal_analyzer.record_audio(duration=0.5)
        audio_features = self.vocal_analyzer.extract_features(audio_chunk)

        voice_energy = audio_features.get("energy", 0.0)
        voice_pitch = audio_features.get("pitch", 0.0)

        # =========================
        # 👤 FACE DETECTION
        # =========================
        faces = self.face_detector.detect_faces(frame)
        participants = []

        for pid, (x, y, w, h) in faces:
            face_region = frame[y:y+h, x:x+w]
            if face_region.size == 0:
                continue

            # =========================
            # 🙂 MICRO-EXPRESSION + CONFIDENCE
            # =========================
            action_units = self.micro_exp_detector.extract_action_units(face_region)
            expression, confidence = self.micro_exp_detector.classify_expression(action_units)
            emotion_confidence = int(confidence * 100)

            # =========================
            # 😰 STRESS DETECTION
            # =========================
            stress_level = "NORMAL"
            if expression == "tension" or voice_energy > 0.08 or voice_pitch > 250:
                stress_level = "HIGH"

            # =========================
            # 🧠 ENGAGEMENT SCORE (0–1)
            # =========================
            engagement_score = 0.0

            if expression in ["neutral", "agreement"]:
                engagement_score += 0.4
            if 0.02 < voice_energy < 0.08:
                engagement_score += 0.3
            if 80 < voice_pitch < 250:
                engagement_score += 0.3

            engagement_score = round(min(engagement_score, 1.0), 2)

            # =========================
            # 🔗 ALIGNMENT SCORE
            # =========================
            alignment_score = 0.6
            if expression == "agreement":
                alignment_score = 0.8
            elif expression == "tension":
                alignment_score = 0.4
            elif expression == "doubt":
                alignment_score = 0.5

            participant = Participant(
                participant_id=pid,
                bbox=(x, y, w, h),
                micro_expression=expression,
                emotion_confidence=emotion_confidence,
                energy=voice_energy,
                pitch=voice_pitch,
                stress_level=stress_level,
                engagement_score=engagement_score,
                alignment_score=alignment_score,
            )

            participants.append(participant)

        # =========================
        # 📊 GROUP CAAI
        # =========================
        caai = self.caai_calculator.compute_group_caai(participants)

        if caai < 0.4:
            alert = "high"
        elif caai < 0.6:
            alert = "medium"
        else:
            alert = "low"

        return GroupState(caai, participants, alert)
