import cv2
import customtkinter as ctk
import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
import asyncio
import edge_tts
from playsound import playsound
import os
import datetime
import sys


# =========================
# VOICE SYSTEM
# =========================

async def speak_async(text):

    communicate = edge_tts.Communicate(
        text,
        voice="en-GB-RyanNeural"
    )

    await communicate.save("voice.mp3")

    playsound("voice.mp3")

    if os.path.exists("voice.mp3"):
        os.remove("voice.mp3")


def speak(text):
    asyncio.run(speak_async(text))


# =========================
# FACE RECOGNITION
# =========================

def recognize_face():

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("face_model.yml")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cam = cv2.VideoCapture(0)

    while True:

        ret, frame = cam.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            face = gray[y:y+h, x:x+w]

            label, confidence = recognizer.predict(face)

            if confidence < 70:

                cam.release()
                cv2.destroyAllWindows()

                return "yoghesh"

            else:

                cam.release()
                cv2.destroyAllWindows()

                return "unknown"

        cv2.imshow("Zenith Face Scan", frame)

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    return "unknown"


# =========================
# AUDIO RECORDING
# =========================

def record_audio(duration=5, fs=44100):

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    wav.write("input.wav", fs, recording)

    return "input.wav"


def listen():

    r = sr.Recognizer()

    audio_file = record_audio()

    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    try:

        command = r.recognize_google(audio, language="en-IN").lower()

        output_label.configure(text="Command: " + command)

        execute_command(command)

    except:

        output_label.configure(text="Could not understand")


# =========================
# COMMAND SYSTEM
# =========================

def execute_command(command):

    if "hello" in command:

        speak("Hello Yoghesh")
        output_label.configure(text="Response: Hello Yoghesh")

    elif "time" in command:

        now = datetime.datetime.now().strftime("%I:%M %p")

        speak("The current time is " + now)
        output_label.configure(text="Response: Time is " + now)

    elif "open youtube" in command:

        speak("Opening YouTube")

        os.system("start https://www.youtube.com")

        output_label.configure(text="Response: Opening YouTube")

    elif "open notepad" in command:

        speak("Opening Notepad")

        os.system("notepad")

        output_label.configure(text="Response: Opening Notepad")

    else:

        speak("I am still learning that command")
        output_label.configure(text="Unknown command")


# =========================
# ZENITH GUI
# =========================

def start_interface():

    global output_label

    ctk.set_appearance_mode("dark")

    app = ctk.CTk()

    app.title("ZENITH AI")

    app.geometry("500x400")


    title = ctk.CTkLabel(
        app,
        text="ZENITH AI",
        font=("Arial",30)
    )

    title.pack(pady=20)


    output_label = ctk.CTkLabel(
        app,
        text="System Ready",
        font=("Arial",18)
    )

    output_label.pack(pady=20)


    button = ctk.CTkButton(
        app,
        text="🎤 Speak Command",
        command=listen,
        height=40,
        width=200
    )

    button.pack(pady=20)


    app.mainloop()


# =========================
# START SYSTEM
# =========================

print("Starting Zenith Vision System...")

person = recognize_face()

if person == "yoghesh":

    speak("Welcome back Yoghesh")

    start_interface()

else:

    speak("Unauthorized user detected. Shutting down system.")

    sys.exit()