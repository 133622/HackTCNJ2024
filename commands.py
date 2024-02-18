import keyboard
import pyautogui
import os
import imageProcessing
import textToSpeech
import speechToText
import webbrowser
import time

application_name = "desktop" # store the name of the application that is currently open
active_window = False # flag to check if focus is on browser window

def browser_command(event):
    if (active_window == True):
        if event.name == 'new_tab': 
            print('Browser: new_tab')
            # keyboard.press('ctrl+t')
            # keyboard.release('ctrl+t')
        elif event.name == 'close_tab':
            print('Browsser: close_tab')
            # keyboard.press('ctrl+w')
            # keyboard.release('ctrl+w')
        elif event.name == 'new_window':
            print('Browser: new_window')
            # keyboard.press('ctrl+n')
            # keyboard.release('ctrl+n')
        elif event.name == 'close_window':
            print('Browswer: close_window')
            # keyboard.press('ctrl+shift+w')
            # keyboard.release('ctrl+shift+w')
    if (event.name == "p"):
        print("Action: Screenshot")
        take_screenshot()
        print("Action: Describe Image")
        describe_image()

def take_screenshot():
    file_names = os.listdir('screenshots')

    # clear screenshots folder before taking new screenshot
    for file_name in file_names:
        file_path = os.path.join('screenshots', file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # take screenshot & store in screenshots folder
    screenshot = pyautogui.screenshot()
    screenshot.save(f'screenshots/screenshot.jpg')

def describe_image():
    # generate text from screenshot + prompt user to learn more
    text, topic = imageProcessing.generate_text("hacktcnj2024", "screenshots/screenshot.jpg")
    print(text)
    textToSpeech.speak_text(text)
    print("prompting user")
    textToSpeech.prompt_user()

    answer = speechToText.get_polarity(speechToText.record_text())
    if (answer >= 0.4):
        response = "Great! I'm glad you're interested in learning more."
        search_google(topic)
    else:
        response = "That's okay, let me know if you change your mind."
    textToSpeech.speak_text(response)

def search_google(topic):
    url='https://www.google.com/search?q={}'.format(topic)
    webbrowser.open(url)
    application_name = "browser"
    time.sleep(2) # wait for 2 seconds; kinda bad
    active_window = True
    for i in range(0, 25):
        time.sleep(0.03)
        keyboard.press('tab')


# take_screenshot()
print("waiting for next command...")
keyboard.on_press(browser_command)


# # Keep the program running until esc
keyboard.wait('esc')  # Press 'esc' to exit the program