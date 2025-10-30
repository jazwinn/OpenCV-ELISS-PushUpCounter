# ELISS Push-Up Counter

A Push-Up assistant inspired by Singapore's ELISS machine, built using **YOLO pose estimation**, **OpenCV**, and custom **biomechanics logic**. The system detects exercise form, evaluates posture angles, plays real-time correction audio cues, and automatically counts reps only when proper form is held.

---
### 🎥 Demo


https://github.com/user-attachments/assets/98ad50d7-28ff-4856-a285-697db160502b






---

## 🚀 Features

* Real‑time pose detection
* Detects shoulder, hip, ankle alignment
* Checks body straightness & leg straightness
* Rep counting based on correct form
* Asynchronous audio feedback cues
* Designed for gym/fitness AI applications

---

## 🧠 Tech Stack

| Component       | Technology                          |
| --------------- | ----------------------------------- |
| Pose Estimation | YOLO‑Pose (YOLO11n)                 |
| Vision          | OpenCV                              |
| Math            | NumPy                               |
| Logic           | Python, angle geometry & thresholds |

---

## ✅ Core Concepts

### Posture Checks

* Body straightness (shoulder‑hip‑ankle angle)
* Leg straightness
* Arm compression & confidence
* Angle to floor (gravity reference)

### Rep Logic
A rep only counts when:

1. Arm compression detected
2. Body straight
3. Leg straight
4. **All held simultaneously** ✔️

## 🏋️‍♂️ Ideal Use Cases

* Fitness coaching apps
* Form‑aware rep counters
* Rehab / physiotherapy assistance
* Smart mirror training systems

---

## 📦 Future Improvements
* Improve detection accuracy
* Add moving average smoothing for angles
* Multi‑exercise support
* Realtime coach voice prompts
* Mobile support
* GUI dashboards
---
