import os
import pyaudio
import vosk
import json
import pyttsx3
import difflib
import time

WAKE_WORD = "windows"
model = vosk.Model("C:\\B.Tech Files\\Asoca\\WW Voice Assistant\\myvenv\\vosk-model-small-en-us-0.15")
rec = vosk.KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
stream.start_stream()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
for i, voice in enumerate(voices):
    print(f"{i}: {voice.name} ({voice.id})")
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 160)

qa_dict = {
    "who are you": "I am a voice assistant for the magician's robot.",
    "what can you do": "I can assist the magician by answering questions, controlling robot actions, and more.",
    "how are you": "I'm just a program, but thanks for asking!",
    "perform magic": "I am unable to perform magic, but I can assist the magician in other ways.",
    "what is your name": "I don't have a personal name, but you can call me Assistant.",
    "tell a joke": "Why don’t skeletons fight each other? They don’t have the guts!",
    "goodbye": "Goodbye! Have a magical day!",
    "stop": "Stopping the assistant. See you soon!"
}

def get_closest_match(query):
    query = query.lower().strip()
    closest_match = difflib.get_close_matches(query, qa_dict.keys(), n=1, cutoff=0.6)
    return closest_match[0] if closest_match else None

def respond_to_query(query):
    matched = get_closest_match(query)
    return qa_dict.get(matched, "Sorry, I don't know the answer to that.")

def speak_response(response):
    engine.say(response)
    engine.runAndWait()

def listen_for_wake_word():
    print("Listening for the wake word...")
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "")
            print("Heard:", text)
            if WAKE_WORD in text.lower():
                print("Wake word detected!")
                return

def listen_for_command(timeout=5):
    print("Listening for a command...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "").strip()
            print("Recognized command:", text)
            if len(text.split()) < 2:
                print("Too short, maybe noise. Ignoring...")
                continue
            return text
    return ""

def main():
    while True:
        listen_for_wake_word()
        command = listen_for_command(timeout=6)
        if not command:
            print("No valid command heard. Going back to listening for wake word.")
            continue

        response = respond_to_query(command)
        print("Response:", response)
        speak_response(response)

        if command.lower() in ["stop", "goodbye"]:
            break

if __name__ == "__main__":
    main()
