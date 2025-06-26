import subprocess
import adbutils
import time
from colorama import Fore, Style, init
from src import logger as log
import sys

def adb_check():
    log.log("ADB Check started")
    try:
        result = subprocess.run(
            ["adb", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        output = result.stdout.strip().splitlines()

        if len(output) >= 3:
            log.log("ADB found on system")
            version = output[0].replace("Android Debug Bridge version", "").strip()
            build = output[1].strip()
            location = output[2].replace("Installed as", "").strip()

            print(f"✅ ADB is installed")
            print(f"🔢 Version: {version}")
            print(f"🧱 Build: {build}")
            print(f"📂 Path: {location}")
            
        else:
            print("⚠️ ADB output is incomplete. Got:\n", result.stdout)
            log.log(f"ERROR: ADB output is incomplete. Got:", result.stdout)

    except FileNotFoundError:
        print("❌ ADB is not installed or not in PATH. \nInstall ADB from https://developer.android.com/tools/releases/platform-tools")
        log.log("ERROR: ADB is not installed on system or not in PATH")
        exit()
    except subprocess.CalledProcessError as e:
        print("❌ ADB command failed !\nADB is installed but produces error(s). Make sure ADB is updated.\nGet the latest binaries from https://developer.android.com/tools/releases/platform-tools")
        log.log("ERROR: ADB might be installed but produces error(s).")
        exit()
def device_check():
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
    log.log("Start listening on localhost:5037")

    while True:
        devices = adb.list(extended=True)

        if not devices:
            print("⏳ Waiting for device to connect...", end="\r")
            time.sleep(2)
            continue

        for info in devices:
            serial = info.serial
            state = info.state.lower()

            if state == "device":
                print(f"✅ Device connected: {serial} ({state})")
                return info

            elif state == "unauthorized":
                print(f"🔒 Device {serial} is unauthorized. Please authorize it on your phone.")
                while True:
                    time.sleep(2)
                    updated_info = next((d for d in adb.list(extended=True) if d.serial == serial), None)
                    if updated_info and updated_info.state.lower() == "device":
                        print(f"✅ Device authorized: {serial}")
                        return updated_info
                    print(f"⏳ Waiting for authorization from {serial}...:P", end="\r")

        time.sleep(2)
def print_gradient_raidmole():
    init(autoreset=True)
    
    ascii_art = """
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
    
   ██████╗  ██████╗ ██╗██████╗ ███╗   ███╗ ██████╗ ██╗     ███████╗
   ██╔══██╗██╔═══██╗██║██╔══██╗████╗ ████║██╔═══██╗██║     ██╔════╝
   ██████╔╝██║   ██║██║██║  ██║██╔████╔██║██║   ██║██║     █████╗  
   ██╔══██╗██║   ██║██║██║  ██║██║╚██╔╝██║██║   ██║██║     ██╔══╝  
   ██║  ██║╚██████╔╝██║██████╔╝██║ ╚═╝ ██║╚██████╔╝███████╗███████╗
   ╚═╝  ╚═╝ ╚═════╝ ╚═╝╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚══════╝
                                                                
=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=
"""
    
    colors = [Fore.WHITE, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.CYAN, Fore.BLUE, Fore.LIGHTBLACK_EX]
    lines = ascii_art.strip().split('\n')
    
    for i, line in enumerate(lines):
        if i < len(colors):
            color = colors[i]
        else:
            color = colors[i % len(colors)]
        print(f"{color}{Style.BRIGHT}{line}")
    log.start()


print_gradient_raidmole()
adb_check()
device_check()