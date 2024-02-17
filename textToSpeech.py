import pyttsx3
engine = pyttsx3.init()

def speak_text(text):
    engine.say(text) # don't use the wait method, nukes the program
    return

