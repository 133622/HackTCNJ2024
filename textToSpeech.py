import pyttsx3

def init_engine():
    engine = pyttsx3.init()
    engine.setProperty( "rate", 200 )
    engine.setProperty( "volume", 1.0 )
    return engine

# engine.setProperty('voice', voices[1].id)

def speak_text(text):
    engine = init_engine()
    engine.say(text) # don't use the wait method, nukes the program
    engine.runAndWait()
    return

def prompt_user():
    engine = init_engine()
    engine.say("Would you like to learn more?")
    engine.runAndWait()
    return

