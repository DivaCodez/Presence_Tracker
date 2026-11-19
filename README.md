# 🎙️ Smart Presence Tracker

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

A simple tool to speed up taking student attendance using voice recognition and a Streamlit interface.

## 💡 Motivation

Taking attendance manually takes time, especially with larger groups. I wanted to test if speaking the attendance list out loud and letting a script fill out the table could make the process faster while still letting the user review and edit the result.

## 🔄 What Changed From the First Version

* **First approach (one-by-one loop):** The initial version read each student's name out loud with text-to-speech (`gTTS`) and waited for a microphone reply after every name. In practice, this was too slow because of the delay between each prompt, and it froze the interface while running.
* **Current approach (single recording):** Instead of going student by student, you record one audio clip reading the list at your own pace (`st.audio_input`). The app transcribes the recording once, cleans the text (lowercase and no accents), and checks the words right after each student's name to mark them `Present` or `Absent`.

## 🧠 Features

* **Voice attendance:** Record a single audio clip in the browser and transcribe it with `SpeechRecognition` (French `fr-algeria`).
* **Name and status matching:** Normalizes text and looks near each student's name for keywords (`présent`, `absent`, `oui`, `non`).
* **Manual mode:** Lets you switch to an editable table (`st.data_editor`) to fix any missed or misheard names before saving.
* **Summary and CSV export:** Displays counts for `Total`, `Present`, `Absent`, and `Not Marked`, and saves the updated list to `temp_list.csv`.

## ⚠️ Limitations

* **Internet connection required:** Uses Google's free Speech-to-Text API (`recognize_google`), so transcription will not work offline.
* **Name spelling variations:** Exact substring matching can miss names if the speech recognizer spells them slightly differently than in the database (e.g., *Kawtar* vs *Kaoutar*, *Yacine* vs *Yassine*).
* **Duplicate first names:** If two students share the same first name and only the first name is spoken, the script matches the first occurrence in the list.
* **Background noise:** Accuracy drops in noisy classrooms if the microphone is far from the speaker.
* **Local CSV storage:** Attendance is saved to a local CSV file (`temp_list.csv`) rather than a persistent database.

## 🛠️ Files

| File | Description |
| :--- | :--- |
| `src/app.py` | Streamlit interface, audio input, manual/auto toggle, summary metrics, and CSV saving. |
| `src/main.py` | Audio transcription, text normalization, and matching logic. |

## 🚀 How to Use

1. Activate your virtual environment and start the app:
   ```bash
   source .venv/bin/activate
   streamlit run src/app.py
   ```
2. Record the attendance list, check the table (or adjust it in **Manual mode**), and click **Save**.
   
