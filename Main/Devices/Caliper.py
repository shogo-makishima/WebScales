import datetime
from os import name
import Main, threading
import Main.Data.Manager as DataManager
from Main.Devices import wiringpi
from Main.Libs.HX711.HX711 import HX711, GenericHX711Exception, time
from Main.Libs.Thread import Thread, CThread, multiprocessing, MULTI_DATA
from Main.Libs.Debug import Debug
from Main.Libs.Perfomance import Monitor


isMM: bool = True
DT: int = 9
CLK: int = 8
isRun: bool = True
zeroValue: float = 0.0
lastValue: float = 0.0

wiringpi.pinMode(CLK, 0)
wiringpi.pinMode(DT, 0)

def Read() -> float:
    global DT, CLK, isMM

    sign: int = 1
    value: int = 0
    inches: int = 0
    array: list[int] = list()
    
    for i in range(24):
        while (wiringpi.digitalRead(CLK) == 0): pass
        while (wiringpi.digitalRead(CLK) == 1): pass
        read = (wiringpi.digitalRead(DT) == 1)

        array.append(1 if (read) else 0)

        if (read):
            if (i < 20): value |= (1 << i)
            if (i == 21):
                sign = -1
            if (i == 23): inches = 1
    
    if (isMM): return (value * sign) / 100 / 2
    else: return (value * sign) / (2000 if (inches) else 100) / 2

@Thread
def Main():
    global isRun, lastValue

    while (isRun):
        lenght: float = Read()

        DataManager.dataContainer.lenght.value = lenght
        if (abs(lastValue - lenght) > 0.1): Debug.Message(Debug, f"Current lenght: {lenght}")
        lastValue = lenght

CaliperProcess = multiprocessing.Process(target=Main, args=())

