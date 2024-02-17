import keyboard
import pyautogui
import os
import imageProcessing
import textToSpeech

def chrome_command(event):
    if event.name == 'new_tab': 
        print('new_tab')
        # keyboard.press('ctrl+t')
        # keyboard.release('ctrl+t')
    elif event.name == 'close_tab':
        print('close_tab')
        # keyboard.press('ctrl+w')
        # keyboard.release('ctrl+w')
    elif event.name == 'new_window':
        print('new_window')
        # keyboard.press('ctrl+n')
        # keyboard.release('ctrl+n')
    elif event.name == 'close_window':
        print('close_window')
        # keyboard.press('ctrl+shift+w')
        # keyboard.release('ctrl+shift+w')
    elif event.name == "p":
        print("screenshot")
        take_screenshot()

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

    # generate text from screenshot + 
    text = imageProcessing.generate_text("hacktcnj2024", "screenshots/screenshot.jpg")
    print(text)
    textToSpeech.speak_text(text)

keyboard.on_press(chrome_command)
print("waiting for next command...")

# Keep the program running until esc
keyboard.wait('esc')  # Press 'esc' to exit the program