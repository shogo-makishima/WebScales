from Main import Web
from Main import Devices

if (__name__ == "__main__"):
    Devices.Scales.Run(Devices.Scales)

    Web.SERVER.run(Web.DEFAULT_IP, Web.DEFAULT_PORT, debug=Web.DEFAULT_DEBUG, use_reloader=False)
