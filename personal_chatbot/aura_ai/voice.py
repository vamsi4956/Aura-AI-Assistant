import speech_recognition as sr
import pyttsx3

# Initialize the Voice Engine
engine = pyttsx3.init()
engine.setProperty('rate', 180) 

def speak(text):
    print(f"Aura: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            # Increased timeout for better stability during demo
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            query = r.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except Exception as e:
            # If it doesn't hear anything, return empty string
            return ""