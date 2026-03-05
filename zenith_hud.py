import customtkinter as ctk
import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
import os
import datetime
import psutil
import asyncio
import edge_tts
from playsound import playsound


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
# GUI SETUP
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

app.title("ZENITH AI")

app.geometry("700x500")


title = ctk.CTkLabel(
    app,
    text="ZENITH AI SYSTEM",
    font=("Arial",30)
)

title.pack(pady=20)


status_label = ctk.CTkLabel(
    app,
    text="STATUS: READY",
    font=("Arial",18)
)

status_label.pack(pady=10)


command_label = ctk.CTkLabel(
    app,
    text="COMMAND: ---",
    font=("Arial",16)
)

command_label.pack(pady=10)


response_label = ctk.CTkLabel(
    app,
    text="RESPONSE: ---",
    font=("Arial",16)
)

response_label.pack(pady=10)


system_label = ctk.CTkLabel(
    app,
    text="CPU: --   RAM: --",
    font=("Arial",14)
)

system_label.pack(pady=20)


# =========================
# AUDIO RECORDING
# =========================

def record_audio(duration=4, fs=44100):

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
# LISTEN FUNCTION
# =========================

def listen():

    status_label.configure(text="STATUS: LISTENING")

    r = sr.Recognizer()

    audio_file = record_audio()

    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    try:

        command = r.recognize_google(audio).lower()

        command_label.configure(text="COMMAND: " + command)

        execute_command(command)

    except:

        response_label.configure(text="RESPONSE: Could not understand")

        speak("I could not understand")

    status_label.configure(text="STATUS: READY")


# =========================
# COMMAND SYSTEM
# =========================

def execute_command(command):

    if "hello" in command:

        response = "Hello Yoghesh"

        response_label.configure(text="RESPONSE: " + response)

        speak(response)


    elif "time" in command:

        now = datetime.datetime.now().strftime("%I:%M %p")

        response = "The current time is " + now

        response_label.configure(text="RESPONSE: " + response)

        speak(response)


    elif "open youtube" in command:

        os.system("start https://www.youtube.com")

        response = "Opening YouTube"

        response_label.configure(text="RESPONSE: " + response)

        speak(response)


    elif "open notepad" in command:

        os.system("notepad")

        response = "Opening Notepad"

        response_label.configure(text="RESPONSE: " + response)

        speak(response)


    else:

        response = "I am still learning that command"

        response_label.configure(text="RESPONSE: " + response)

        speak(response)


# =========================
# SYSTEM MONITOR
# =========================

def update_system():

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    system_label.configure(
        text=f"CPU: {cpu}%   RAM: {ram}%"
    )

    app.after(1000, update_system)


update_system()


# =========================
# MICROPHONE BUTTON
# =========================

listen_button = ctk.CTkButton(
    app,
    text="🎤 ACTIVATE ZENITH",
    command=listen,
    height=50,
    width=200
)

listen_button.pack(pady=20)


app.mainloop()