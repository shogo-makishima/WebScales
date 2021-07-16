from __future__ import absolute_import, unicode_literals
from traceback import format_exception

from Main import DataManager
import Main
from Main.Devices import GPIO, IS_RASPI, BOARD
from Main.Libs.HX711.HX711 import HX711, GenericHX711Exception, time
from Main.Libs.Thread import Thread
from Main.Libs.Debug import Debug
from Main.Libs.Perfomance import Monitor


class Scales:
    hx711: HX711 = HX711(IS_RASPI, 3, 5, board=BOARD)
    isOpen: bool = False


    @Thread
    def SetZeroPoint(self) -> None:
        self.isOpen = False

        self.hx711.Tare(5)

        self.isOpen = True

    @Thread
    def Run(self) -> None:
        global hx711

        time.sleep(10)

        self.hx711.Reset()

        time.sleep(5)
        
        self.SetZeroPoint(Scales)

        Debug.Message(Debug, f"Tare weight: {self.hx711.tareWeight} gr.")

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

                    Main.TableManager.table.AddPlotPoint()

                    if (abs(DataManager.dataContainer.weight - lastWeight) > 10): Debug.Message(Debug, f"Weight: {DataManager.dataContainer.weight};")

                    lastWeight = DataManager.dataContainer.weight
                
                time.sleep(0.05)
            except Exception as exception:
                Debug.Error(Debug, exception)

