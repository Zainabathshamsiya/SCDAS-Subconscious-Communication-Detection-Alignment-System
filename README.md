# 🎥 SCDAS – Smart Cognitive & Dynamic Analysis System

SCDAS (Smart Cognitive & Dynamic Analysis System) is a **real-time multimodal analysis system** that combines **facial expression analysis, voice analysis, and engagement metrics** using webcam and microphone input.

The system is designed to analyze **human emotional state, stress level, and engagement** in real time, making it suitable for applications such as **online interviews, virtual classrooms, mental state monitoring, and human–computer interaction research**.

---

## 🚀 Features

* 🎭 **Facial Emotion Analysis**

  * Face detection via webcam
  * Micro-expression estimation
  * Emotion confidence percentage

* 🎤 **Voice Analysis**

  * Live audio recording
  * Pitch detection (Hz)
  * Voice energy analysis
  * Stress indicator based on vocal features

* 📊 **Cognitive Metrics**

  * Engagement score
  * Stress level classification
  * Overall alert level

* 🖥️ **Live Webcam Interface**

  * Real-time video feed
  * On-screen overlays for emotion, stress, and engagement
  * Voice energy bar visualization

---

## 🧠 System Architecture

```
project_scdas/
│
├── main.py
├── requirements.txt
│
├── core/
│   ├── scdas_system.py        # Central system controller
│   ├── caai_calculator.py     # Cognitive & alert index calculation
│
├── vision/
│   ├── face_detector.py
│   ├── gaze_tracker.py
│   └── micro_expression.py
│
├── audio/
│   └── vocal_analyzer.py
│
└── demos/
    ├── demo_realtime.py       # Live webcam + mic demo
    └── demo_single_frame.py   # Single-frame analysis
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/SCDAS.git
cd project_scdas
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the main program:

```bash
python main.py
```

You will be prompted to choose:

```
1. Real-time Demo
2. Single Frame Demo
```

### 🔴 Real-time Demo

* Opens webcam
* Performs live facial and voice analysis
* Displays engagement, stress, and emotion metrics on screen

### 🖼️ Single Frame Demo

* Processes a single frame
* Outputs calculated CAAI, alert level, and participant count

---

## 📈 Sample Output

```
CAAI: 0.500
Alert Level: Medium
Participants: 0
Emotion Confidence: 72%
Stress Level: Moderate
Engagement Score: 0.63
```

---

## 🧪 Technologies Used

* **Python 3**
* **OpenCV** – Computer Vision
* **NumPy / SciPy** – Signal Processing
* **SoundDevice / Librosa** – Audio Analysis
* **Machine Learning Concepts** – Emotion & stress estimation

---

## 🎯 Applications

* Online interview monitoring
* Virtual classroom engagement tracking
* Behavioral research
* Human–AI interaction systems
* Mental state analysis tools

---

## 📌 Project Status

✔️ Functional prototype
✔️ Real-time webcam & audio integration
🚧 Future improvements planned:

* Deep learning–based emotion models
* Multi-person tracking
* Web-based dashboard

---

## 👩‍💻 Author

**Saniya Naaz Ammu**
Final Year AI Engineering Student

📫 Feel free to connect on **LinkedIn** and explore the project on **GitHub**!

---

⭐ *If you like this project, don’t forget to star the repository!*
