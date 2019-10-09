function handleWhatIsButton(event){
    var scroll = new SmoothScroll('a[href*="#"]', {
        speed: 1000
    });
    let vh = window.innerHeight * 0.01
    scroll.animateScroll(vh*90);
}


    

