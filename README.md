## 🏫 Academic Context

[![FASTAPI](https://img.shields.io/badge/FASTAPI-%23009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![STREAMLIT](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PYTHON](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**Student Status:** Computer Science Student (3rd-Year Licence)  
**Context:** Personal side project built alongside undergraduate studies to explore practical automation and voice interfaces.  
**Objective:** Building a lightweight, voice-assisted attendance tool that automates roll-call using speech-to-text (STT) and text-to-speech (TTS), integrated with a FastAPI backend and a Streamlit dashboard.

---

## 📖 Repository Overview

This repository provides a simple, hands-on solution for university roll-call. Instead of manual data entry, the system reads student names aloud via speech synthesis, listens for oral responses through the microphone, and updates attendance status dynamically in a local interface.

🧠 Core Features
1. **Voice Roll-Call Automation**
   * **Speech Recognition:** Configured using Python's `speech_recognition` library and Google Speech API (supporting French-Algerian accents `fr-DZ`) to capture "Present" or "Absent" responses.
   * **Vocal Prompts:** Uses Text-to-Speech (`gTTS`) to call out student names sequentially.

2. **Hybrid Client-Server Architecture**
   * **FastAPI Backend (`PresenceTracker.py`):** Handles student records, microphone listening loops, and verification logic via REST endpoints.
   * **Streamlit Frontend (`app.py`):** Provides an interactive web dashboard with toggleable manual/automatic modes, live summary metrics, and data export.

## 🛠️ Technical Summary

| File / Endpoint | Technology | Description |
| :--- | :--- | :--- |
| `POST /verify` | FastAPI, SpeechRecognition | Triggers the audio prompt for a student, listens to the microphone, and returns the status. |
| `GET /students` | FastAPI | Serves the mock student list to the frontend interface. |
| `app.py` | Streamlit, Pandas | Renders the interactive table, statistics metrics, and triggers API verification requests. |

## 🚀 Getting Started

1. Start the FastAPI backend:
   ```bash
   uvicorn main:app --reload
   
