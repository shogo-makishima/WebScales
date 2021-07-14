import jsonpickle

class SettingsContainer:
    """Контейнер настроек"""
    def __init__(self, scaleCalibration: float = -4.53, isGr: bool = False, maxWeight: float = 20000, SSID: str = "1", PSK: str = "1") -> None:
        self.scaleCalibration = scaleCalibration
        self.isGr = isGr
        self.SSID = SSID
        self.PSK = PSK
        self.maxWeight = maxWeight
    
    def GetJson(self) -> str:
        return jsonpickle.encode(self)

class DataContainer:
    """Класс сохранения данных"""
    def __init__(self) -> None:
        self.weight: float = 0.0
        self.weightArray: list[float] = []

        self.lenght: float = 0.0
        self.leghtArray: list[float] = []
    
    def GetJson(self) -> str:
        return jsonpickle.encode(self)

dataContainer: DataContainer = DataContainer()
settingsContainer: SettingsContainer = SettingsContainer()

class DataToSend:
    def __init__(self) -> None:
        self.Update()
    
    def Update(self):
        self.weight = dataContainer.weight
        self.lenght = dataContainer.lenght

        self.isGr = settingsContainer.isGr
        self.scaleCalibration = settingsContainer.scaleCalibration
        self.maxWeight = settingsContainer.maxWeight

dataToSend: DataToSend = DataToSend()
