import streamlit as st
import cv2
import numpy as np
import time
from collections import deque

from vision.face_detector import FaceDetector
from vision.emotion_detector import EmotionDetector
from vision.gaze_tracker import GazeTracker

from cognition.alignment_model import CognitiveAlignment
from cognition.engagement_model import EngagementModel
from cognition.caai_index import CAAIIndex

from analytics.charts import emotion_chart, engagement_gauge, timeline
from analytics.insights import generate_insight


# -----------------------
# CONFIG
# -----------------------

st.set_page_config(layout="wide")
st.title("🧠 CAAI Real-Time AI Dashboard")

start = st.button("▶ Start")
stop = st.button("⏹ Stop")

if "run" not in st.session_state:
    st.session_state.run = False

if start:
    st.session_state.run = True

if stop:
    st.session_state.run = False


# -----------------------
# MODELS
# -----------------------

face = FaceDetector()
emotion_model = EmotionDetector()
gaze_model = GazeTracker()

align = CognitiveAlignment()
eng_model = EngagementModel()
caai_model = CAAIIndex()


# -----------------------
# STATE
# -----------------------

if "emotion_counts" not in st.session_state:
    st.session_state.emotion_counts = {}

if "timeline_scores" not in st.session_state:
    st.session_state.timeline_scores = []

if "buffer" not in st.session_state:
    st.session_state.buffer = deque(maxlen=10)

if "frame_id" not in st.session_state:
    st.session_state.frame_id = 0


# -----------------------
# UI PLACEHOLDERS
# -----------------------

frame_placeholder = st.empty()

col1, col2 = st.columns(2)
emotion_placeholder = col1.empty()
gauge_placeholder = col2.empty()

timeline_placeholder = st.empty()
caai_placeholder = st.empty()
insight_placeholder = st.empty()


# -----------------------
# CAMERA
# -----------------------

cap = cv2.VideoCapture(0)


# -----------------------
# LOOP
# -----------------------

while st.session_state.run:

    ret, frame = cap.read()
    if not ret:
        st.error("Camera error")
        break

    st.session_state.frame_id += 1

    faces = face.detect(frame)

    score = 0
    caai_score = 0
    insight = "Analyzing..."

    for (x, y, w, h) in faces:

        face_img = frame[y:y+h, x:x+w]

        # Emotion
        emotion = emotion_model.detect(face_img)
        st.session_state.buffer.append(emotion)

        stable_emotion = max(
            set(st.session_state.buffer),
            key=st.session_state.buffer.count
        )

        # Gaze
        gaze = gaze_model.detect(frame)

        # Engagement
        score = align.compute(stable_emotion, gaze)
        engagement = eng_model.predict(score)

        # CAAI
        caai_score = caai_model.compute(
            stable_emotion, gaze, engagement
        )

        # Store
        st.session_state.timeline_scores.append(score)

        st.session_state.emotion_counts[stable_emotion] = \
            st.session_state.emotion_counts.get(stable_emotion, 0) + 1

        # Insight
        insight = generate_insight(stable_emotion, engagement)

        # Draw
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        cv2.putText(frame, stable_emotion, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.putText(frame, f"Eng: {engagement}", (x, y+h+25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)

        cv2.putText(frame, f"CAAI: {caai_score}", (x, y+h+50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

    # -----------------------
    # SHOW FRAME
    # -----------------------

    frame_placeholder.image(frame, channels="BGR")

    # -----------------------
    # DASHBOARD (SAFE UPDATE)
    # -----------------------

    if len(st.session_state.timeline_scores) > 10:

        emotion_placeholder.plotly_chart(
            emotion_chart(st.session_state.emotion_counts),
            width="stretch",
            key=f"emotion_{st.session_state.frame_id}"
        )

        gauge_placeholder.plotly_chart(
            engagement_gauge(score),
            width="stretch",
            key=f"gauge_{st.session_state.frame_id}"
        )

        timeline_placeholder.plotly_chart(
            timeline(st.session_state.timeline_scores),
            width="stretch",
            key=f"timeline_{st.session_state.frame_id}"
        )

        caai_placeholder.metric("🧠 CAAI Index", caai_score)

        insight_placeholder.subheader("🤖 AI Insight")
        insight_placeholder.write(insight)

    # FPS control
    time.sleep(0.03)


cap.release()