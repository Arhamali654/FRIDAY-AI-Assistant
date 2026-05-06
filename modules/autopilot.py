import pyautogui
import subprocess
import time
import os
import sys
import ctypes
import pyperclip
sys.path.insert(0, "F:\\JARVIS")

pyautogui.FAILSAFE = True
pyautogui.PAUSE    = 0.3

def type_text(text: str) -> str:
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.3)
    return f"Typed: {text}"

def click(x: int = None, y: int = None, button: str = "left") -> str:
    if x and y:
        pyautogui.click(x, y, button=button)
    else:
        pyautogui.click(button=button)
    return "Clicked."

def double_click(x: int = None, y: int = None) -> str:
    if x and y:
        pyautogui.doubleClick(x, y)
    else:
        pyautogui.doubleClick()
    return "Double clicked."

def right_click(x: int = None, y: int = None) -> str:
    if x and y:
        pyautogui.rightClick(x, y)
    else:
        pyautogui.rightClick()
    return "Right clicked."

def press_key(key: str) -> str:
    pyautogui.press(key)
    return f"Pressed {key}."

def hotkey(*keys) -> str:
    pyautogui.hotkey(*keys)
    return f"Pressed {' + '.join(keys)}."

def scroll(direction: str = "down", amount: int = 5) -> str:
    clicks = -amount if direction == "down" else amount
    pyautogui.scroll(clicks)
    return f"Scrolled {direction}."

def drag(x1: int, y1: int, x2: int, y2: int) -> str:
    pyautogui.drag(x1, y1, x2-x1, y2-y1, duration=0.5)
    return f"Dragged from {x1},{y1} to {x2},{y2}."

def find_and_click(text: str) -> str:
    try:
        import pytesseract
        from PIL import Image
        from config import TESSERACT_PATH
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        screenshot = pyautogui.screenshot()
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
        for i, word in enumerate(data["text"]):
            if text.lower() in word.lower() and int(data["conf"][i]) > 40:
                x = data["left"][i] + data["width"][i] // 2
                y = data["top"][i] + data["height"][i] // 2
                pyautogui.click(x, y)
                return f"Found and clicked '{text}'."
        return f"Could not find '{text}' on screen."
    except Exception as e:
        return f"Find and click error: {e}"

def switch_window(app_name: str) -> str:
    try:
        EnumWindows      = ctypes.windll.user32.EnumWindows
        EnumWindowsProc  = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText    = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLen = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible  = ctypes.windll.user32.IsWindowVisible
        SetForeground    = ctypes.windll.user32.SetForegroundWindow
        found_hwnd       = [None]

        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLen(hwnd)
                if length > 0:
                    buf = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buf, length + 1)
                    if app_name.lower() in buf.value.lower():
                        found_hwnd[0] = hwnd
                        return False
            return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)

        if found_hwnd[0]:
            ctypes.windll.user32.ShowWindow(found_hwnd[0], 9)
            SetForeground(found_hwnd[0])
            time.sleep(0.6)
            return f"Switched to {app_name}."
        return f"Could not find window: {app_name}"
    except Exception as e:
        return f"Window switch error: {e}"

def open_notepad_and_type(text: str) -> str:
    subprocess.Popen("notepad.exe")
    time.sleep(2.5)
    w, h = pyautogui.size()
    pyautogui.click(w // 2, h // 2)
    time.sleep(0.5)
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.3)
    return f"Opened Notepad and typed: {text}"

def open_app_and_type(app: str, text: str) -> str:
    result = switch_window(app)
    if "Could not find" in result:
        subprocess.Popen(["start", app], shell=True)
        time.sleep(2.5)
    w, h = pyautogui.size()
    pyautogui.click(w // 2, h // 2)
    time.sleep(0.5)
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")
    return f"Typed in {app}: {text}"

def open_browser_and_search(query: str) -> str:
    import webbrowser
    webbrowser.open(f"https://www.google.com/search?q={query}")
    time.sleep(2)
    return f"Searched Google for: {query}"

def copy_selected() -> str:
    pyautogui.hotkey("ctrl", "c")
    time.sleep(0.3)
    text = pyperclip.paste()
    return f"Copied: {text[:100]}" if text else "Copied selection."

def paste_text() -> str:
    pyautogui.hotkey("ctrl", "v")
    return "Pasted."

def select_all() -> str:
    pyautogui.hotkey("ctrl", "a")
    return "Selected all."

def save_file() -> str:
    pyautogui.hotkey("ctrl", "s")
    return "Saved file."

def close_window() -> str:
    pyautogui.hotkey("alt", "f4")
    return "Window closed."

def minimize_window() -> str:
    pyautogui.hotkey("win", "down")
    return "Window minimized."

def maximize_window() -> str:
    pyautogui.hotkey("win", "up")
    return "Window maximized."

def lock_screen() -> str:
    pyautogui.hotkey("win", "l")
    return "Screen locked."

def undo() -> str:
    pyautogui.hotkey("ctrl", "z")
    return "Undone."

def redo() -> str:
    pyautogui.hotkey("ctrl", "y")
    return "Redone."

def handle_autopilot_command(command: str) -> str:
    cmd = command.lower()

    if "notepad" in cmd and ("write" in cmd or "type" in cmd or "open" in cmd):
        text = (cmd.replace("open notepad and write", "")
                   .replace("open notepad and type", "")
                   .replace("write on notepad", "")
                   .replace("type on notepad", "")
                   .replace("write in notepad", "")
                   .replace("type in notepad", "")
                   .replace("notepad", "")
                   .replace("write", "")
                   .replace("type", "")
                   .strip())
        if not text:
            subprocess.Popen("notepad.exe")
            return "Opened Notepad."
        return open_notepad_and_type(text)

    elif "switch to" in cmd or "go to window" in cmd:
        app = cmd.replace("switch to", "").replace("go to window", "").strip()
        return switch_window(app)

    elif "click on" in cmd or "click the" in cmd:
        target = cmd.replace("click on", "").replace("click the", "").strip()
        return find_and_click(target)

    elif "type" in cmd or "write" in cmd:
        text = cmd.replace("type", "").replace("write", "").strip()
        return type_text(text)

    elif "scroll down" in cmd:
        return scroll("down", 5)

    elif "scroll up" in cmd:
        return scroll("up", 5)

    elif "press enter" in cmd:
        pyautogui.press("enter")
        return "Pressed Enter."

    elif "press escape" in cmd or "press esc" in cmd:
        pyautogui.press("escape")
        return "Pressed Escape."

    elif "press" in cmd:
        key = cmd.replace("press", "").strip()
        pyautogui.press(key)
        return f"Pressed {key}."

    elif "copy" in cmd:
        return copy_selected()

    elif "paste" in cmd:
        return paste_text()

    elif "select all" in cmd:
        return select_all()

    elif "save file" in cmd or "save this" in cmd:
        return save_file()

    elif "close window" in cmd or "close this" in cmd:
        return close_window()

    elif "minimize" in cmd:
        return minimize_window()

    elif "maximize" in cmd:
        return maximize_window()

    elif "lock screen" in cmd:
        return lock_screen()

    elif "undo" in cmd:
        return undo()

    elif "redo" in cmd:
        return redo()

    elif ("search google" in cmd or ("google" in cmd and "search" in cmd)):
        query = (cmd.replace("search google for", "")
                    .replace("search on google", "")
                    .replace("google", "")
                    .replace("search", "")
                    .replace("for", "")
                    .strip())
        return open_browser_and_search(query)

    else:
        return "I didn't understand that automation command. Try: open notepad and write hello, scroll down, click on search, press enter."
