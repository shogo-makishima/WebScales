from Main.Libs.Debug import Debug
from Main.Data.PlotPoint import PlotPoint
import jsonpickle

class SettingsContainer:
    """Контейнер настроек"""
    def __init__(self, scaleCalibration: float = -4.53, isGr: bool = False, maxWeight: float = 20000, boundWeight: float = 10.0, SSID: str = "1", PSK: str = "1") -> None:
        self.scaleCalibration = scaleCalibration
        self.isGr = isGr
        self.SSID = SSID
        self.PSK = PSK
        self.maxWeight = maxWeight
        self.boundWeight = boundWeight
    
    def GetJson(self) -> str:
        return jsonpickle.encode(self)

settingsContainer: SettingsContainer = SettingsContainer()

class DataContainer:
    """Класс сохранения данных"""
    def __init__(self) -> None:
        self.weight: float = 0.0
        self.lenght: float = 0.0
    
    def GetJson(self) -> str:
        return jsonpickle.encode(self)

dataContainer: DataContainer = DataContainer()

class DataToSend:
    def __init__(self) -> None:
        self.Update()
    
    def Update(self):
        self.weight = dataContainer.weight
        self.lenght = dataContainer.lenght

        self.isGr = settingsContainer.isGr
        self.scaleCalibration = settingsContainer.scaleCalibration
        self.maxWeight = settingsContainer.maxWeight
        self.boundWeight = settingsContainer.boundWeight

dataToSend: DataToSend = DataToSend()
