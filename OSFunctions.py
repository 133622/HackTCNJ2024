#Functions to control the OS
from AppOpener import open
from win32gui import GetWindowText, GetForegroundWindow
import pyautogui
pyautogui.FAILSAFE = False
x = 1

def increment_volume():
    pyautogui.press('volumeup')
    
def decrement_volume():
    pyautogui.press('volumedown')

def mute_volume():
    pyautogui.press('volumemute')

def get_currently_active_window():
    return GetWindowText(GetForegroundWindow())

def open_application(application_name: str):
    open(application_name, match_closest=True) # Opens Chrome



# Set the system volume
open_application('can you open chrome please')