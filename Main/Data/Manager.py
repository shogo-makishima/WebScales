from Main.Libs.Debug import Debug
from Main.Data.PlotPoint import PlotPoint
import jsonpickle, os
from Main.Libs.Thread import Thread

SAVE_PATH: str = f"{os.getcwd()}/Main/Data/Settings/"

class SettingsContainer:
    """Контейнер настроек"""
    def __init__(self, scaleCalibration: float = -4.53, isGr: bool = False, maxWeight: float = 20000, boundWeight: float = 10.0) -> None:
        self.scaleCalibration = scaleCalibration
        self.isGr = isGr
        self.maxWeight = maxWeight
        self.boundWeight = boundWeight
    
    def GetJson(self) -> str:
        return jsonpickle.encode(self)

settingsContainer: SettingsContainer = SettingsContainer()

def Load():
    global settingsContainer, SAVE_PATH

    Debug.Message(Debug, "Try to load Settings")
    try: 
        with open(f"{SAVE_PATH}settings.json", "r") as settings:
            text = settings.read()
            settingsContainer = jsonpickle.decode(text)
            
            Debug.Success(Debug, text)
    except Exception as exception:
        Debug.Error(Debug, exception)

@Thread
def Save():
    global settingsContainer, SAVE_PATH

    Debug.Message(Debug, "Try to save Settings")
    try: 
        with open(f"{SAVE_PATH}settings.json", "w") as settings:
            settings.write(settingsContainer.GetJson())
    except Exception as exception:
        Debug.Error(Debug, exception)

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
