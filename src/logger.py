# This script handles generating logs. If you're contributing in custom device scripts or any other code, please make sure to use this to be as verbose as much as possible.
import os
from pathlib import Path
from datetime import datetime

root_dir = Path(__file__).resolve().parent.parent
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
reports_dir = root_dir / 'reports'
file_path = reports_dir / f"log_{timestamp}.txt"
def start():
    if not reports_dir.exists():
        print("📁 'reports' folder not found. Creating...")
        reports_dir.mkdir()
        
        with open(file_path, 'w') as f:
            f.write(f"[{timestamp}]:DroidMole started\n")

        print(f"📝 New report created: {file_path}")

    else:
        print("✅ 'reports' folder exists.")

        with open(file_path, 'w') as f:
            f.write(f"[{timestamp}]:DroidMole started\n")

        print(f"📝 New report created: {file_path}")

def log(log_data):
    with open(file_path, 'a') as f:
        f.write(f"[{timestamp}]:{log_data}\n")