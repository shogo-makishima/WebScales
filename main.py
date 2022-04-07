from Main.Data.Manager import DataContainer, settingsContainer, Save, Load
from Main.Data.TableManager import table
from Main import Web
from Main import Devices
from Main.Libs.Debug import Debug

if (__name__ == "__main__"):
    Load()

    table.Update()

    try:
        # Devices.Scales.Run(Devices.Scales)
        Devices.ScalesProcess.start()
        Devices.Caliper.CaliperProcess.start()

        Web.SERVER.run(Web.DEFAULT_IP, Web.DEFAULT_PORT, debug=Web.DEFAULT_DEBUG, use_reloader=False, threaded=True)
    except Exception as exception:
        Debug.Error(Debug, f"{exception.with_traceback()}", True)
