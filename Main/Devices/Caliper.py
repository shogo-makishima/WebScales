from Main import DataManager
import Main
from Main.Devices import GPIO, IS_RASPI, BOARD
from Main.Libs.HX711.HX711 import HX711, GenericHX711Exception, time
from Main.Libs.Thread import Thread
from Main.Libs.Debug import Debug
from Main.Libs.Perfomance import Monitor

class Caliper:
    isMM: bool = True
    DT: int = 7
    CLK: int = 11
    isRun: bool = True
    zeroValue: float = 0.0

    @Thread
    def Update(self) -> None:
        GPIO.setup(self.DT, GPIO.IN)
        GPIO.setup(self.CLK, GPIO.IN)

        time.sleep(5)

        while (self.isRun):
            Debug.Error(Debug, self.Read(self))
            time.sleep(0.2)

    def Read(self) -> float:
        value: float = 0
        sign: int = 1
        inches: int = 0

        for i in range(24):
            while (GPIO.input(self.CLK) == GPIO.LOW): pass
            while (GPIO.input(self.CLK) == GPIO.HIGH): pass
            time.sleep(0.025)
            if (GPIO.input(self.DT) == GPIO.HIGH):
                if (i < 20): value |= (1 << i)
                if (i == 20): sign = -1
                if (i == 23): inches = 1
        
        print(value, sign, inches)
        if (self.isMM): return (value * sign) / 100 / 2
        else: return (value * sign) / (2000 if (inches) else 100) / 2