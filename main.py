import time
import sys
sys.path.insert(0, "F:\\JARVIS")
from modules.voice import listen, speak
from modules.brain import think
from modules.memory import save_conversation, init_db
from modules.system import handle_system_command
from modules.weather import handle_weather_command
from modules.music import handle_music_command
from modules.reminder import handle_reminder_command, start_reminder_thread
from modules.screen import handle_screen_command
from modules.autopilot import handle_autopilot_command
from config import WAKE_WORD, JARVIS_NAME

running = True

def greet():
    hour = time.localtime().tm_hour
    if 5 <= hour < 12:
        period = "Good morning"
    elif 12 <= hour < 17:
        period = "Good afternoon"
    else:
        period = "Good evening"
    msg = f"{period}. {JARVIS_NAME} online. How can I assist you?"
    print(f"[{JARVIS_NAME.upper()}] {msg}")
    speak(msg)

def route_command(command: str) -> str:
    cmd = command.lower()

    screen_keywords   = ["read screen", "describe screen", "what's on screen",
                         "what is on screen", "whats on screen", "read my screen",
                         "what do you see", "look at screen", "screen says",
                         "what apps", "what is open", "what's open"]
    autopilot_keywords= ["click on", "click the", "switch to", "go to window",
                         "scroll down", "scroll up", "type this", "press enter",
                         "press escape", "copy this", "paste", "select all",
                         "save file", "close window", "close this", "minimize",
                         "maximize", "lock screen", "undo", "redo",
                         "search google for", "automate"]
    system_keywords   = ["open", "close", "launch", "start", "kill",
                         "screenshot", "volume", "mute", "unmute",
                         "shutdown", "restart", "system stats", "system status",
                         "cpu usage", "ram usage", "disk space"]
    weather_keywords  = ["weather", "temperature", "forecast", "rain", "humidity"]
    news_keywords     = ["news", "headlines", "latest news"]
    music_keywords    = ["play music", "pause music", "stop music", "next song",
                         "previous song", "play song", "spotify", "skip song"]
    reminder_keywords = ["remind", "reminder", "alarm", "timer", "schedule"]

    if any(k in cmd for k in screen_keywords):
        return handle_screen_command(command)
    elif any(k in cmd for k in autopilot_keywords):
        return handle_autopilot_command(command)
    elif any(k in cmd for k in system_keywords):
        return handle_system_command(command)
    elif any(k in cmd for k in weather_keywords):
        return handle_weather_command(command)
    elif any(k in cmd for k in news_keywords):
        return handle_weather_command(command)
    elif any(k in cmd for k in music_keywords):
        return handle_music_command(command)
    elif any(k in cmd for k in reminder_keywords):
        return handle_reminder_command(command)
    else:
        return think(command)

def process_command(command: str):
    print(f"\n[YOU] {command}")
    response = route_command(command)
    print(f"[{JARVIS_NAME.upper()}] {response}")
    speak(response)
    save_conversation(command, response)

def wake_word_loop():
    speak(f"Say {WAKE_WORD} to activate me.")
    while running:
        audio = listen(timeout=5, phrase_limit=3)
        if audio and WAKE_WORD.lower() in audio.lower():
            speak("Yes?")
            command = listen(timeout=8, phrase_limit=15)
            if command:
                process_command(command)
        time.sleep(0.1)

def continuous_loop():
    speak("Continuous mode active. Speak your command.")
    while running:
        command = listen(timeout=10, phrase_limit=15)
        if command:
            if any(x in command.lower() for x in ["goodbye", "bye", "shutdown friday", "exit friday"]):
                speak("Goodbye. Shutting down.")
                break
            process_command(command)

def main():
    global running
    print("=" * 50)
    print(f"  {JARVIS_NAME} — Starting up")
    print("=" * 50)

    init_db()
    start_reminder_thread()
    greet()

    print("\nMode: (1) Wake word  (2) Continuous  (3) Text only")
    mode = input("Select mode [1/2/3]: ").strip()

    if mode == "1":
        print(f"\nWake word mode — say '{WAKE_WORD}' to activate")
        wake_word_loop()
    elif mode == "2":
        print("\nContinuous mode — speak freely")
        continuous_loop()
    elif mode == "3":
        print("\nText mode — type your commands (type 'exit' to quit)")
        while running:
            command = input("\nYou: ").strip()
            if not command:
                continue
            if command.lower() in ["exit", "quit", "bye"]:
                speak("Goodbye!")
                break
            process_command(command)
    else:
        while running:
            command = input("\nYou: ").strip()
            if not command:
                continue
            if command.lower() in ["exit", "quit"]:
                break
            process_command(command)

    running = False
    print(f"\n{JARVIS_NAME} offline.")

if __name__ == "__main__":
    main()
