from Main.Data.Manager import *
from Main.Libs.Thread import Thread

import os, time, xlwt
from datetime import datetime

IS_SAVING: bool = False

class Table:
    isSaving: bool = False
    tableWasCreate: bool = False

    def __init__(self) -> None:
        self.name: str = "Empty"
        self.plotPointsArray: list[PlotPoint] = []
        self.workDirectiory: str = f"{os.getcwd()}/Main/Data/Sheets/"
        self.listTables: list[str] = []
        self.fileType: str = "xlsx"
    
    def SetNewTable(self, name: str) -> None:
        if (self.isSaving): return

        # Имя состоит из названия и времени создания
        self.name = f"{name} {datetime.now().strftime('{%Y %m %d} [%H-%M-%S]')}"
        self.plotPointsArray.clear()

        self.tableWasCreate = True

        Debug.Warning(Debug, f"Set table with name: {self.name}")

    def AddPlotPoint(self) -> None:
        if (self.isSaving and not self.tableWasCreate): return

        if (len(self.plotPointsArray) == 0): self.plotPointsArray.append(PlotPoint(dataContainer.weight, 0))
        elif (abs(self.plotPointsArray[-1].x - dataContainer.weight) > settingsContainer.boundWeight): self.plotPointsArray.append(PlotPoint(dataContainer.weight, len(self.plotPointsArray)))

        if (len(self.plotPointsArray) > 5): self.SaveTableToFile()

    def UpdateListTables(self) -> None:
        self.listTables = list(filter(lambda x: x if x[-len(self.fileType):] == self.fileType else None, os.listdir(self.workDirectiory)))

    @Thread
    def SaveTableToFile(self) -> None:
        self.isSaving = True

        Debug.Warning(Debug, f"Saving table with name: {self.name}")

        book = xlwt.Workbook()
        table = book.add_sheet("Weight | Lenght")

        collumns = { 
            "A": 0,
            "B": 1,
        }

        for i in range(len(self.plotPointsArray)):
            row = table.row(i)
            
            row.write(collumns["A"], self.plotPointsArray[i].x)
            row.write(collumns["B"], i)

        book.save(f"{self.workDirectiory}/{self.name}.{self.fileType}")

        self.tableWasCreate = False
        self.isSaving = False
        

table: Table = Table()
table.UpdateListTables()
table.SetNewTable("Test")
