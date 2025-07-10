from os import name
import adbutils as adb
import pkgutil
import importlib
import devices
import json
from src import logger as log

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
    import main
    log.log("Starting props check..")
    for key in prop_keys:
        try:
            value = d.shell(f"getprop {key}").strip()
            ro_list[key] = value
            log.log(f"Got prop {key}: {value}")
        except Exception as e:
            log.log(f"ERROR: getting prop {key}: {e}")
            ro_list[key] = None
    with open("props.json", "w") as f:
        json.dump(ro_list, f, indent=4)
    if ro_list["ro.product.device"] == None:
        ro_list["ro.product.device"]="Unknown"
    else:
        pass
    if ro_list["ro.build.version.release"] == None:
        ro_list["ro.build.version.release"]="Unknown"
    else:
        pass
    if ro_list["ro.serialno"] == None:
        ro_list["ro.serialno"]="Unknown"
    else:
        pass
    main.clear()
    main.print_gradient_raidmole(False)
    main.is_rooted = specific_checks()
    print(f"Model:{ro_list['ro.product.device']} | Android Version:{ro_list['ro.build.version.release']} | Serial:{ro_list['ro.serialno']} | Rooted:{main.is_rooted}")
    print("=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=")

def specific_checks():
    import main
    full_module_name = f"devices.{ro_list['ro.product.device']}"
    log.log("Starting specific checks..")
    if ro_list['ro.product.device'] == "Unknown":
        print("❌ Device name is unknown. Cannot perform specific checks.")
        log.log("ERROR: Device name is unknown.")
        return False
    else:
        try:
            module = importlib.import_module(full_module_name)
            if hasattr(module, "root_check"):
                log.log(f"Root check for {ro_list['ro.product.device']} completed. Rooted : {module.root_check()}")
                return module.root_check()
            else:
                print(f"No 'check' function in {full_module_name}")
                log.log(f"ERROR: No 'check' function in {full_module_name}. Using generic root check logic.")
                print("Using generic root check logic.")
                generic_root_check()
                return False
        except ModuleNotFoundError:
            print(f"No custom module found for {ro_list['ro.product.device']}.")
            log.log(f"INFO: No custom module found for {ro_list['ro.product.device']}.")
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