from threading import local
import time
from Main.Devices import GPIO

class GenericHX711Exception(Exception):
    pass

class HX711:
    """Класс тензо датчика"""
    def __init__(self, isRaspi: bool = False, dt_pin: int = 5, sck_pin: int = 6, channel: str = "A", gain: int = 128, board: int = 1) -> None:
        # Плата является Raspberry PI или нет?
        self.isRaspri: bool = isRaspi
        self.dt: int = dt_pin
        self.sck: int = sck_pin
        self.channel: str = channel
        self.gain: int = gain
        # Модель платы, для Orange PI
        self.board: int = board

        # Калибровачный коэффициент
        self.scaleCalibration = -4.53

        # Вес тары
        self.tareWeight = 0

        # Максимальное кол-во попыток
        self.maxTries = 10
        
        GPIO.setup(self.sck, GPIO.OUT)
        GPIO.setup(self.dt, GPIO.IN)
    
    def PowerDown(self) -> None:
        GPIO.output(self.sck, False)
        GPIO.output(self.sck, True)
        time.sleep(0.01)

    def PowerUp(self) -> None:
        GPIO.output(self.sck, False)
        time.sleep(0.01)
    
    def Reset(self) -> None:
        self.PowerDown()
        self.PowerUp()
    
    def ApplySetting(self) -> None:
        self.Read()
        time.sleep(0.5)
    
    def isReady(self) -> bool:
        return (GPIO.input(self.dt) == 0)
    
    def SetChannelGain(self, num: int) -> bool:
        if (not 1 <= num <= 3):
            raise AttributeError(""""num" has to be in the range of 1 to 3""")
            
        for _ in range(num):
            start_counter = time.perf_counter()
            GPIO.output(self.sck, True)
            GPIO.output(self.sck, False)
            end_counter = time.perf_counter()
            time_elapsed = float(end_counter - start_counter)

            if time_elapsed >= 0.00006:
                result = self.Read()
                if (result is False):
                    raise GenericHX711Exception("channel was not set properly")
            
        return True

    def Read(self) -> int:
        GPIO.output(self.sck, False)
        readyCounter = 0

        while (not self.isReady()):
            time.sleep(0.01)
            readyCounter += 1

            if (readyCounter >= self.maxTries): return False

        data_in = 0

        for i in range(24):
            start_counter = time.perf_counter()

            GPIO.output(self.sck, True)
            GPIO.output(self.sck, False)

            end_counter = time.perf_counter()
            time_elapsed = float(end_counter - start_counter)

            if time_elapsed >= 0.00006:
                return False

            data_in = (data_in << 1) | GPIO.input(self.dt)

        if (self.channel == 'A' and self.gain == 128): self.SetChannelGain(1)  # send one bit
        elif (self.channel == 'A' and self.gain == 64): self.SetChannelGain(3)  # send three bits
        else: self.SetChannelGain(2)  # send two bits

        if (data_in == 0x7fffff or data_in == 0x800000): return False

        signed_data = 0
        if (data_in & 0x800000):  # 0b1000 0000 0000 0000 0000 0000 check if the sign bit is 1. Negative number.
            signed_data = -((data_in ^ 0xffffff) + 1)  # convert from 2's complement to int
        else: signed_data = data_in

        return signed_data

    def GetUnits(self) -> int:
        return self.Read()
    
    def GetWeight(self, count: int = 1) -> int:
        numbers: list[int] = []
        for i in range(count):
            read: int = self.GetUnits() * 0.035274
            if (read): numbers.append(read)

            if (i < count - 1): time.sleep(0.025)

        count: int = len(numbers)
        if (count == 0): count = 1

        return (sum(numbers) / count) / self.scaleCalibration - self.tareWeight

    def Tare(self, count: int = 1) -> None:
        self.tareWeight = 0
        self.tareWeight = self.GetWeight(count)

    def Calibration(self, currentWeight: float, count: int = 1):
        if (currentWeight != 0):
            localWeight = self.GetUnits()

            localCalibration: float = (self.GetWeight()) / (currentWeight)
            if (localCalibration != 0): self.scaleCalibration = localCalibration

"""
hx711 = HX711(False, 3, 5, board=GPIO.ZERO)

print(f"[DEBUG] Is Ready: {hx711.isReady()}")
hx711.Reset()
time.sleep(1)
hx711.Tare()

maxWeight: float = 20000
currentWeight: float = 0

print(f"[DEBUG] Tare width: {hx711.tareWeight}")

try:
    weightArray: list = []
    
    zeroCount: int = 0
    maxZeroCount: int = 4

    maxWeightArray: int = 8

    while (True):
        weight: float = round(hx711.GetWeight(), 1)

        if (weight <= 2): weight = 0
        elif (weight == -round(hx711.tareWeight, 1)): weight = 0
        elif (weight >= maxWeight):
            if (len(weightArray) > 0):
                weight = weightArray[-1]
            else: weight = 0
        
        if (weight == 0): 
            zeroCount += 1

            if (zeroCount >= maxZeroCount):
                weightArray = [0 for i in range(maxWeightArray)]
                zeroCount = 0
        else: 
            zeroCount = 0
            weightArray.append(weight)

        if (len(weightArray) >= maxWeightArray):
            currentWeight = round(sum(weightArray) / len(weightArray), 1)
            if (currentWeight <= 2): currentWeight = 0

            weightArray.clear()

            print(currentWeight)

        time.sleep(0.1)
except Exception as exception:
    print(exception.with_traceback())
    GPIO.cleanup()
"""
