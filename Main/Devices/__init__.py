import platform

OS = platform.platform().split("-")

if (OS[0] == "Windows"):
    from RPiSim.GPIO import GPIO
elif (OS[0] == "Linux"):
    try: import RPi.GPIO as GPIO
    except: import OPi.GPIO as GPIO

IS_RASPI: bool = False
BOARD: int = 1

if (IS_RASPI):
    GPIO.setmode(GPIO.BCM)
else:
    GPIO.setboard(BOARD)
    GPIO.setmode(GPIO.BOARD)

from Main.Devices.Scales import Scales
from Main.Devices.Caliper import Caliper
