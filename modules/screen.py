import pyautogui
import pytesseract
import datetime
import os
import subprocess
from PIL import Image
import sys
sys.path.insert(0, "F:\\JARVIS")
from config import TESSERACT_PATH, JARVIS_NAME
from modules.brain import think

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def get_active_window_title() -> str:
    try:
        import ctypes
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value
    except:
        return "Unknown"

def get_all_open_windows() -> list:
    try:
        import ctypes
        import ctypes.wintypes
        titles = []
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible

        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                if length > 0:
                    buf = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buf, length + 1)
                    if buf.value.strip():
                        titles.append(buf.value.strip())
            return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)
        return titles
    except:
        return []

def capture_screen() -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(os.path.expanduser("~"), "Pictures", f"friday_screen_{timestamp}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(path)
    return path

def read_screen() -> str:
    try:
        active = get_active_window_title()
        path   = capture_screen()
        img    = Image.open(path)
        text   = pytesseract.image_to_string(img).strip()
        os.remove(path)

        if not text:
            return f"The active window is '{active}'. I can see your screen but there is no readable text right now."

        if len(text) > 800:
            text = text[:800] + "..."

        return f"Active window: {active}. Screen text: {text}"
    except Exception as e:
        return f"Screen reading error: {e}"

def describe_screen() -> str:
    try:
        active  = get_active_window_title()
        windows = get_all_open_windows()

        visible = [w for w in windows if len(w) > 3 and w not in ["NVIDIA GeForce Overlay", "Program Manager"]][:8]
        windows_str = ", ".join(visible) if visible else "none detected"

        path = capture_screen()
        img  = Image.open(path)
        text = pytesseract.image_to_string(img).strip()
        os.remove(path)

        if len(text) > 500:
            text = text[:500]

        prompt = (
            f"The user's currently active window is: '{active}'\n"
            f"Other open windows include: {windows_str}\n"
            f"OCR text from screen: {text[:300] if text else 'none'}\n\n"
            f"Based on this, describe what the user is currently doing in one or two sentences. "
            f"Focus on the ACTIVE window '{active}', not other windows. "
            f"Be concise and natural like FRIDAY from Iron Man."
        )
        return think(prompt)
    except Exception as e:
        return f"Screen description error: {e}"

def what_is_open() -> str:
    try:
        active  = get_active_window_title()
        windows = get_all_open_windows()
        visible = [w for w in windows if len(w) > 3 and
                   w not in ["NVIDIA GeForce Overlay", "Program Manager", "Windows Input Experience"]][:10]

        if not visible:
            return f"The active window is {active}."

        prompt = (
            f"Active window: '{active}'\n"
            f"All open windows: {', '.join(visible)}\n\n"
            f"Tell the user what apps they currently have open in a natural conversational way. "
            f"Mention the active app first. Keep it brief."
        )
        return think(prompt)
    except Exception as e:
        return f"Window detection error: {e}"

def answer_about_screen(question: str) -> str:
    try:
        active  = get_active_window_title()
        path    = capture_screen()
        img     = Image.open(path)
        text    = pytesseract.image_to_string(img).strip()
        os.remove(path)

        if len(text) > 500:
            text = text[:500]

        prompt = (
            f"User question: '{question}'\n"
            f"Active window: '{active}'\n"
            f"Screen text: {text if text else 'no text detected'}\n\n"
            f"Answer the question based on what is visible on screen. Be concise."
        )
        return think(prompt)
    except Exception as e:
        return f"Screen analysis error: {e}"

def find_on_screen(target: str) -> str:
    try:
        active = get_active_window_title()
        path   = capture_screen()
        img    = Image.open(path)
        text   = pytesseract.image_to_string(img).strip()
        os.remove(path)

        if target.lower() in text.lower() or target.lower() in active.lower():
            return f"Yes, I can see '{target}' on your screen."
        else:
            return f"I cannot find '{target}' on your screen right now. Active window is '{active}'."
    except Exception as e:
        return f"Search error: {e}"

def handle_screen_command(command: str) -> str:
    cmd = command.lower()

    if "what" in cmd and ("open" in cmd or "running" in cmd or "apps" in cmd):
        return what_is_open()
    elif "read" in cmd and "screen" in cmd:
        return read_screen()
    elif "describe" in cmd and "screen" in cmd:
        return describe_screen()
    elif "what" in cmd and "screen" in cmd:
        return describe_screen()
    elif "find" in cmd or ("see" in cmd and "screen" in cmd):
        target = cmd.replace("find", "").replace("on screen", "").replace("screen", "").replace("can you see", "").strip()
        if target:
            return find_on_screen(target)
        return describe_screen()
    else:
        return answer_about_screen(command)
