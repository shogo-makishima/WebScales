from flask import Flask, render_template, request
from flask_restful import reqparse, abort, Api, Resource
import Main.Data.Manager as DataManager
from Main.Devices.Scales import Scales

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
    
    DataManager.dataToSend.Update()
    return DataManager.dataToSend.__dict__, 200

@SERVER.route("/api/set_zero_point", methods=["POST"])
def setZeroPoint():
    Scales.SetZeroPoint(Scales)

    DataManager.dataToSend.Update()
    return DataManager.dataToSend.__dict__, 200

class Data(Resource):
    def get(self):
        DataManager.dataToSend.Update()
        return DataManager.dataToSend.__dict__
    
    def post(self):
        DataManager.dataToSend.Update()
        return DataManager.dataToSend.__dict__, 200

API.add_resource(Data, "/api/update_data")