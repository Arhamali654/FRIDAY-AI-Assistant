import threading
import time
import datetime
import sqlite3
from config import DB_PATH, JARVIS_NAME

def start_reminder_thread():
    thread = threading.Thread(target=_reminder_loop, daemon=True)
    thread.start()

def _reminder_loop():
    while True:
        try:
            _check_reminders()
        except Exception as e:
            print(f"[{JARVIS_NAME}] Reminder error: {e}")
        time.sleep(30)

def _check_reminders():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        "SELECT id, message FROM reminders WHERE remind_at <= ? AND done = 0",
        (now,)
    )
    rows = cursor.fetchall()
    for row in rows:
        reminder_id, message = row
        print(f"\n[{JARVIS_NAME}] REMINDER: {message}")
        try:
            from modules.voice import speak
            speak(f"Reminder: {message}")
        except:
            pass
        cursor.execute("UPDATE reminders SET done = 1 WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()

def set_reminder(message: str, minutes: int = None, hours: int = None, at_time: str = None) -> str:
    try:
        now = datetime.datetime.now()
        if at_time:
            try:
                remind_at = datetime.datetime.strptime(at_time, "%H:%M").replace(
                    year=now.year, month=now.month, day=now.day
                )
                if remind_at < now:
                    remind_at += datetime.timedelta(days=1)
            except:
                return f"Invalid time format. Use HH:MM like 14:30."
        elif hours:
            remind_at = now + datetime.timedelta(hours=hours)
        elif minutes:
            remind_at = now + datetime.timedelta(minutes=minutes)
        else:
            remind_at = now + datetime.timedelta(minutes=5)

        remind_at_str = remind_at.strftime("%Y-%m-%d %H:%M")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reminders (message, remind_at, done) VALUES (?, ?, 0)",
            (message, remind_at_str)
        )
        conn.commit()
        conn.close()

        time_str = remind_at.strftime("%I:%M %p")
        return f"Reminder set for {time_str}: {message}"

    except Exception as e:
        return f"Could not set reminder: {str(e)}"

def set_timer(seconds: int, label: str = "Timer") -> str:
    def _timer():
        time.sleep(seconds)
        print(f"\n[{JARVIS_NAME}] {label} is done!")
        try:
            from modules.voice import speak
            speak(f"{label} is done!")
        except:
            pass

    thread = threading.Thread(target=_timer, daemon=True)
    thread.start()

    if seconds >= 3600:
        h = seconds // 3600
        return f"Timer set for {h} hour{'s' if h > 1 else ''}."
    elif seconds >= 60:
        m = seconds // 60
        return f"Timer set for {m} minute{'s' if m > 1 else ''}."
    else:
        return f"Timer set for {seconds} seconds."

def list_reminders() -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT message, remind_at FROM reminders WHERE done = 0 ORDER BY remind_at ASC LIMIT 5"
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "No upcoming reminders."
    result = "Upcoming reminders: "
    for message, remind_at in rows:
        time_str = datetime.datetime.strptime(remind_at, "%Y-%m-%d %H:%M").strftime("%I:%M %p")
        result += f"{message} at {time_str}. "
    return result

def handle_reminder_command(command: str) -> str:
    cmd = command.lower()

    if "list" in cmd or "show" in cmd or "what" in cmd:
        return list_reminders()

    elif "timer" in cmd:
        import re
        hours_match   = re.search(r'(\d+)\s*hour', cmd)
        minutes_match = re.search(r'(\d+)\s*min', cmd)
        seconds_match = re.search(r'(\d+)\s*sec', cmd)

        seconds = 0
        if hours_match:
            seconds += int(hours_match.group(1)) * 3600
        if minutes_match:
            seconds += int(minutes_match.group(1)) * 60
        if seconds_match:
            seconds += int(seconds_match.group(1))

        if seconds == 0:
            seconds = 300

        label = cmd.replace("set", "").replace("timer", "").replace("a", "").strip().capitalize()
        return set_timer(seconds, label if label else "Timer")

    elif "remind" in cmd or "reminder" in cmd or "alarm" in cmd:
        import re
        hours_match   = re.search(r'(\d+)\s*hour', cmd)
        minutes_match = re.search(r'(\d+)\s*min', cmd)
        time_match    = re.search(r'at\s+(\d{1,2}:\d{2})', cmd)
        at_match      = re.search(r'at\s+(\d{1,2})\s*(am|pm)', cmd)

        message = cmd
        for word in ["remind", "reminder", "me", "to", "set", "an", "alarm", "friday", "a"]:
            message = message.replace(word, "")
        import re as _re
        message = _re.sub(r'\d+\s*(hour|min|sec|am|pm|:\d+)', '', message)
        message = message.strip().capitalize()
        if not message:
            message = "Reminder"

        if time_match:
            return set_reminder(message, at_time=time_match.group(1))
        elif at_match:
            hour = int(at_match.group(1))
            period = at_match.group(2)
            if period == "pm" and hour != 12:
                hour += 12
            elif period == "am" and hour == 12:
                hour = 0
            at_time = f"{hour:02d}:00"
            return set_reminder(message, at_time=at_time)
        elif hours_match:
            return set_reminder(message, hours=int(hours_match.group(1)))
        elif minutes_match:
            return set_reminder(message, minutes=int(minutes_match.group(1)))
        else:
            return set_reminder(message, minutes=5)

    return "Reminder command not recognized. Try: remind me to drink water in 10 minutes."
