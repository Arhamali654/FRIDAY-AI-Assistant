import subprocess
import time
import pyautogui
import pyperclip

# Open notepad
subprocess.Popen("notepad.exe")
time.sleep(2.5)

# Click in the middle of screen to focus notepad
pyautogui.click(400, 400)
time.sleep(0.5)

# Method 1: Use clipboard paste instead of typewrite
text = "Hello World from FRIDAY"
pyperclip.copy(text)
pyautogui.hotkey("ctrl", "v")
time.sleep(0.5)

print("Done! Check Notepad.")
