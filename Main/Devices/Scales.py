from __future__ import absolute_import, unicode_literals

import Main.Data.Manager as DataManager
import Main
from Main.Devices import wiringpi
from Main.Libs.HX711.HX711 import HX711, GenericHX711Exception, time
from Main.Libs.Thread import Thread
from Main.Libs.Debug import Debug
from Main.Libs.Perfomance import Monitor


class Scales:
    hx711: HX711 = HX711(False, 15, 16, board=1)
    isOpen: bool = False
    isReady: bool = False

    @Thread
    def SetZeroPoint(self) -> None:
        self.isOpen = False

        self.hx711.Tare(5)

        self.isOpen = True

    @Thread
    def Calibration(self, weight: float) -> None:
        if (not self.isOpen): return

        self.isOpen = False

        Debug.Message(Debug, "Start calibration wait 2 sec. and put the weight 8 sec.")
        
        time.sleep(2)

        self.hx711.scaleCalibration = 1
        self.hx711.Tare(5)

        time.sleep(8)

        self.hx711.Calibration(weight, 25)

        DataManager.settingsContainer.scaleCalibration = Scales.hx711.scaleCalibration

        Debug.Success(Debug, f"Calibtaion continue with scaleCalibration: {DataManager.settingsContainer.scaleCalibration}")
        DataManager.Save()

        self.isOpen = True

    @Thread
    def Run(self) -> None:
        global hx711

        time.sleep(5)

        self.hx711.Reset()

        Scales.hx711.scaleCalibration = DataManager.settingsContainer.scaleCalibration

        time.sleep(5)
        
        self.SetZeroPoint(Scales)

        time.sleep(5)

        Debug.Message(Debug, f"Tare weight: {self.hx711.tareWeight} gr.")

        self.isReady = True

        weightArray: list = []
        
        zeroCount: int = 0
        maxZeroCount: int = 4

        maxWeightArray: int = 4

        lastWeight: float = 0

        while (True):
            try:
                if (not self.isOpen):
                    weightArray.clear()
                    zeroCount = 0
                    continue

                weight: float = round(self.hx711.GetWeight(), 1)

                if (abs(weight) <= 3): weight = 0
                elif (abs(weight) == -round(self.hx711.tareWeight, 1)): weight = 0
                elif (abs(weight) >= DataManager.settingsContainer.maxWeight):
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
                    # Debug.Error(Debug, f"Array: {weightArray}")

                    for i in range(maxWeightArray):
                        nonZeroArray: list = [abs(i) for i in weightArray if abs(i) > 0]
                        
                        if (nonZeroArray != list()):
                            min_w: float = min(nonZeroArray)
                            current_w: float = abs(weightArray[i])

                            if (current_w / min_w > 10): weightArray[i] = min_w

                    DataManager.dataContainer.weight = round(sum(weightArray) / len(weightArray), 1)
                    if (abs(DataManager.dataContainer.weight) <= 2): DataManager.dataContainer.weight = 0

                    weightArray.clear()

                    if (abs(DataManager.dataContainer.weight - lastWeight) > 10): Debug.Message(Debug, f"Weight: {DataManager.dataContainer.weight};")

                    lastWeight = DataManager.dataContainer.weight
                
                time.sleep(0.025)
            except Exception as exception:
                Debug.Error(Debug, exception)

