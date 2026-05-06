import subprocess
import os
import webbrowser
import pyautogui
import psutil
import datetime
from config import JARVIS_NAME

APPS = {
    "chrome":        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox":       r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "edge":          r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "microsoft edge":r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "notepad":       "notepad.exe",
    "calculator":    "calc.exe",
    "vs code":       r"C:\Users\arham\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "vscode":        r"C:\Users\arham\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "explorer":      "explorer.exe",
    "file explorer": "explorer.exe",
    "task manager":  "taskmgr.exe",
    "word":          r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel":         r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "powerpoint":    r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "vlc":           r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "spotify":       r"C:\Users\arham\AppData\Roaming\Spotify\Spotify.exe",
    "discord":       r"C:\Users\arham\AppData\Local\Discord\Update.exe",
    "telegram":      r"C:\Users\arham\AppData\Roaming\Telegram Desktop\Telegram.exe",
    "whatsapp":      r"C:\Users\arham\AppData\Local\WhatsApp\WhatsApp.exe",
    "paint":         "mspaint.exe",
    "cmd":           "cmd.exe",
    "command prompt":"cmd.exe",
}

WEBSITES = {
    "youtube":   "https://youtube.com",
    "google":    "https://google.com",
    "github":    "https://github.com",
    "facebook":  "https://facebook.com",
    "instagram": "https://instagram.com",
    "twitter":   "https://twitter.com",
    "whatsapp":  "https://web.whatsapp.com",
    "gmail":     "https://mail.google.com",
    "chatgpt":   "https://chat.openai.com",
    "netflix":   "https://netflix.com",
}

def open_app(app_name: str) -> str:
    name = app_name.lower().strip()
    for key, path in APPS.items():
        if key in name:
            try:
                subprocess.Popen(path)
                return f"Opening {key}."
            except FileNotFoundError:
                return f"Could not find {key}. Please check the path in system.py."
            except Exception as e:
                return f"Error opening {key}: {e}"
    return f"I don't know how to open {app_name}. You can add it to the APPS list in system.py."

def close_app(app_name: str) -> str:
    name = app_name.lower().strip()
    process_names = {
        "chrome":         "chrome.exe",
        "edge":           "msedge.exe",
        "microsoft edge": "msedge.exe",
        "firefox":        "firefox.exe",
        "notepad":        "notepad.exe",
        "calculator":     "calculator.exe",
        "vs code":        "Code.exe",
        "vscode":         "Code.exe",
        "vlc":            "vlc.exe",
        "spotify":        "Spotify.exe",
        "discord":        "Discord.exe",
        "telegram":       "Telegram.exe",
        "word":           "WINWORD.EXE",
        "excel":          "EXCEL.EXE",
        "powerpoint":     "POWERPNT.EXE",
        "task manager":   "Taskmgr.exe",
        "paint":          "mspaint.exe",
    }
    for key, process in process_names.items():
        if key in name:
            os.system(f"taskkill /f /im {process}")
            return f"Closed {key}."
    return f"Could not find {app_name} to close."

def open_website(site_name: str) -> str:
    name = site_name.lower().strip()
    for key, url in WEBSITES.items():
        if key in name:
            webbrowser.open(url)
            return f"Opening {key}."
    webbrowser.open(f"https://www.google.com/search?q={site_name}")
    return f"Searching for {site_name} on Google."

def search_web(query: str) -> str:
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Searching Google for: {query}"

def take_screenshot() -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(os.path.expanduser("~"), "Pictures", f"jarvis_{timestamp}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(path)
    return f"Screenshot saved to Pictures folder."

def get_system_stats() -> str:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('C:\\')
    ram_used = round(ram.used / (1024**3), 1)
    ram_total = round(ram.total / (1024**3), 1)
    disk_free = round(disk.free / (1024**3), 1)
    disk_total = round(disk.total / (1024**3), 1)
    return (
        f"CPU usage is {cpu} percent. "
        f"RAM is {ram_used} GB used out of {ram_total} GB. "
        f"C drive has {disk_free} GB free out of {disk_total} GB."
    )

def set_volume(level: str) -> str:
    if "up" in level or "increase" in level or "louder" in level:
        pyautogui.press("volumeup", presses=5)
        return "Volume increased."
    elif "down" in level or "decrease" in level or "lower" in level:
        pyautogui.press("volumedown", presses=5)
        return "Volume decreased."
    elif "mute" in level:
        pyautogui.press("volumemute")
        return "Volume muted."
    elif "unmute" in level:
        pyautogui.press("volumemute")
        return "Volume unmuted."
    return "Volume command not recognized."

def handle_system_command(command: str) -> str:
    cmd = command.lower()

    if "screenshot" in cmd or "capture screen" in cmd:
        return take_screenshot()

    elif "system" in cmd and ("stat" in cmd or "status" in cmd or "performance" in cmd):
        return get_system_stats()

    elif ("cpu" in cmd or "ram" in cmd) and ("usage" in cmd or "how much" in cmd):
        return get_system_stats()

    elif "volume" in cmd or "mute" in cmd or "unmute" in cmd:
        return set_volume(cmd)

    elif "search" in cmd:
        query = cmd.replace("search", "").replace("google", "").replace("on", "").replace("web", "").replace("internet", "").replace("for", "").strip()
        return search_web(query)

    elif "close" in cmd or "exit" in cmd or "kill" in cmd:
        app = cmd.replace("close", "").replace("exit", "").replace("kill", "").strip()
        return close_app(app)

    elif "open" in cmd or "launch" in cmd or "start" in cmd:
        for site in WEBSITES:
            if site in cmd:
                return open_website(site)
        app = cmd.replace("open", "").replace("launch", "").replace("start", "").strip()
        return open_app(app)

    elif "shutdown" in cmd or "shut down" in cmd:
        return "Say confirm shutdown to proceed."

    elif "confirm shutdown" in cmd:
        os.system("shutdown /s /t 5")
        return "Shutting down your PC in 5 seconds."

    elif "restart" in cmd:
        os.system("shutdown /r /t 5")
        return "Restarting your PC in 5 seconds."

    else:
        return f"System command not recognized: {command}"
