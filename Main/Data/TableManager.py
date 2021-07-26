import Main
from threading import local
from Main.Data.Manager import *
from Main.Libs.Thread import Thread

import os, time, xlwt
from datetime import datetime
import pandas, xlsxwriter
from pandas.core.frame import DataFrame

IS_SAVING: bool = False

class Table:
    isSaving: bool = False
    tableWasCreate: bool = False
    isRun: bool = True

    def __init__(self) -> None:
        self.name: str = "Empty"
        self.plotPointsArray: list[PlotPoint] = []
        self.workDirectiory: str = f"{settingsContainer.path}/Main/Data/Sheets/"
        self.listTables: list[str] = []
        self.fileType: str = "xlsx"
        self.maxPoints: int = 5
        self.isPause: bool = False

        self.time: float = 0.1
        self.startTime: float = 0.0
        self.lastTime: float = 0.0
    
    def SetNewTable(self, name: str) -> None:
        if (self.isSaving): return

        # Имя состоит из названия и времени создания
        self.name = f"{name} {datetime.now().strftime('{%Y %m %d} [%H-%M-%S]')}"
        self.plotPointsArray.clear()

        self.tableWasCreate = True

        self.startTime = time.time()
        self.lastTime = self.startTime

        Debug.Warning(Debug, f"Set table with name: {self.name}")

    def AddPlotPoint(self) -> None:
        if (self.isSaving or not self.tableWasCreate or self.isPause): return

        if (len(self.plotPointsArray) == 0): self.plotPointsArray.append(PlotPoint(dataContainer.weight, 0))
        elif (abs(self.plotPointsArray[-1].x - dataContainer.weight) > self.boundWeight): self.plotPointsArray.append(PlotPoint(dataContainer.weight, len(self.plotPointsArray)))

        if (len(self.plotPointsArray) >= self.maxPoints): self.SaveTableToFile()

    def ChangePause(self, getPause: bool = None) -> None:
        if (getPause != None and type(getPause) == bool): self.isPause = getPause  
        else: self.isPause = not self.isPause

    def UpdateListTables(self) -> None:
        local_files = list(filter(lambda x: x if x[-len(self.fileType):] == self.fileType else None, os.listdir(self.workDirectiory)))
        self.listTables = [file[len(self.workDirectiory):] for file in sorted([f"{self.workDirectiory}{file}" for file in local_files], key=os.path.getmtime, reverse=True)]

    def GetTableName(self) -> str:
        if (not self.tableWasCreate): return "Null"

        return self.name
 
    def GetTableSize(self) -> float:
        if (not self.tableWasCreate): return "Null"

        return round((100 / self.maxPoints) * len(self.plotPointsArray), 1)

    @Thread
    def Update(self) -> None:
        while (self.isRun):
            if (not Main.Devices.Scales.isReady or self.isSaving or not self.tableWasCreate or self.isPause): continue

            if ((time.time() - self.lastTime) >= self.time):
                self.plotPointsArray.append(PlotPoint(dataContainer.weight, dataContainer.lenght.value, round(time.time() - self.startTime, 1)))
                self.lastTime = time.time()
            
            if (len(self.plotPointsArray) >= self.maxPoints): self.SaveTableToFile()

    @Thread
    def Clear(self):
        self.plotPointsArray.clear()

    def AddChart(self, workbook: xlsxwriter.workbook.Workbook, valueLine: str = "B", categotiesLine: str = "D", valueName: str = "Weight", categoriesName: str = "Time") -> None:
        chart = workbook.add_chart({'type': 'line'})

        chart.add_series({
            'values':     f"=Sheet1!${valueLine}${2}:${valueLine}${2 + len(self.plotPointsArray)}",
            'categories': f"=Sheet1!${categotiesLine}${2}:${categotiesLine}${2 + len(self.plotPointsArray)}",
            'line':       {'color': 'black'},
        })

        chart.set_x_axis({'name': categoriesName, 'major_gridlines': {'visible': True, 'line': {'width': 1.25, 'dash_type': 'dash'}}, 'position_axis': 'on_tick'})
        chart.set_y_axis({'name': valueName, 'major_gridlines': {'visible': True}, 'minor_gridlines': {'visible': True}})

        chart.set_legend({'position': 'none'})

        return chart

    @Thread
    def SaveTableToFile(self) -> None:
        if (self.isSaving or not self.tableWasCreate): return

        self.isSaving = True

        Debug.Warning(Debug, f"Saving table with name: {self.name}")

        data = {"Weight": list(), "Lenght": list(), "Time": list()}

        for point in self.plotPointsArray:
            data["Weight"].append(point.x)
            data["Lenght"].append(point.y)
            data["Time"].append(point.z)

        dataFrame = pandas.DataFrame(data)

        writer = pandas.ExcelWriter(f"{self.workDirectiory}/{self.name}.{self.fileType}", engine="xlsxwriter")

        dataFrame.to_excel(writer, sheet_name='Sheet1')

        workbook: xlsxwriter.workbook.Workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        worksheet.insert_chart('F2', self.AddChart(workbook, "B", "D", "Weight"), {'x_scale': 2, 'y_scale': 1})
        worksheet.insert_chart('F20', self.AddChart(workbook, "C", "D", "Lenght"), {'x_scale': 2, 'y_scale': 1})

        writer.save()

        self.Clear()

        self.tableWasCreate = False
        self.isSaving = False
        

table: Table = Table()
