from os import name
import adbutils as adb
import main
import pkgutil
import importlib
import devices
from src import logger as log
full_module_name = f"devices.{main.device_name}"
for loader, module_name, is_pkg in pkgutil.iter_modules(devices.__path__):
    importlib.import_module(f"devices.{module_name}")
d = adb.device()
prop_keys={"ro.product.device",
    "ro.product.model",
    "ro.product.manufacturer",
    "ro.serialno",
    "ro.hardware",
    "ro.board.platform",
    "ro.build.version.release",
    "ro.build.version.sdk",
    "ro.build.id",
    "ro.build.display.id",
    "ro.build.version.security_patch",
    "ro.build.fingerprint",
    "ro.build.type",
    "ro.build.tags",
    "ro.boot.verifiedbootstate",
    "ro.boot.flash.locked",
    "ro.boot.vbmeta.device_state",
    "ro.secure",
    "ro.debuggable",
    "ro.adb.secure",
    "ro.product.first_api_level"
    }
ro_list={}
def get_info():
    log.log("Starting props check..")
    for key in prop_keys:
        try:
            value = d.shell(f"getprop {key}").strip()
            ro_list[key] = value
            log.log(f"Got prop {key}: {value}")
        except Exception as e:
            log.log(f"ERROR: getting prop {key}: {e}")
            ro_list[key] = None
    if ro_list["ro.product.device"] == None:
        main.device_name="Unknown"
    else:
        main.device_name=ro_list["ro.product.device"]
    if ro_list["ro.build.version.release"] == None:
        main.android_version="Unknown"
    else:
        main.android_version=ro_list["ro.build.version.release"]
    if ro_list["ro.serialno"] == None:
        main.serial_no="Unknown"
    else:
        main.serial_no=ro_list["ro.serialno"]
    main.clear()
    main.print_gradient_raidmole()
    main.is_rooted = specific_checks()
    print(f"Model:{main.device_name} | Android Version:{main.android_version} | Serial:{main.serial_no}\n | Rooted:{main.is_rooted}")
    print("=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=")

def specific_checks():
    log.log("Starting specific checks..")
    if main.device_name == "Unknown":
        print("❌ Device name is unknown. Cannot perform specific checks.")
        log.log("ERROR: Device name is unknown.")
        return False
    else:
        try:
            module = importlib.import_module(full_module_name)
            if hasattr(module, "root_check"):
                log.log(f"Root check for {main.device_name} completed. Rooted : {module.root_check()}")
                return module.root_check()
            else:
                print(f"No 'check' function in {full_module_name}")
                log.log(f"ERROR: No 'check' function in {full_module_name}. Using generic root check logic.")
                print("Using generic root check logic.")
                generic_root_check()
                return False
        except ModuleNotFoundError:
            print(f"No custom module found for {main.device_name}.")
            log.log(f"ERROR: Module {main.device_name} not found.")
            log.log("Using default root check logic.")
            print("Using default root check logic.")
            return generic_root_check()
        
def generic_root_check():
    log.log("Using generic root check logic.")
    try:
        output = d.shell("su -c 'id'").strip()
        if "uid=0" in output:
            print("✅ Device is rooted")
            log.log("Device is rooted")
            return True
        else:
            print("❌ Device is not rooted")
            log.log("Device is not rooted")
            return False
    except adb.AdbError as e:
        print(f"❌ Error checking root: {e}")
        log.log(f"ERROR: {e}")
        return False