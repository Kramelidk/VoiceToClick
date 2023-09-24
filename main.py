#pip install pyautogui
#pip install sounddevice
#pip install numpy
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

clicking = False
screaming = False

print(f" audio threshold - {audio_threshold}\n")

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
    print("released")

def callback(indata, frames, time, status):
    global clicking, screaming
    volume_norm = np.linalg.norm(indata) * 10
    if volume_norm > audio_threshold:
        if not screaming:
            screaming = True
            start_clicking()
    else:
        if screaming:
            screaming = False
            stop_clicking()

stream = sd.InputStream(callback=callback, latency='low', channels=1)
stream.start()

try:
    while True:
        sd.sleep(10)
except KeyboardInterrupt:
    pass
finally:
    if screaming:
        stop_clicking()
    stream.stop()
    stream.close()
