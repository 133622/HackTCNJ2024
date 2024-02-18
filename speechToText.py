import speech_recognition as sr
from textblob import TextBlob

r = sr.Recognizer()
m = sr.Microphone()

def record_text():
    with m as source:
        r.adjust_for_ambient_noise(source=source)
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=3)
        try:
            text = r.recognize_google(audio, language = 'en-IN', show_all = True)
            print(text['alternative'][0]['transcript'])
            return text['alternative'][0]['transcript']
        except sr.UnknownValueError:
            t = "Google Speech Recognition could not understand audio"
            print(t)
            return t
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service: {e}")
            return "Could not request results from Google Speech Recognition service: {e}"
        except Exception as e:
            print(f"A terrible error has occurred: {e}")
            return "A terrible error has occurred: {e}"

# record_text() 
# function to get polarity of text (>0.4 is positive sentiment (yes), <0.5 is negative (no))
def get_polarity(answer):
    print("User response", answer)
    blob = TextBlob(answer)

    # used to artificially inflate polarity because sentiment not always accurate
    positive_words = {"yes", "sure", "okay", "please"}
    polarity = blob.sentiment.polarity
    if any(positive_words in answer for positive_words in positive_words):
        polarity += 0.5

    print("polarity: ", polarity)
    return polarity

# record_text()
# print(get_polarity("no"))