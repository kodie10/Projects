//Citation for the following page
//Date: 11/2/2022
//Adapted From:
//Source URL: https://github.com/osu-cs340-ecampus/nodejs-starter-app

function deleteType(typeID) {
    // Put our data we want to send in a javascript object
    let data = {
        type_id: typeID
    };
    // Setup our AJAX request
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "/delete-types-ajax", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    // Tell our AJAX request how to resolve
    xhttp.onreadystatechange = () => {
        if (xhttp.readyState == 4 && xhttp.status == 204) {
            // Add the new data to the table
            deleteRow(typeID);
        } else if (xhttp.readyState == 4 && xhttp.status != 204) {
            console.log("There was an error with the input.")
        }
    }
    // Send the request and wait for the response
    xhttp.send(JSON.stringify(data));
};


function deleteRow(typeID){
    let table = document.getElementById("Types-table");
    for (let i = 0, row; row = table.rows[i]; i++) {
        //iterate through rows
        //rows would be accessed using the "row" variable assigned in the for loop
        if (table.rows[i].getAttribute("data-value") == typeID) {
             table.deleteRow(i);
             deleteDropDownMenu(typeID);
             break;
        }
    }   
};
