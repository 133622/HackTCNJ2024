import speech_recognition as sr
from textblob import TextBlob

r = sr.Recognizer()

def record_text():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source=source)
        print("Listening...")
        audio = r.listen(source, timeout=3)
        try:
            text = r.recognize_google(audio, language = 'en-IN', show_all = True)
            print(text['alternative'][0]['transcript'])
            return text['alternative'][0]['transcript']
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
            return "Could not request results from Google Speech Recognition service: {e}"
        except Exception as e:
            print(f"A terrible error has occurred: {e}")
            return "A terrible error has occurred: {e}"

# record_text()
def get_polarity(answer):
    print("User response", answer)
    blob = TextBlob(answer)
    positive_words = {"yes", "sure", "okay", "please"}
    polarity = blob.sentiment.polarity
    if any(positive_words in answer for positive_words in positive_words):
        polarity += 0.5
    print("polarity: ", polarity)
    return polarity

# record_text()
# print(get_polarity("no"))