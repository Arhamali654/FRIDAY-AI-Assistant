import os
import shutil

startup_folder = os.path.join(
    os.environ["APPDATA"],
    "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
)

bat_content = '@echo off\npy -3.11 F:\\JARVIS\\friday_ui.py\n'
bat_path = os.path.join(startup_folder, "FRIDAY.bat")

with open(bat_path, "w") as f:
    f.write(bat_content)

print(f"FRIDAY added to startup! File created at:\n{bat_path}")
print("FRIDAY will now launch automatically when Windows starts.")
