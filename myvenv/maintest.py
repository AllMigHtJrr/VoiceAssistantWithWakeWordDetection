import os
import pyaudio
import wave
import vosk
import json

# Set the wake word you want
WAKE_WORD = "assistant"

# Initialize vosk model
model = vosk.Model("C:\\B.Tech Files\\Asoca\\WW Voice Assistant\\myvenv\\vosk-model-small-en-us-0.15")  # Download the Vosk model from https://alphacephei.com/vosk/models
rec = vosk.KaldiRecognizer(model, 16000)

# Microphone setup
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000)
stream.start_stream()

# Function to process incoming audio and detect the wake word
def listen_for_wake_word():
    print("Listening for the wake word...")
    while True:
        data = stream.read(4000)
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result_json = json.loads(result)
            text = result_json.get("text", "")
            print(f"Recognized: {text}")
            if WAKE_WORD in text.lower():
                print("Wake word detected! Ready for your commands.")
                return True

# Dictionary-based response function
def respond_to_query(query):
    query = query.lower()
    if query in qa_dict:
        return qa_dict[query]
    else:
        return "Sorry, I don't know the answer to that."

# Main loop
if __name__ == "__main__":
    while True:
        if listen_for_wake_word():
            print("Please ask your question.")
            # Capture question after detecting the wake word
            while True:
                data = stream.read(4000)
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    result_json = json.loads(result)
                    query = result_json.get("text", "")
                    print(f"Query: {query}")
                    if query:
                        answer = respond_to_query(query)
                        print(f"Answer: {answer}")
                        break
