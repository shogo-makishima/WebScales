from flask.helpers import url_for
from Main.Libs.Debug import Debug
from flask import Flask, render_template, request, send_from_directory, send_file, redirect
from flask_restful import reqparse, abort, Api, Resource
import Main.Data.Manager as DataManager
from Main.Data.TableManager import table
from Main.Devices.Scales import Scales
import os

"""Сервер"""
SERVER = Flask(__name__)
API = Api(SERVER)

@SERVER.route("/")
def index():
    """Перехват главной страницы"""
    return render_template("html/index.html")

@SERVER.route("/api/set_data", methods=["POST"])
def setSettings():
    json = dict(request.json)

    if (json.get("isGr") != None): DataManager.settingsContainer.isGr = json["isGr"]
    DataManager.Save()

    DataManager.dataToSend.Update()
    return DataManager.dataToSend.__dict__, 200

@SERVER.route("/api/set_zero_point", methods=["POST"])
def setZeroPoint():
    Scales.SetZeroPoint(Scales)

    DataManager.dataToSend.Update()
    return DataManager.dataToSend.__dict__, 200

@SERVER.route("/api/get_file_list", methods=["GET"])
def getFileList():
    table.UpdateListTables()
    return { "directory": table.workDirectiory, "files": table.listTables }, 200

@SERVER.route("/api/set_new_test", methods=["POST"])
def setNewTest():
    json = dict(request.json)

    Debug.Error(Debug, json)

    if (json.get("name") != None and json.get("size") != None):
        table.maxPoints = int(json["size"])
        table.SetNewTable(json["name"])
    
    return {}, 200

@SERVER.route("/api/set_pause_table", methods=["POST"])
def setPauseTable():
    table.ChangePause()
    return {}, 200

@SERVER.route("/api/set_close_table", methods=["POST"])
def setCloseTable():
    table.SaveTableToFile()
    return {}, 200

@SERVER.route("/api/set_calibration_scales", methods=["POST"])
def setCalibrationScales():
    json = dict(request.json)

    if (json.get("weight") != None):
        Scales.Calibration(Scales, float(json["weight"]))
    elif (json.get("scaleCalibration") != None):
        Scales.hx711.scaleCalibration = float(json["scaleCalibration"])
        DataManager.settingsContainer.scaleCalibration = Scales.hx711.scaleCalibration
        DataManager.Save()
    
    return {}, 200

@SERVER.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(table.workDirectiory, filename)

@SERVER.route('/delete', methods=['GET', 'POST'])
def delete():
    json = dict(request.json)
    os.remove(f"{table.workDirectiory}{json['filename']}")

    table.UpdateListTables()
    return { "directory": table.workDirectiory, "files": table.listTables }, 200

class Data(Resource):
    def get(self):
        DataManager.dataToSend.Update()

        data = DataManager.dataToSend.__dict__
        data["testName"] = table.GetTableName()
        data["testSize"] = table.GetTableSize()
        data["testPause"] = table.isPause
        
        return data, 200
    
    def post(self):
        DataManager.dataToSend.Update()

        data = DataManager.dataToSend.__dict__
        data["testName"] = table.GetTableName()
        data["testSize"] = table.GetTableSize()
        data["testPause"] = table.isPause

        return data, 200

API.add_resource(Data, "/api/update_data")