import adbutils as adb
import main
from src import logger as log
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
    print(f"Model:{main.device_name} | Android Version:{main.android_version} | Serial:{main.serial_no}\n")
    print("=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=")