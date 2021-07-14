class ByteType:
    def __init__(self, code = "\33[0m"): self.code = code
    def __str__(self): return self.code

class Colored:
    TEXT_RED = ByteType("\33[31m")
    TEXT_YELLOW = ByteType("\33[93m")
    TEXT_GREEN = ByteType("\33[92m")
    TEXT_ITALIC = ByteType("\33[3m")
    TEXT_BOLD = ByteType("\33[1m")
    TEXT_STANDART = ByteType("\33[0m")
    TEXT_BLINK = ByteType("\33[94m")

class Debug:
    @staticmethod
    def Message(self, object: object = "MESSAGE"):
        print(f"{Colored.TEXT_BOLD}{Colored.TEXT_BLINK}{Colored.TEXT_ITALIC}MESSAGE: {Colored.TEXT_STANDART}{object.__str__()}")

    @staticmethod
    def Success(self, object: object = "SUCCESS"):
        print(f"{Colored.TEXT_BOLD}{Colored.TEXT_GREEN}{Colored.TEXT_ITALIC}SUCCESS: {Colored.TEXT_STANDART}{object.__str__()}")

    @staticmethod
    def Warning(self, object: object = "WARNING"):
        print(f"{Colored.TEXT_BOLD}{Colored.TEXT_YELLOW}{Colored.TEXT_ITALIC}WARNING: {Colored.TEXT_STANDART}{object.__str__()}")

    @staticmethod
    def Error(self, object: object = "ERROR"):
        print(f"{Colored.TEXT_BOLD}{Colored.TEXT_RED}{Colored.TEXT_ITALIC}ERROR: {Colored.TEXT_STANDART}{object.__str__()}")


"""
Debug.Message(Debug, object=["1", "2"])
Debug.Success(Debug, object=["1", "2"])
Debug.Warning(Debug, object=["1", "2"])
Debug.Error(Debug, object=["1", "2"])
"""