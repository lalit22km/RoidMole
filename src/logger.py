# This script handles generating logs. If you're contributing in custom device scripts or any other code, please make sure to use this to be as verbose as much as possible.
from pathlib import Path
from datetime import datetime

full_path = ''
root_dir = Path(__file__).resolve().parent.parent
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
reports_dir = root_dir / 'reports'
def start(report_id):
    #global report_id_local
    #report_id_local = report_id
    report_folder = reports_dir/str(report_id)
    global full_path
    file_path = report_folder / f"log_{report_id}.txt"
    full_path = file_path
    if not reports_dir.exists():
        print("📁 'reports' folder not found. Creating...")
        reports_dir.mkdir()
        report_folder.mkdir(parents=True)
        with open(file_path, 'w') as f:
            f.write(f"[{timestamp}]:RoidMole started\n")
        print(f"📝 New log started: {file_path}")

    else:
        print("✅ 'reports' folder exists.")
        report_folder.mkdir(parents=True)
        with open(file_path, 'w') as f:
            f.write(f"[{timestamp}]:RoidMole started\n")

        print(f"📝 New log started: {file_path}")

def log(log_data):
    with open(full_path, 'a') as f:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        f.write(f"[{current_time}]:{log_data}\n")