function handleRadios(){
    if ($("#order_select1").is(":checked")) {
        document.getElementById("customOrderForm").style.display = "none"
    }  
    else if ($("#order_select2").is(":checked")) {
        document.getElementById("customOrderForm").style.display = "block"
    }
}

function submitOrder(round_id){
    var person_id = document.getElementById("participant_select").value
    var xhr = new XMLHttpRequest();
    $('add_order_button').prop('disabled', true);
    var data = ""
    if ($("#order_select1").is(":checked")) { //Usual order
        var url = "/api/orders";
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        data = JSON.stringify({
            "person_id": person_id,
            "favDrink": true,
            "round_id": round_id
        });
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                location.reload()
            }
        }
        xhr.send(data);
    }  
    else if ($("#order_select2").is(":checked")) { //Custom order
        var url = "/api/orders";
        var drink_id = document.getElementById("drink_select").value
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        var data = JSON.stringify({
            "person_id": person_id,
            "favDrink": false,
            "round_id": round_id,
            "drink_id": drink_id
        });
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                location.reload()
            }
        }
        xhr.send(data);
    }
}