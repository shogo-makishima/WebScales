from __future__ import absolute_import, unicode_literals
from glob import glob
import re

import Main.Data.Manager as DataManager
import Main, multiprocessing, threading
from Main.Devices import wiringpi
from Main.Libs.HX711.HX711 import HX711, GenericHX711Exception, time
from Main.Libs.Thread import Thread
from Main.Libs.Debug import Debug
from Main.Libs.Perfomance import Monitor



class Scales(threading.Thread):
    def __init__(self):
        super(Scales, self).__init__()

        self.hx711: HX711 = HX711(False, 8, 9, board=1)
        self.isOpen: bool = False
        self.isReady: bool = False

        self.zeroCount: int = 0
        self.maxZeroCount: int = 4
        self.maxWeightArray: int = 4
        self.lastWeight: float = 0
        self.weightArray: list = []

    def SetZeroPoint(self) -> None:
        self.isOpen = False

        # self.hx711.Tare(5)
        self.hx711.tareWeight = 0
        self.hx711.tareWeight = self.GetWeight()

        Debug.Warning(Debug, f"Tare weight: {self.hx711.tareWeight} gr. Scale Calibration: {self.hx711.scaleCalibration}")

        self.isOpen = True

    def Calibration(self, weight: float) -> None:
        if (not isOpen): return

        self.isOpen = False
        Debug.Message(Debug, "Start calibration wait 2 sec. and put the weight 8 sec.")
        
        time.sleep(2)

        self.hx711.scaleCalibration = 1
        self.hx711.Tare(5)

        time.sleep(58)

        self.hx711.Calibration(weight, 25)

        DataManager.settingsContainer.scaleCalibration = self.hx711.scaleCalibration
        Debug.Success(Debug, f'Calibtaion continue with scaleCalibration: {DataManager.settingsContainer.scaleCalibration}')
        DataManager.Save()

        isOpen = True
    
    def GetWeight(self) -> float:
        retWeight = None
        while (len(self.weightArray) < self.maxWeightArray):     
            weight: float = round(self.hx711.GetWeight(), 1)

            if (abs(weight) <= 3): weight = 0
            elif (abs(weight) == -round(self.hx711.tareWeight, 1)): weight = 0
            elif (abs(weight) >= DataManager.settingsContainer.maxWeight):
                if (len(self.weightArray) > 0):
                    weight = self.weightArray[-1]
                else: weight = 0
            
            if (weight == 0): 
                self.zeroCount += 1
                if (self.zeroCount >= self.maxZeroCount):
                    self.weightArray = [0 for i in range(self.maxWeightArray)]
                    self.zeroCount = 0
            else: 
                self.zeroCount = 0
                self.weightArray.append(weight)
            
        print(f"{len(self.weightArray)} >= {self.maxWeightArray}")
        if (len(self.weightArray) >= self.maxWeightArray):
            for i in range(self.maxWeightArray):
                nonZeroArray: list = [abs(i) for i in self.weightArray if abs(i) > 0]
                
                if (nonZeroArray != list()):
                    min_w: float = min(nonZeroArray)
                    current_w: float = abs(self.weightArray[i])
                    if (current_w / min_w > 10): self.weightArray[i] = min_w
            
            retWeight = round(sum(self.weightArray) / len(self.weightArray), 1)

            print(retWeight)

            if (abs(retWeight) <= 2): retWeight = 0

            self.weightArray.clear()

        return retWeight

    def run(self):
        time.sleep(5)

        self.hx711.Reset()
        self.hx711.scaleCalibration = DataManager.settingsContainer.scaleCalibration

        time.sleep(5)
        
        self.SetZeroPoint()

        time.sleep(5)

        self.isReady = True

        while (True):
            try:
                weight = self.GetWeight()
                if (not weight is None):
                    DataManager.dataContainer.weight = weight

                    if (abs(DataManager.dataContainer.weight - self.lastWeight) > 10): Debug.Message(Debug, f"Weight: {DataManager.dataContainer.weight};")

                    self.lastWeight = DataManager.dataContainer.weight
                
                time.sleep(0.025)
            except Exception as exception:
                Debug.Error(Debug, f"{exception.with_traceback()}")


ScalesProcess = Scales()