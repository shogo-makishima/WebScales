var currentTestTableLenght = 0;
var wasServerAwake = false;
var fileFirstLoad = false;

function GetUpdate() {
    if (wasServerAwake) {
        $.ajax({
            type: "GET",
            url: "/api/update_data",
            cache: false,
            dataType: "text/json",
            statusCode: {
                200: function(data) {
                    var json = JSON.parse(data.responseText);
                    Update(json);
                }
            }
        });
        
        if (fileFirstLoad === false) {
            GetFileList();
            fileFirstLoad = true;
        }
    }

    window.setTimeout(GetUpdate, 250);
}

function ChangePause() {
    if (wasServerAwake) {
        $.post({
            url: "/api/set_pause_table",
            cache: false,
            contentType: 'application/json',
            statusCode: {
                200: function(data) {
                }
            }
        });
    }
}

function CloseTable() {
    if (wasServerAwake) {
        $.post({
            url: "/api/set_close_table",
            cache: false,
            contentType: 'application/json',
            statusCode: {
                200: function(data) {
                }
            }
        });
    }
}

function ClearTable() {
    if (wasServerAwake) {
        $.post({
            url: "/api/set_clear_table",
            cache: false,
            contentType: 'application/json',
            statusCode: {
                200: function(data) {
                }
            }
        });
    }
}

function SetCalibrationScales(weight = null, scaleCalibration = null) {
    if (wasServerAwake) {
        $.post({
            url: "/api/set_calibration_scales",
            cache: false,
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                weight: weight,
                scaleCalibration: scaleCalibration,
            }),
            statusCode: {
                200: function(data) {
                }
            }
        });
    }
}

function ChangeSettings(isGr = null, scaleCalibration = null, maxWeight = null) {
    if (wasServerAwake) {
        $.post({
            url: "/api/set_data",
            cache: false,
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                isGr: isGr,
                scaleCalibration: scaleCalibration,
                maxWeight: maxWeight,
            }),
            statusCode: {
                200: function(data) {
                    // console.log(data);
                   // var json = JSON.parse(data);
                    Update(data);
                }
            }
        });
    }
}

function SetZeroPoint() {
    if (wasServerAwake) {
        $.post({
            url: "/api/set_zero_point",
            cache: false,
            contentType: 'application/json',
            dataType: 'json',
            statusCode: {
                200: function(data) {
                    //var json = JSON.parse(data);
                    Update(data);
                }
            }
        });
    }
}

function SetNewTest(name = null, size = 100, time = 0.2) {
    if (wasServerAwake) {
        $.post({
            url: "/api/set_new_test",
            cache: false,
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                name: name,
                size: size,
                time: time,
            }),
            statusCode: {
                200: function(data) {
                }
            }
        });
    }
}

function Delete(filename) {
    if (wasServerAwake) {
        $.post({
            url: "/delete",
            cache: false,
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                filename: filename,
            }),
            statusCode: {
                200: function(data) {
                    setFileManager(data);
                }
            }
        });
    }
}

function GetFileList() {
    if (wasServerAwake) {
        $.ajax({
            type: "GET",
            url: "/api/get_file_list",
            cache: false,
            dataType: "text/json",
            statusCode: {
                200: function(data) {
                    var json = JSON.parse(data.responseText);
                    
                    setFileManager(json);
                }
            }
        });
    }
}

function getDataStart() {   
    setTimeout(function() {wasServerAwake = true;}, 2000);
}

GetUpdate()

/*
function sendGCODE(gcode) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            // document.getElementById("coefficient_input").value = data["scales"]["scaleCalibration"];
            // Update(data);
        }
    };
    
    xhttp.open("GET", "scale_set?code=" + gcode, true);
    xhttp.send();
}

function getDataStart() {
    wasServerAwake = true;
    
    setTimeout(function () {
        updateID = window.setInterval(function() { if (wasServerAwake) { getDataUpdate(); } }, 1000);
    }, 2000);
}
function getDataUpdate() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            console.log(data);
            
            Update(data);
            //document.getElementById("coefficient_input").value = data["scales"]["scaleCalibration"];
        }
    };
    xhttp.open("GET", "update_data", true);
    xhttp.send();
}
*/

function Update(json) {
    setWeight(json["weight"], json["isGr"]);
    setTestDebug(json["testName"], json["testSize"], json["testPause"]);

    document.getElementById("coefficient_input").value = json["scaleCalibration"];
}

function setFileManager(json) {
    $("#list_files").empty();
                    
    for (let i = 0; i < json["files"]["length"]; i++) {
        $("#list_files").append("<p class=\"name_file_ref\">" + json["files"][i] + "</p>");
        $("#list_files").append("<a id=\"download_file_ref\" href=\"/download/" + json["files"][i] + "\"> Скачать </a>");

        var b_delete = $('<input/>').attr({
            type: "button",
            id: "remove_file_ref",
            value: "Удалить",
        });
        b_delete.click(function() { Delete(json["files"][i]); });
        $("#list_files").append(b_delete);
        
        
        //$("#list_files").append("<p>" + json["files"][i]  + "</p>")
        //x.append("<button class=\"button\" onclick=\"DownloadTable(\"1\")\">" + "Скачать" + "</button>");
        $("#list_files").append("<span><span/>");
        $("#list_files").append("<br/>");
        $("#list_files").append("<br/>");
    }
}

function setWeight(weight, mode) {
    document.getElementById("units").innerHTML = `${(mode) ? " кг." : " гр."}`;
    document.getElementById("weight").innerHTML = (mode) ?  Math.round(weight * 0.01) / 10 : weight;
}

function setTestDebug(name, size, pause) {
    document.getElementById("file_name_debug").innerHTML = `${name}`;

    var lastSize_STR = document.getElementById("file_size_debug").innerHTML;
    if (lastSize_STR === "Null" || size === "Null") {
        document.getElementById("file_size_debug").innerHTML = `${size}${(size === "Null") ? "" : "%"}`;
    } else {
        var lastSize = parseInt(document.getElementById("file_size_debug").innerHTML);
        document.getElementById("file_size_debug").innerHTML = `${(size > lastSize) ? size : lastSize}${(size === "Null") ? "" : "%"}`;
    }

    document.getElementById("file_pause_debug").innerHTML = `${(pause) ? "Приостановлено" : "Запущено"}`;
}