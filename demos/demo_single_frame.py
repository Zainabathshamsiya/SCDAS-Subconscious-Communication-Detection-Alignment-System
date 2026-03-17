import cv2
import time
from core.scdas_system import SCDASSystem

def demo_single_frame():
    print("Running Single Frame Demo...")

    system = SCDASSystem()

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to capture frame")
        return

    # ✅ CORRECT CALL (NO audio_chunk)
    group_state = system.process_frame(frame, time.time())

    print(f"\nCAAI: {group_state.caai:.3f}")
    print(f"Alert Level: {group_state.alert_level}")
    print(f"Participants: {len(group_state.participants)}")

    for p in group_state.participants:
        print(f"\nParticipant {p.participant_id}")
        print(f"Alignment Score: {p.alignment_score:.3f}")
        print(f"Expression: {p.micro_expression}")
        print(f"Voice Energy: {p.energy:.4f}")
