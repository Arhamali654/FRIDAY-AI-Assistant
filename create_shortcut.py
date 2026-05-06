import os
import sys

def create_shortcut():
    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        os.system("py -3.11 -m pip install winshell pywin32")
        import winshell
        from win32com.client import Dispatch

    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, "FRIDAY.lnk")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = r"C:\Users\arham\AppData\Local\Programs\Python\Python311\python.exe"
    shortcut.Arguments = r"F:\JARVIS\friday_ui.py"
    shortcut.WorkingDirectory = r"F:\JARVIS"
    shortcut.IconLocation = r"C:\Users\arham\AppData\Local\Programs\Python\Python311\python.exe"
    shortcut.Description = "FRIDAY AI Assistant"
    shortcut.save()
    print("Desktop shortcut created!")

create_shortcut()
