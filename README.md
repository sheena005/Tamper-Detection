# 🔐 Evidence-Grade Tamper Detection System

A digital forensic system to detect **partial tampering** in images, videos, audio, and files using **Merkle Trees and adaptive hashing**.

---

## 🚀 Setup Instructions

Follow these steps to run the project locally.

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/sheena005/Tamper-Detection.git
cd Tamper-Detection

python3 -m venv venv
source venv/bin/activate

python -m venv venv
venv\Scripts\activate

pip install streamlit opencv-python librosa pillow matplotlib reportlab blake3

streamlit run app.py
