import os
import unicodedata
import speech_recognition as sr
from gtts import gTTS



students = [
  { "id": 1, "first_name": "Karim", "last_name": "Benali", "gender": "M", "wilaya": "Alger", "presence": [] },
  { "id": 2, "first_name": "Amel", "last_name": "Rahmani", "gender": "F", "wilaya": "Oran", "presence": [] },
  { "id": 3, "first_name": "Ahmed", "last_name": "Bouaziz", "gender": "M", "wilaya": "Constantine", "presence": [] },
  { "id": 4, "first_name": "Nadia", "last_name": "Bensalem", "gender": "F", "wilaya": "Annaba", "presence": [] },
  { "id": 5, "first_name": "Sofiane", "last_name": "Mansouri", "gender": "M", "wilaya": "Tlemcen", "presence": [] },
  { "id": 6, "first_name": "Yasmine", "last_name": "Khelifi", "gender": "F", "wilaya": "Batna", "presence": [] },
  { "id": 7, "first_name": "Rachid", "last_name": "Belkacem", "gender": "M", "wilaya": "Sétif", "presence": [] },
  { "id": 8, "first_name": "Leila", "last_name": "Boudiaf", "gender": "F", "wilaya": "Tizi Ouzou", "presence": [] },
]


# 1- Function to normalize text for comparison
def normalize(text):
    text = text.lower()
    return "".join(
        c
        for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )

def speak(text):
    tts = gTTS(text=text, lang="fr")
    tts.save("temp_audio.mp3")
    os.system("start temp_audio.mp3") 
    os.remove("temp_audio.mp3")



# 2- Verify the presence of students based on audio input.
def verify_presence(audio_bytes, df_students):
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8

    with sr.AudioFile(audio_bytes) as source:
        audio_data = recognizer.record(source)

    try:
        transcript = recognizer.recognize_google(audio_data, language="fr-algeria")
    except sr.UnknownValueError:
        speak("I couldn't understand what you said.")
        return "", ["Not Marked"] * len(df_students)
    except sr.RequestError as e:
        raise RuntimeError(f"Erreur du service Google Speech : {e}")

    text = normalize(transcript)
    statuses = []

    for _, student in df_students.iterrows():
        first = normalize(str(student["first_name"]))
        last = normalize(str(student["last_name"]))
        full = f"{first} {last}"

        pos = text.find(full)
        if pos == -1:
            pos = text.find(last)
        if pos == -1:
            pos = text.find(first)

        if pos != -1:
            window = text[pos : pos + len(full) + 15]
            if any(w in window for w in ["absent", "absente", "non", "no"]):
                statuses.append("Absent")
            elif any(w in window for w in ["present", "presente", "oui", "ici", "yes", "here"]):
                statuses.append("Present")
            else:
                statuses.append("Not Marked")
        else:
            statuses.append("Not Marked")

    return transcript, statuses


