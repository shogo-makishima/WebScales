var currentTestTableLenght = 0;
var wasServerAwake = false;

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

function SetNewTest(name = null, size = 10) {
    if (wasServerAwake) {
        $.post({
            url: "/api/set_new_test",
            cache: false,
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                name: name,
                size: size,
            }),
            statusCode: {
                200: function(data) {
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
                    
                    $("#list_files").empty();
                    
                    for (let i = 0; i < json["files"]["length"]; i++) {
                        $("#list_files").append("<a href=\"/download/" + json["files"][i] + "\">" + json["files"][i] + "</a>");
                        $("#list_files").append("<span><span/>");
                        $("#list_files").append("<br/>");
                    }
                    
                    // `<a href="${json["directory"]}/${json["files"][i]}>${json["files"][i]}</a>`;
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
    console.log(json);
    setWeight(json["weight"], json["isGr"]);
    setTestDebug(json["testName"], json["testSize"], json["testPause"])
}

function clearTable() {
    document.getElementById("test_table_body").innerHTML = "";
    currentTestTableLenght = 0;
}

function setTestTable(data) {
    clearTable();
    var table = data["table"];
    currentTestTableLenght = table["length"];
    for (let i = 0; i < table["length"]; i++) {
        document.getElementById("test_table_body").innerHTML += `
            <tr>
                <td id="test_table_td">${i}</td>
                <td id="test_table_td">${table[i]["weight"]}</td>
                <td id="test_table_td">${table[i]["lenght"]}</td>
            </tr>
        `;
    }
}

function setWeight(weight, mode) {
    document.getElementById("units").innerHTML = `${(mode) ? " кг." : " гр."}`;
    document.getElementById("weight").innerHTML = (mode) ?  Math.round(weight * 0.01) / 10 : weight;
}

function setTestDebug(name, size, pause) {
    document.getElementById("file_name_debug").innerHTML = `${name}`;
    document.getElementById("file_size_debug").innerHTML = `${size}`;
    document.getElementById("file_pause_debug").innerHTML = `${(pause) ? "Приостановлено" : "Запущено"}`;
}