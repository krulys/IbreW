function handleWhatIsButton(event){
    var scroll = new SmoothScroll('a[href*="#"]', {
        speed: 1000
    });
    let vh = window.innerHeight * 0.01
    scroll.animateScroll(vh*90);
}

// We listen to the resize event
window.addEventListener('resize', () => {
    // We execute the same script as before
    let vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
    console.log(window.innerHeight);
    });
    

