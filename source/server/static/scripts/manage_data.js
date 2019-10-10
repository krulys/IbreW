function handleAddPerson() {
    document.getElementById("person_name").value = ""
    document.getElementById("person_team").value = ""
    document.getElementById("commit_person_btn").value = -1
    document.getElementById("commit_person_btn").innerHTML = "Create Person"
    $('#edit_people_modal').modal("show")
}

function deletePerson(value){
    var xhr = new XMLHttpRequest();
    var url = "/api/people";
    xhr.open("DELETE", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({
        "person_id": value
    });
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            location.reload()
        }
    }
    xhr.send(data);
}

function handlePeopleEditButton(value) {
    personName = document.getElementById("person_name-"+value).innerHTML
    personTeam = document.getElementById("person_team-"+value).innerHTML

    document.getElementById("person_name").value = personName
    document.getElementById("person_team").value = personTeam
    document.getElementById("commit_person_btn").value = value
    document.getElementById("commit_person_btn").innerHTML = "Commit changes"
    $('#edit_people_modal').modal("show")
}

function handlePeopleEditCommit(value){
    var xhr = new XMLHttpRequest();
    var url = "/api/people";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({
        "person_id": value,
        "displayName": document.getElementById("person_name").value,
        "name": document.getElementById("person_name").value.toLowerCase(),
        "team": document.getElementById("person_team").value,
        "favDrink_id": document.getElementById("drink_select").value
    });
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            location.reload()
        }
    }
    xhr.send(data);
    document.getElementById("commit_person_btn").innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>'
}


function handleAddDrink() {
    document.getElementById("drink_name").value = ""
    document.getElementById("drink_type").value = ""
    document.getElementById("drink_recipe").value = ""
    document.getElementById("commit_drink_btn").value = -1
    document.getElementById("commit_drink_btn").innerHTML = "Create Drink"
    $('#edit_drinks_modal').modal("show")
}

function handleDrinkEditButton(value) {
    drinkName = document.getElementById("drink_name-"+value).innerHTML
    drinkType = document.getElementById("drink_type-"+value).innerHTML
    drinkRecipe = document.getElementById("drink_recipe-"+value).innerHTML
    document.getElementById("drink_name").value = drinkName
    document.getElementById("drink_type").value = drinkType
    document.getElementById("drink_recipe").value = drinkRecipe
    document.getElementById("commit_drink_btn").value = value
    document.getElementById("commit_drink_btn").innerHTML = "Commit changes"
    $('#edit_drinks_modal').modal("show")
}

function handleDrinkEditCommit(value){
    form = document.getElementById("edit_drink_form")
    var xhr = new XMLHttpRequest();
    var url = "/api/drinks";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({
        "drink_id": value,
        "displayName": document.getElementById("drink_name").value,
        "drink_type": document.getElementById("drink_type").value.toLowerCase(),
        "recipe": (document.getElementById("drink_recipe").value == "" ? null : document.getElementById("drink_recipe").value )
    });
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            location.reload()
        }
    }
    xhr.send(data);
    document.getElementById("commit_drink_btn").innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>'
}

function deleteDrink(value){
    var xhr = new XMLHttpRequest();
    var url = "/api/drinks";
    xhr.open("DELETE", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({
        "drink_id": value
    });
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            location.reload()
        }
    }
    xhr.send(data);
}

function deleteRound(value){
    var xhr = new XMLHttpRequest();
    var url = "/api/rounds";
    xhr.open("DELETE", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({
        "round_id": value
    });
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            location.reload()
        }
    }
    xhr.send(data);
}

function deleteOrder(value){
    var xhr = new XMLHttpRequest();
    var url = "/api/orders";
    xhr.open("DELETE", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({
        "order_id": value
    });
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            location.reload()
        }
    }
    xhr.send(data);
}

function start_round(){
    var brewer_id = document.getElementById("initiator_select").value
    var time = document.getElementById("brew_time").value
    var xhr = new XMLHttpRequest();
    var url = "/api/rounds";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"initiator": brewer_id, "time": time});
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            location.reload()
        }
    }
    xhr.send(data);
    document.getElementById("start_round_btn").innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>'
}

function handleAddOrder(){
    var roundID = document.getElementById("round_select").value
    location.href = '/round/id/'+roundID;
}

is_timer_past_colon = false
function appendColonToTime(){
    time_input_val = document.getElementById("brew_time").value
    if (time_input_val.length == 2 && !is_timer_past_colon){
        is_timer_past_colon = true
        document.getElementById("brew_time").value = time_input_val + ":"
    }
    else if(time_input_val.length == 2 && is_timer_past_colon){
        is_timer_past_colon = false
        document.getElementById("brew_time").value = time_input_val.substring(0,time_input_val.length-1)
    }
}