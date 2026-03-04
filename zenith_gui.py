import customtkinter as ctk
import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
import asyncio
import edge_tts
from playsound import playsound
import os
import datetime


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
# RECORD AUDIO
# =========================

def record_audio(duration=5, fs=44100):

    status_label.configure(text="Status: Listening...")

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    wav.write("input.wav", fs, recording)

    return "input.wav"


# =========================
# SPEECH RECOGNITION
# =========================

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

        output_label.configure(text="Response: Command not recognized")


# =========================
# GUI
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("ZENITH AI")

app.geometry("500x400")


title = ctk.CTkLabel(
    app,
    text="ZENITH AI",
    font=("Arial",30)
)

title.pack(pady=20)


status_label = ctk.CTkLabel(
    app,
    text="Status: Idle",
    font=("Arial",18)
)

status_label.pack(pady=10)


output_label = ctk.CTkLabel(
    app,
    text="Command output will appear here",
    font=("Arial",16)
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