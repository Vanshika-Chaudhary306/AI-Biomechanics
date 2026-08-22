# AI Biomechanics Coach 🏀⚽

An AI-powered sports mechanics coach that uses computer vision to provide real-time, zero-sensor athletic form analysis.

**Team:** Debug Divas  
**Track:** AI/ML & SportsTech

## 🚀 Overview
Athletes often lack access to professional coaching and precise biomechanical feedback. This project solves that by using markerless human pose estimation to convert standard video into structural biomechanical data. It tracks joints, calculates precise kinematic angles, and provides dynamic phase-based feedback overlaying the video.

## 🛠️ Tech Stack
* **Frontend UI:** Streamlit
* **AI/ML Model:** Ultralytics YOLOv8-pose
* **Computer Vision:** OpenCV
* **Language:** Python

## 🏃‍♀️ Features
* **Real-Time Joint Angle Tracking:** Automatically extracts coordinates (wrist/shoulder, hip/knee/ankle) to calculate angles.
* **Dynamic Phase Detection:** Evaluates the exact state of motion (e.g., Gather/Set Point/Release or Wind-up/Strike).
* **Visual Overlay:** Projects colored bounding lines and instantaneous text feedback directly onto the video feed.

## 💻 How to Run Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/Vanshika-Chaudhary306/AI-Biomechanics.git](https://github.com/Vanshika-Chaudhary306/AI-Biomechanics.git)
