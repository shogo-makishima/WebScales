import psutil

class Monitor:
    @staticmethod
    def GetCpu() -> float:
        return psutil.cpu_percent()
    
    @staticmethod
    def GetAvailableRam() -> float:
        return psutil.virtual_memory().available * 100 / psutil.virtual_memory().total