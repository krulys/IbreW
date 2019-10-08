is_timer_past_colon = false
is_started_round = false
function appendColonToTime(event){
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

function start_round(event){
    var brewer_id = document.getElementById("initiator_select").value
    var time = document.getElementById("brew_time").value
    var newRoundID = ""

    console.log(JSON.stringify({"initiator": brewer_id, "time": time}))
    console.log("id: " + brewer_id)
    console.log("time: "+ time)
    if(!is_started_round){
        var xhr = new XMLHttpRequest();
        var url = "/api/rounds";
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        var data = JSON.stringify({"initiator": brewer_id, "time": time});
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                is_started_round = false
                $('#start_modal').modal("hide")
                document.getElementById("start_round_btn").innerHTML = "Start!"
                newRoundLink = "https://IbreW.io/round/id/".concat(xhr.responseText);
                document.getElementById("round_link").innerHTML = newRoundLink
                document.getElementById("round_link").setAttribute('href', "/round/id/".concat(xhr.responseText));
                $('#link_modal').modal()
            }
        }
        xhr.send(data);
        is_started_round = true
        document.getElementById("start_round_btn").innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>'
    }
}