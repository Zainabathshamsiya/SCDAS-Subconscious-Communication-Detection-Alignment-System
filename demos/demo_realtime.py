import cv2
import time
from core.scdas_system import SCDASSystem


def demo_realtime():
    print("========================================")
    print(" SCDAS - LIVE WEBCAM ANALYSIS")
    print("========================================")
    print("Press 'Q' to quit")

    system = SCDASSystem()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


    if not cap.isOpened():
        print("❌ ERROR: Webcam not accessible")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # =========================
        # PROCESS FRAME
        # =========================
        group_state = system.process_frame(frame, time.time())

        # =========================
        # GLOBAL DISPLAY
        # =========================
        cv2.putText(
            frame,
            f"CAAI: {group_state.caai:.2f} | Alert: {group_state.alert_level.upper()}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

        # =========================
        # PER PARTICIPANT DISPLAY
        # =========================
        for p in group_state.participants:
            x, y, w, h = p.bbox

            # Face bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Emotion + confidence
            cv2.putText(
                frame,
                f"{p.micro_expression.upper()} ({p.emotion_confidence}%)",
                (x, y - 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            # Pitch + Stress
            stress_color = (0, 0, 255) if p.stress_level == "HIGH" else (0, 255, 0)
            cv2.putText(
                frame,
                f"Pitch: {p.pitch:.1f} Hz | Stress: {p.stress_level}",
                (x, y - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                stress_color,
                2
            )

            # =========================
            # VOICE ENERGY BAR
            # =========================
            bar_max_width = w
            bar_width = int(min(p.energy * 400, bar_max_width))

            cv2.rectangle(
                frame,
                (x, y + h + 5),
                (x + bar_width, y + h + 25),
                (0, 0, 255),
                -1
            )

            cv2.rectangle(
                frame,
                (x, y + h + 5),
                (x + w, y + h + 25),
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                "Voice Energy",
                (x, y + h + 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 255),
                1
            )

            # Engagement score
            cv2.putText(
                frame,
                f"Engagement: {p.engagement_score}",
                (x, y + h + 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 0),
                2
            )

        cv2.imshow("SCDAS - Live Webcam Analysis", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
