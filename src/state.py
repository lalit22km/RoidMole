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
    main.clear()
    main.print_gradient_raidmole()