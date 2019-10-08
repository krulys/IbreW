function setTimer(){
    document.getElementById("countdown-timer").style.webkitAnimationPlayState = "paused";
    document.getElementById("countdown-timer").style.opacity = 0
    document.getElementById("countdown-timer-text1").style.webkitAnimationPlayState = "paused";
    document.getElementById("countdown-timer-text1").style.opacity = 0
    document.getElementById("countdown-timer-text2").style.webkitAnimationPlayState = "paused";
    document.getElementById("countdown-timer-text2").style.opacity = 0
    document.getElementById("social-icons").style.webkitAnimationPlayState = "paused";
    // Set the date we're counting down to
    var countDownDate = new Date("Oct 10, 2019 09:30:00").getTime();
    // Update the count down every 1 second
    var x = setInterval(function() {

    // Get today's date and time
    var now = new Date().getTime();

    // Find the distance between now and the count down date
    var distance = countDownDate - now;

    // Time calculations for days, hours, minutes and seconds
    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    // Display the result in the element
   
    document.getElementById("countdown-timer").innerHTML = days + "d " + hours + "h "
    + minutes + "m " + seconds + "s ";
    document.getElementById("countdown-timer").style.webkitAnimationPlayState = "running";
    document.getElementById("countdown-timer").style.opacity = 1;
    document.getElementById("countdown-timer").addEventListener("animationend", function() {
        document.getElementById("countdown-timer-text1").style.webkitAnimationPlayState = "running";
        document.getElementById("countdown-timer-text1").style.opacity = 1;
        document.getElementById("countdown-timer-text1").addEventListener("animationend", function() {
            document.getElementById("countdown-timer-text2").style.webkitAnimationPlayState = "running";
            document.getElementById("countdown-timer-text2").style.opacity = 1;
            document.getElementById("countdown-timer-text2").addEventListener("animationend", function() {
                document.getElementById("social-icons").style.webkitAnimationPlayState = "running";
            },false);
        }, false);
    }, false);
    // If the count down is finished, write some text
    if (distance < 0) {
        clearInterval(x);
        document.getElementById("countdown-timer").innerHTML = "<img src='https://emoji.slack-edge.com/T0330CH2P/the_klaud/e8136277351e6c52.png' />";
    }
    }, 1000);
}