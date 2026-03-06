import cv2
import sounddevice as sd
import os
import datetime
import queue
import json
from vosk import Model, KaldiRecognizer
import pyttsx3


# =========================
# VOICE SYSTEM
# =========================

engine = pyttsx3.init('sapi5')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)   # male voice
engine.setProperty('rate', 170)


def speak(text):

    print("Zenith:", text)

    engine.say(text)
    engine.runAndWait()


# =========================
# LOAD VOSK MODEL
# =========================

print("Loading voice recognition model...")

model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)


# =========================
# LISTEN SYSTEM
# =========================

def listen():

    q = queue.Queue()

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):

        while True:

            data = q.get()

            if recognizer.AcceptWaveform(data):

                result = json.loads(recognizer.Result())

                command = result.get("text")

                if command != "":
                    print("You said:", command)
                    return command


# =========================
# WAKE WORD SYSTEM
# =========================

def wake_word():

    while True:

        command = listen().lower()

        if "zenith" in command:

            speak("Yes Sir")

            # conversation mode
            while True:

                command = listen().lower()

                if "stop listening" in command or "go to sleep" in command:

                    speak("Going back to standby")

                    break

                execute_command(command)


# =========================
# FACE RECOGNITION
# =========================

def recognize_face():

    recognizer_face = cv2.face.LBPHFaceRecognizer_create()
    recognizer_face.read("face_model.yml")

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            label, confidence = recognizer_face.predict(face)

            print("Confidence:", confidence)

            if confidence < 40:

                cap.release()
                cv2.destroyAllWindows()

                return "yoghesh"

            else:

                cap.release()
                cv2.destroyAllWindows()

                return "unknown"

        cv2.imshow("Zenith Face Scan", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return "unknown"


# =========================
# COMMAND SYSTEM
# =========================

def execute_command(command):

    if "hello" in command:

        speak("Hello Yoghesh")

    elif "time" in command:

        now = datetime.datetime.now().strftime("%I:%M %p")

        speak("The time is " + now)

    elif "open youtube" in command:

        speak("Opening YouTube")

        os.system("start https://www.youtube.com")

    elif "open notepad" in command:

        speak("Opening Notepad")

        os.system("notepad")

    else:

        speak("I am still learning that command")


# =========================
# START SYSTEM
# =========================

print("Starting Zenith Vision System...")

person = recognize_face()

if person == "yoghesh":

    speak("Welcome back Sir")

    wake_word()

else:

    speak("Unauthorized user detected. Shutting down system.")