#pip install pyautogui
#pip install sounddevice
#pip install numpy
#pip install pyobjc-framework-Quartz  # Required for pyautogui on macOS
#pip install pyobjc-framework-CoreAudio  # Required for sounddevice on macOS
#pip install ctypes
#pip install clint


import pyautogui
import sounddevice as sd
import numpy as np
import ctypes
from clint.textui import colored

ctypes.windll.kernel32.SetConsoleTitleW("VTC (VoiceToClick) by kramel")


audio_threshold_input = input("Enter audio threshold (recommended is 1): ")
if audio_threshold_input:
    audio_threshold = float(audio_threshold_input)
else:
    audio_threshold = 1


click_duration_input = input("Enter click duration in seconds (recommended is 0.05): ")
if click_duration_input:
    click_duration = float(click_duration_input)
else:
    click_duration = 0.05



clicking = False

print(f" audio threshold - {audio_threshold}")

print(f" click duration - {click_duration}")
print("")

print(colored.green("running!"))

def start_clicking():
    global clicking
    clicking = True
    pyautogui.mouseDown()
    print("clicked")

def stop_clicking():
    global clicking
    clicking = False
    pyautogui.mouseUp()

def callback(indata, frames, time, status):
    global clicking
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > audio_threshold:
        if not clicking:
            start_clicking()
    else:
        if clicking:
            stop_clicking()

stream = sd.InputStream(callback=callback, latency='low', channels=1)
stream.start()

try:
    while True:
        sd.sleep(10)
except KeyboardInterrupt:
    pass
finally:
    stream.stop()
    stream.close()
