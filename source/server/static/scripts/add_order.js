function handleRadios(){
    if ($("#order_select1").is(":checked")) {
        document.getElementById("customOrderForm").style.display = "none"
    }  
    else if ($("#order_select2").is(":checked")) {
        document.getElementById("customOrderForm").style.display = "block"
    }
}

function submitOrder(){
    //TODO submit order
    alert("submitted!")
}